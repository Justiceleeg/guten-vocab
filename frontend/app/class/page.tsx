"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { api, openLibraryApi } from "@/lib/api";
import {
  ClassStatsResponse,
  ClassRecommendationResponse,
} from "@/lib/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { BookDetailModal } from "@/components/ui/book-detail-modal";
import { WordDetailModal } from "@/components/ui/word-detail-modal";
import { VocabularyTableCard } from "@/components/ui/vocabulary-table-card";
import { cn } from "@/lib/utils";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { BookOpen, AlertTriangle, TrendingUp, Users, Loader2 } from "lucide-react";

export default function ClassOverviewPage() {
  const [classStats, setClassStats] = useState<ClassStatsResponse | null>(null);
  const [classRecommendations, setClassRecommendations] = useState<ClassRecommendationResponse[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(true);
  const [errorStats, setErrorStats] = useState<string | null>(null);
  const [errorRecommendations, setErrorRecommendations] = useState<string | null>(null);
  
  // Book modal state
  const [selectedBookId, setSelectedBookId] = useState<number | null>(null);
  const [bookCovers, setBookCovers] = useState<Map<number, string | null>>(new Map());
  const [loadingCovers, setLoadingCovers] = useState<Set<number>>(new Set());
  
  // Word modal state
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [isDark, setIsDark] = useState(false);

  // Detect dark mode
  useEffect(() => {
    const checkDarkMode = () => {
      setIsDark(document.documentElement.classList.contains("dark"));
    };
    checkDarkMode();
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    fetchClassStats();
    fetchClassRecommendations();
  }, []);

  // Fetch book covers when recommendations load
  useEffect(() => {
    if (classRecommendations.length > 0) {
      classRecommendations.forEach((book) => {
        if (!bookCovers.has(book.book_id) && !loadingCovers.has(book.book_id)) {
          fetchBookCover(book.book_id, book.title, book.author);
        }
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [classRecommendations]);

  const fetchBookCover = async (bookId: number, title: string, author: string | null) => {
    setLoadingCovers((prev) => new Set(prev).add(bookId));
    try {
      const details = await openLibraryApi.getBookDetails(title, author);
      setBookCovers((prev) => {
        const next = new Map(prev);
        next.set(bookId, details.coverUrl);
        return next;
      });
    } catch (err) {
      setBookCovers((prev) => {
        const next = new Map(prev);
        next.set(bookId, null);
        return next;
      });
    } finally {
      setLoadingCovers((prev) => {
        const next = new Set(prev);
        next.delete(bookId);
        return next;
      });
    }
  };

  const fetchClassStats = async () => {
    try {
      setLoadingStats(true);
      setErrorStats(null);
      const data = await api.getClassStats();
      setClassStats(data);
    } catch (error) {
      setErrorStats(error instanceof Error ? error.message : "Failed to load class statistics");
    } finally {
      setLoadingStats(false);
    }
  };

  const fetchClassRecommendations = async () => {
    try {
      setLoadingRecommendations(true);
      setErrorRecommendations(null);
      const data = await api.getClassRecommendations();
      setClassRecommendations(data.slice(0, 2)); // Take only top 2
    } catch (error) {
      setErrorRecommendations(error instanceof Error ? error.message : "Failed to load class recommendations");
    } finally {
      setLoadingRecommendations(false);
    }
  };

  // Prepare chart data for reading level distribution
  const getReadingLevelChartData = () => {
    if (!classStats) return [];
    return Object.entries(classStats.reading_level_distribution)
      .map(([level, count]) => ({
        level: `Grade ${level}`,
        students: count,
      }))
      .sort((a, b) => {
        const levelA = parseInt(a.level.replace("Grade ", ""));
        const levelB = parseInt(b.level.replace("Grade ", ""));
        return levelA - levelB;
      });
  };

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Class Overview</h1>
        <p className="text-muted-foreground">
          View class-wide statistics, book recommendations, and vocabulary insights
        </p>
      </div>

      {/* Section 1: Class Statistics */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Class Statistics</h2>
        {loadingStats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <div className="h-6 bg-muted animate-pulse rounded" />
                </CardHeader>
                <CardContent>
                  <div className="h-20 bg-muted animate-pulse rounded" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : errorStats ? (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{errorStats}</AlertDescription>
            <Button onClick={fetchClassStats} variant="outline" size="sm" className="mt-2">
              Retry
            </Button>
          </Alert>
        ) : classStats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Total Students Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Total Students
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold">{classStats.total_students}</div>
                <p className="text-muted-foreground mt-2">students in the class</p>
              </CardContent>
            </Card>

            {/* Average Vocabulary Mastery Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Average Vocabulary Mastery
                </CardTitle>
                <CardDescription>Across all students</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold mb-4">
                  {classStats.avg_vocab_mastery_percent.toFixed(1)}%
                </div>
                <Progress value={classStats.avg_vocab_mastery_percent} className="h-3" />
                <p className="text-sm text-muted-foreground mt-2">
                  Words mastered correctly in context
                </p>
              </CardContent>
            </Card>

            {/* Reading Level Distribution Chart */}
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Reading Level Distribution</CardTitle>
                <CardDescription>Number of students at each grade level</CardDescription>
              </CardHeader>
              <CardContent>
                {getReadingLevelChartData().length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={getReadingLevelChartData()}>
                      <CartesianGrid 
                        strokeDasharray="3 3" 
                        stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
                        opacity={0.3}
                      />
                      <XAxis 
                        dataKey="level" 
                        tick={{ fill: isDark ? "oklch(0.7982 0.0243 82.1078)" : "oklch(0.5391 0.0387 71.1655)" }}
                        stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
                      />
                      <YAxis 
                        tick={{ fill: isDark ? "oklch(0.7982 0.0243 82.1078)" : "oklch(0.5391 0.0387 71.1655)" }}
                        stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
                      />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: isDark ? "oklch(0.3237 0.0155 59.0603)" : "oklch(0.9914 0.0098 87.4695)",
                          border: `1px solid ${isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}`,
                          borderRadius: "0.5rem",
                          color: isDark ? "oklch(0.9239 0.019 83.0636)" : "oklch(0.376 0.0225 64.3434)",
                        }}
                        labelStyle={{
                          color: isDark ? "oklch(0.9239 0.019 83.0636)" : "oklch(0.376 0.0225 64.3434)",
                          fontWeight: 600,
                        }}
                      />
                      <Bar 
                        dataKey="students" 
                        fill={isDark ? "oklch(0.7264 0.0581 66.6967)" : "oklch(0.618 0.0778 65.5444)"}
                        radius={[4, 4, 0, 0]}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <p className="text-muted-foreground text-center py-8">
                    No reading level data available
                  </p>
                )}
              </CardContent>
            </Card>
          </div>
        ) : null}
      </section>

      {/* Section 2: Class-Wide Book Recommendations */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Recommended Books for the Class</h2>
        {loadingRecommendations ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2].map((i) => (
              <Card key={i}>
                <CardHeader>
                  <div className="h-6 bg-muted animate-pulse rounded" />
                </CardHeader>
                <CardContent>
                  <div className="h-32 bg-muted animate-pulse rounded" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : errorRecommendations ? (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{errorRecommendations}</AlertDescription>
            <Button onClick={fetchClassRecommendations} variant="outline" size="sm" className="mt-2">
              Retry
            </Button>
          </Alert>
        ) : classRecommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {classRecommendations.map((book) => {
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
                      {/* Book Cover */}
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
                              unoptimized
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
                        {classStats?.total_students || "?"} students
                      </span>
                    </div>
                    <div>
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span className="text-muted-foreground">Average Match Score</span>
                        <span className="font-semibold">{(book.avg_match_score * 100).toFixed(0)}%</span>
                      </div>
                      <Progress value={book.avg_match_score * 100} className="h-2" />
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
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <BookOpen className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground">No book recommendations available yet</p>
            </CardContent>
          </Card>
        )}
      </section>

      {/* Sections 3 & 4: Vocabulary Gaps and Common Mistakes - Side by Side */}
      {classStats && (
        <section>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Section 3: Vocabulary Gaps */}
            <VocabularyTableCard
              title="Top 10 Words Students Need to Learn"
              description="Focus instruction on these words to help the most students"
              emptyMessage="No vocabulary gaps detected"
              columns={[
                { header: "Word", align: "left" },
                { header: "Total Students", align: "right" },
              ]}
              rows={classStats.top_missing_words.map((item, index) => ({
                key: index,
                cells: [
                  { content: item.word, className: "font-medium" },
                  { content: item.students_missing, className: "text-right" },
                ],
                onClick: () => setSelectedWord(item.word),
                rowClassName: "cursor-pointer hover:bg-muted/50",
              }))}
            />

            {/* Section 4: Common Mistakes */}
            <VocabularyTableCard
              title="Words Frequently Used Incorrectly"
              description="Review these words with the class to address systematic misunderstandings"
              emptyMessage="No common mistakes found"
              columns={[
                { header: "Word", align: "left" },
                { header: "Total Misuses", align: "right" },
                ...(classStats.commonly_misused_words.some((w) => w.students_affected)
                  ? [{ header: "Students Affected", align: "right" as const }]
                  : []),
              ]}
              rows={classStats.commonly_misused_words.map((item, index) => {
                const isThrough = item.word.toLowerCase() === "through";
                return {
                  key: index,
                  cells: [
                    {
                      content: item.word,
                      className: cn("font-medium", isThrough && "font-bold"),
                    },
                    { content: item.misuse_count, className: "text-right" },
                    ...(classStats.commonly_misused_words.some((w) => w.students_affected)
                      ? [
                          {
                            content: item.students_affected || "-",
                            className: "text-right",
                          },
                        ]
                      : []),
                  ],
                  onClick: () => setSelectedWord(item.word),
                  rowClassName: cn(
                    "cursor-pointer hover:bg-muted/50",
                    isThrough && "bg-yellow-50 dark:bg-yellow-950/20"
                  ),
                };
              })}
            />
          </div>
        </section>
      )}

      {/* Book Detail Modal */}
      {selectedBookId && classRecommendations.find((b) => b.book_id === selectedBookId) && (
        <BookDetailModal
          book={classRecommendations.find((b) => b.book_id === selectedBookId)!}
          open={selectedBookId !== null}
          onOpenChange={(open) => !open && setSelectedBookId(null)}
          isClassView={true}
          totalStudents={classStats?.total_students}
        />
      )}

      {/* Word Detail Modal */}
      {selectedWord && (
        <WordDetailModal
          word={selectedWord}
          open={selectedWord !== null}
          onOpenChange={(open) => !open && setSelectedWord(null)}
        />
      )}
    </div>
  );
}


