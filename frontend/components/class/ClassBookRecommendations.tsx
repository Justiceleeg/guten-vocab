"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Image from "next/image";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { BookDetailModal } from "@/components/ui/book-detail-modal";
import { ClassRecommendationResponse, ClassStatsResponse } from "@/lib/types";
import { getBookDetails } from "@/lib/actions";
import { BookOpen, Loader2 } from "lucide-react";

interface ClassBookRecommendationsProps {
  recommendations: ClassRecommendationResponse[];
  totalStudents?: number;
}

export function ClassBookRecommendations({
  recommendations,
  totalStudents,
}: ClassBookRecommendationsProps) {
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [bookCovers, setBookCovers] = useState<Map<number, string | null>>(new Map());
  const [loadingCovers, setLoadingCovers] = useState<Set<number>>(new Set());
  const [bookDetailsCache, setBookDetailsCache] = useState<Map<number, {
    coverUrl: string | null;
    summary: string | null;
    pageCount: number | null;
  }>>(new Map());
  // Use ref to track fetched books to prevent duplicate fetches
  const fetchedBooksRef = useRef<Set<number>>(new Set());

  const fetchBookCover = useCallback(async (bookId: number, title: string, author: string | null) => {
    // Single source of truth check - exit if already fetched
    if (fetchedBooksRef.current.has(bookId)) {
      return;
    }
    
    // Mark as fetched immediately to prevent duplicate requests
    fetchedBooksRef.current.add(bookId);
    setLoadingCovers((prev) => new Set(prev).add(bookId));
    
    try {
      const details = await getBookDetails(title, author);
      setBookCovers((prev) => {
        const next = new Map(prev);
        next.set(bookId, details.coverUrl);
        return next;
      });
      // Cache full details for modal
      setBookDetailsCache((prev) => {
        const next = new Map(prev);
        next.set(bookId, details);
        return next;
      });
    } catch (err) {
      setBookCovers((prev) => {
        const next = new Map(prev);
        next.set(bookId, null);
        return next;
      });
      setBookDetailsCache((prev) => {
        const next = new Map(prev);
        next.set(bookId, { coverUrl: null, summary: null, pageCount: null });
        return next;
      });
    } finally {
      setLoadingCovers((prev) => {
        const next = new Set(prev);
        next.delete(bookId);
        return next;
      });
    }
  }, []);

  useEffect(() => {
    // Fetch covers for any books that haven't been fetched yet
    recommendations.forEach((book) => {
      if (!fetchedBooksRef.current.has(book.book_id)) {
        fetchBookCover(book.book_id, book.title, book.author);
      }
    });
  }, [recommendations, fetchBookCover]);

  if (recommendations.length === 0) {
    return (
      <Card>
        <CardContent className="py-12 text-center">
          <BookOpen className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <p className="text-muted-foreground">No book recommendations available yet</p>
        </CardContent>
      </Card>
    );
  }

  const selectedBook = recommendations.find((b) => b.book_id === selectedBookId);

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {recommendations.map((book) => {
          const coverUrl = bookCovers.get(book.book_id);
          const isLoadingCover = loadingCovers.has(book.book_id);

          return (
            <Card
              key={book.book_id}
              className="border-2 hover:border-primary transition-colors cursor-pointer"
              onClick={() => setSelectedBookId(book.book_id)}
            >
              <CardHeader>
                <div className="flex gap-4">
                  <div className="flex-shrink-0">
                    {isLoadingCover ? (
                      <div className="h-24 w-16 bg-muted rounded flex items-center justify-center">
                        <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                      </div>
                    ) : coverUrl ? (
                      <div className="relative h-24 w-16 rounded overflow-hidden shadow-md">
                        <Image
                          src={coverUrl}
                          alt={`Cover of ${book.title}`}
                          fill
                          className="object-cover"
                          sizes="64px"
                          priority
                        />
                      </div>
                    ) : (
                      <div className="h-24 w-16 bg-muted rounded flex items-center justify-center">
                        <BookOpen className="h-8 w-8 text-muted-foreground" />
                      </div>
                    )}
                  </div>
                  <div className="flex-1">
                    <CardTitle className="text-xl">{book.title}</CardTitle>
                    {book.author && (
                      <CardDescription className="mt-1">by {book.author}</CardDescription>
                    )}
                    {book.reading_level && (
                      <div className="text-sm text-muted-foreground mt-1">
                        Grade Level: {book.reading_level.toFixed(1)}
                      </div>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium">
                    Recommended for {book.students_recommended_count} of{" "}
                    {totalStudents || "?"} students
                  </span>
                </div>
                <p className="text-sm text-muted-foreground">
                  This book is recommended for most students in your class, offering appropriate
                  vocabulary challenge for {book.students_recommended_count} students.
                </p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {selectedBook && (
        <BookDetailModal
          book={selectedBook}
          open={selectedBookId !== null}
          onOpenChange={(open) => !open && setSelectedBookId(null)}
          isClassView={true}
          totalStudents={totalStudents}
          preloadedCoverUrl={bookCovers.get(selectedBook.book_id) ?? undefined}
          preloadedBookDetails={bookDetailsCache.get(selectedBook.book_id) ?? undefined}
        />
      )}
    </>
  );
}

