"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  ClassStatsResponse,
  ClassRecommendationResponse,
} from "@/lib/types";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { BookOpen, AlertTriangle, TrendingUp, Users } from "lucide-react";

export default function ClassOverviewPage() {
  const [classStats, setClassStats] = useState<ClassStatsResponse | null>(null);
  const [classRecommendations, setClassRecommendations] = useState<ClassRecommendationResponse[]>([]);
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(true);
  const [errorStats, setErrorStats] = useState<string | null>(null);
  const [errorRecommendations, setErrorRecommendations] = useState<string | null>(null);

  useEffect(() => {
    fetchClassStats();
    fetchClassRecommendations();
  }, []);

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
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="level" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="students" fill="hsl(var(--primary))" />
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
            {classRecommendations.map((book) => (
              <Card key={book.book_id} className="border-2 hover:border-primary transition-colors">
                <CardHeader>
                  <div className="flex gap-4">
                    <div className="h-24 w-16 bg-muted rounded flex items-center justify-center">
                      <BookOpen className="h-8 w-8 text-muted-foreground" />
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
            ))}
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
            <div>
              <h2 className="text-2xl font-semibold mb-4">Top 10 Words Students Need to Learn</h2>
              <Card>
                <CardContent className="pt-6">
                  {classStats.top_missing_words.length > 0 ? (
                    <>
                      <p className="text-sm text-muted-foreground mb-4">
                        Focus instruction on these words to help the most students
                      </p>
                      <Table>
                        <TableHeader>
                          <TableRow>
                            <TableHead>Word</TableHead>
                            <TableHead className="text-right">Total Students</TableHead>
                          </TableRow>
                        </TableHeader>
                        <TableBody>
                          {classStats.top_missing_words.map((item, index) => (
                            <TableRow key={index}>
                              <TableCell className="font-medium">{item.word}</TableCell>
                              <TableCell className="text-right">{item.students_missing}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </>
                  ) : (
                    <div className="py-12 text-center">
                      <p className="text-muted-foreground">No vocabulary gaps detected</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Section 4: Common Mistakes */}
            <div>
              <h2 className="text-2xl font-semibold mb-4">Words Frequently Used Incorrectly</h2>
              <Card>
                <CardContent className="pt-6">
                  {classStats.commonly_misused_words.length > 0 ? (
                    <>
                      <p className="text-sm text-muted-foreground mb-4">
                        Review these words with the class to address systematic misunderstandings
                      </p>
                      <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Word</TableHead>
                          <TableHead className="text-right">Total Misuses</TableHead>
                          {classStats.commonly_misused_words.some((w) => w.students_affected) && (
                            <TableHead className="text-right">Students Affected</TableHead>
                          )}
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {classStats.commonly_misused_words.map((item, index) => {
                          const isThrough = item.word.toLowerCase() === "through";
                          return (
                            <TableRow
                              key={index}
                              className={isThrough ? "bg-yellow-50 dark:bg-yellow-950/20" : ""}
                            >
                              <TableCell className={`font-medium ${isThrough ? "font-bold" : ""}`}>
                                {item.word}
                              </TableCell>
                              <TableCell className="text-right">{item.misuse_count}</TableCell>
                              {classStats.commonly_misused_words.some((w) => w.students_affected) && (
                                <TableCell className="text-right">
                                  {item.students_affected || "-"}
                                </TableCell>
                              )}
                            </TableRow>
                          );
                        })}
                      </TableBody>
                    </Table>
                    </>
                  ) : (
                    <div className="py-12 text-center">
                      <p className="text-muted-foreground">No common mistakes found</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}


