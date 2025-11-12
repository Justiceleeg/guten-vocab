"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { BookRecommendationResponse, ClassRecommendationResponse } from "@/lib/types";
import { openLibraryApi } from "@/lib/api";
import { BookOpen, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import Image from "next/image";

interface BookDetailModalProps {
  book: BookRecommendationResponse | ClassRecommendationResponse;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  isClassView?: boolean;
  totalStudents?: number;
}

export function BookDetailModal({
  book,
  open,
  onOpenChange,
  isClassView = false,
  totalStudents,
}: BookDetailModalProps) {
  const [loading, setLoading] = useState(false);
  const [bookDetails, setBookDetails] = useState<{
    coverUrl: string | null;
    summary: string | null;
    pageCount: number | null;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open && !bookDetails) {
      fetchBookDetails();
    }
  }, [open]);

  const fetchBookDetails = async () => {
    setLoading(true);
    setError(null);
    try {
      const details = await openLibraryApi.getBookDetails(book.title, book.author);
      setBookDetails(details);
    } catch (err) {
      setError("Failed to load book details");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getMatchScoreColor = (score: number) => {
    if (score >= 0.8) {
      return "text-green-600 dark:text-green-400";
    } else if (score >= 0.6) {
      return "text-yellow-600 dark:text-yellow-400";
    } else {
      return "text-orange-600 dark:text-orange-400";
    }
  };

  const matchScore = "match_score" in book ? book.match_score : book.avg_match_score;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl">{book.title}</DialogTitle>
          {book.author && (
            <DialogDescription className="text-base">
              by {book.author}
            </DialogDescription>
          )}
        </DialogHeader>

        <div className="space-y-4 mt-4">
          {/* Book Cover */}
          <div className="flex justify-center">
            {loading ? (
              <div className="w-48 h-72 bg-muted rounded-lg flex items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              </div>
            ) : bookDetails?.coverUrl ? (
              <div className="relative w-48 h-72 rounded-lg overflow-hidden shadow-lg">
                <Image
                  src={bookDetails.coverUrl}
                  alt={`Cover of ${book.title}`}
                  fill
                  className="object-cover"
                  unoptimized
                />
              </div>
            ) : (
              <div className="w-48 h-72 bg-muted rounded-lg flex flex-col items-center justify-center p-4 shadow-lg">
                <BookOpen className="h-16 w-16 text-muted-foreground mb-2" />
                <p className="text-sm text-muted-foreground text-center font-medium">
                  {book.title}
                </p>
                {book.author && (
                  <p className="text-xs text-muted-foreground text-center mt-1">
                    {book.author}
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Book Details */}
          <div className="grid grid-cols-2 gap-4">
            {book.reading_level && (
              <div>
                <p className="text-sm text-muted-foreground">Reading Level</p>
                <p className="font-semibold">Grade {book.reading_level.toFixed(1)}</p>
              </div>
            )}
            {bookDetails?.pageCount && (
              <div>
                <p className="text-sm text-muted-foreground">Pages</p>
                <p className="font-semibold">{bookDetails.pageCount}</p>
              </div>
            )}
          </div>

          {/* Match Score */}
          <div>
            <p className="text-sm text-muted-foreground mb-1">Match Score</p>
            <div className="flex items-center gap-2">
              <span className={cn("text-lg font-semibold", getMatchScoreColor(matchScore))}>
                {(matchScore * 100).toFixed(0)}%
              </span>
              {isClassView && "students_recommended_count" in book && (
                <span className="text-sm text-muted-foreground">
                  (Recommended for {book.students_recommended_count} of {totalStudents || "?"} students)
                </span>
              )}
            </div>
          </div>

          {/* Vocabulary Stats */}
          {"known_words_percent" in book && (
            <div>
              <p className="text-sm text-muted-foreground mb-1">Vocabulary</p>
              <p className="text-sm">
                Known: {(book.known_words_percent * 100).toFixed(1)}% | New:{" "}
                {((1 - book.known_words_percent) * 100).toFixed(1)}% ({book.new_words_count} words)
              </p>
            </div>
          )}

          {/* Summary */}
          {error ? (
            <div className="text-sm text-muted-foreground">
              Unable to load book summary at this time.
            </div>
          ) : bookDetails?.summary ? (
            <div>
              <p className="text-sm font-semibold mb-2">Summary</p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {bookDetails.summary}
              </p>
            </div>
          ) : loading ? (
            <div className="text-sm text-muted-foreground">Loading summary...</div>
          ) : null}
        </div>
      </DialogContent>
    </Dialog>
  );
}

