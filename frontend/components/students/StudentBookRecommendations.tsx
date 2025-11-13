"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import Image from "next/image";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { BookDetailModal } from "@/components/ui/book-detail-modal";
import { BookRecommendationResponse } from "@/lib/types";
import { getBookDetails } from "@/lib/actions";
import { cn } from "@/lib/utils";
import { BookOpen, Loader2 } from "lucide-react";

interface StudentBookRecommendationsProps {
  books: BookRecommendationResponse[];
  studentName: string;
}

export function StudentBookRecommendations({
  books,
  studentName,
}: StudentBookRecommendationsProps) {
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
    books.forEach((book) => {
      if (!fetchedBooksRef.current.has(book.book_id)) {
        fetchBookCover(book.book_id, book.title, book.author);
      }
    });
  }, [books, fetchBookCover]);

  if (books.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Book Recommendations</CardTitle>
          <CardDescription>
            These books will challenge {studentName} with new vocabulary words while reinforcing words they already know.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No book recommendations available.</p>
        </CardContent>
      </Card>
    );
  }

  const selectedBook = books.find((b) => b.book_id === selectedBookId);

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Book Recommendations</CardTitle>
          <CardDescription>
            These books will challenge {studentName} with new vocabulary words while reinforcing words they already know.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            {books.map((book) => {
              const coverUrl = bookCovers.get(book.book_id);
              const isLoadingCover = loadingCovers.has(book.book_id);

              return (
                <Card
                  key={book.book_id}
                  className="border-2 cursor-pointer hover:border-primary transition-colors"
                  onClick={() => setSelectedBookId(book.book_id)}
                >
                  <CardHeader>
                    <div className="mb-3 flex justify-center">
                      {isLoadingCover ? (
                        <div className="w-32 h-48 bg-muted rounded flex items-center justify-center">
                          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
                        </div>
                      ) : coverUrl ? (
                        <div className="relative w-32 h-48 rounded overflow-hidden shadow-md">
                          <Image
                            src={coverUrl}
                            alt={`Cover of ${book.title}`}
                            fill
                            className="object-cover"
                            sizes="128px"
                            priority
                          />
                        </div>
                      ) : (
                        <div className="w-32 h-48 bg-muted rounded flex flex-col items-center justify-center p-2 shadow-md">
                          <BookOpen className="h-10 w-10 text-muted-foreground mb-1" />
                          <p className="text-xs text-muted-foreground text-center font-medium line-clamp-2">
                            {book.title}
                          </p>
                        </div>
                      )}
                    </div>

                    <div className="mb-2">
                      <CardTitle className="text-lg mb-1">{book.title}</CardTitle>
                      {book.author && (
                        <CardDescription className="text-xs">
                          by {book.author}
                        </CardDescription>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    {book.reading_level && (
                      <p className="text-xs text-muted-foreground">
                        Reading Level: {book.reading_level.toFixed(1)}
                      </p>
                    )}
                    <div className="text-sm">
                      <p className="font-medium">
                        Known: {(book.known_words_percent * 100).toFixed(1)}% | New:{" "}
                        {((1 - book.known_words_percent) * 100).toFixed(1)}% ({book.new_words_count} words)
                      </p>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {selectedBook && (
        <BookDetailModal
          book={selectedBook}
          open={selectedBookId !== null}
          onOpenChange={(open) => !open && setSelectedBookId(null)}
          preloadedCoverUrl={bookCovers.get(selectedBook.book_id) ?? undefined}
          preloadedBookDetails={bookDetailsCache.get(selectedBook.book_id) ?? undefined}
        />
      )}
    </>
  );
}

