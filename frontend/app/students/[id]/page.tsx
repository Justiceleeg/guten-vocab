"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { StudentDetailResponse } from "@/lib/types";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";

export default function StudentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const studentId = params?.id ? parseInt(params.id as string, 10) : null;
  
  const [student, setStudent] = useState<StudentDetailResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    if (!studentId || isNaN(studentId)) {
      setError("Invalid student ID");
      setLoading(false);
      return;
    }

    const fetchStudent = async () => {
      try {
        setLoading(true);
        setError(null);
        setNotFound(false);
        const data = await api.getStudentById(studentId);
        setStudent(data);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Failed to load student";
        setError(errorMessage);
        
        // Check if it's a 404 error
        if (errorMessage.includes("Not Found") || errorMessage.includes("404")) {
          setNotFound(true);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchStudent();
  }, [studentId]);

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-muted-foreground">Loading student data...</div>
      </div>
    );
  }

  if (notFound || error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <nav className="mb-4" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-muted-foreground">
            <li>
              <Link href="/" className="hover:text-foreground">
                Home
              </Link>
            </li>
            <li>/</li>
            <li>
              <Link href="/students" className="hover:text-foreground">
                Students
              </Link>
            </li>
            <li>/</li>
            <li className="text-foreground">Student Not Found</li>
          </ol>
        </nav>
        
        <div className="text-red-600 dark:text-red-400 mb-4">
          {notFound ? (
            <div>
              <h1 className="text-2xl font-bold mb-2">Student Not Found</h1>
              <p>Sorry, we couldn't find the student you're looking for.</p>
            </div>
          ) : (
            <div>
              <h1 className="text-2xl font-bold mb-2">Error</h1>
              <p>{error}</p>
            </div>
          )}
        </div>
        
        <Link
          href="/students"
          className="inline-block px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
        >
          Back to Students
        </Link>
      </div>
    );
  }

  if (!student) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-muted-foreground">No student data available.</div>
      </div>
    );
  }

  const getMasteryColor = (percent: number) => {
    if (percent < 50) {
      return "text-red-600 dark:text-red-400";
    } else if (percent < 75) {
      return "text-yellow-600 dark:text-yellow-400";
    } else {
      return "text-green-600 dark:text-green-400";
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

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Breadcrumbs */}
      <nav className="mb-6" aria-label="Breadcrumb">
        <ol className="flex items-center space-x-2 text-sm text-muted-foreground">
          <li>
            <Link href="/" className="hover:text-foreground">
              Home
            </Link>
          </li>
          <li>/</li>
          <li>
            <Link href="/students" className="hover:text-foreground">
              Students
            </Link>
          </li>
          <li>/</li>
          <li className="text-foreground">{student.name}</li>
        </ol>
      </nav>

      <div className="space-y-6">
        {/* Section 1: Student Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Student Overview</CardTitle>
            <CardDescription>
              Basic information and vocabulary mastery
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">{student.name}</h2>
              <div className="text-muted-foreground space-y-1">
                <p>Reading Level: {student.reading_level.toFixed(1)}</p>
                <p>Assigned Grade: {student.assigned_grade}</p>
              </div>
            </div>
            
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Grade Mastery</span>
                <span className={cn("text-sm font-semibold", getMasteryColor(student.vocab_mastery.mastery_percent))}>
                  {student.vocab_mastery.mastery_percent.toFixed(1)}%
                </span>
              </div>
              <Progress value={student.vocab_mastery.mastery_percent} className="h-3" />
              <p className="text-sm text-muted-foreground">
                {student.vocab_mastery.words_mastered} of {student.vocab_mastery.total_grade_level_words} words mastered
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Section 2: Book Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle>Book Recommendations</CardTitle>
            <CardDescription>
              Personalized book suggestions based on vocabulary profile
            </CardDescription>
          </CardHeader>
          <CardContent>
            {student.book_recommendations.length === 0 ? (
              <p className="text-muted-foreground">No book recommendations available.</p>
            ) : (
              <div className="grid gap-4 md:grid-cols-3">
                {student.book_recommendations.map((book) => (
                  <Card key={book.book_id} className="border-2">
                    <CardHeader>
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <CardTitle className="text-lg mb-1">{book.title}</CardTitle>
                          {book.author && (
                            <CardDescription className="text-xs">
                              by {book.author}
                            </CardDescription>
                          )}
                        </div>
                        <div className="ml-2 text-right">
                          <div className={cn("text-sm font-semibold", getMatchScoreColor(book.match_score))}>
                            {(book.match_score * 100).toFixed(0)}% match
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {book.reading_level && (
                        <p className="text-xs text-muted-foreground">
                          Reading Level: {book.reading_level.toFixed(1)}
                        </p>
                      )}
                      <div className="text-sm">
                        <p className="font-medium mb-1">
                          Known: {(book.known_words_percent * 100).toFixed(1)}% | New: {((1 - book.known_words_percent) * 100).toFixed(1)}% ({book.new_words_count} words)
                        </p>
                        <p className="text-muted-foreground text-xs">
                          This book will challenge you with {book.new_words_count} new vocabulary words while reinforcing words you already know.
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Section 3: Vocabulary Progress */}
        <Card>
          <CardHeader>
            <CardTitle>Vocabulary Progress</CardTitle>
            <CardDescription>
              Grade-level vocabulary mastery and missing words
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">
                  Mastered {student.vocab_mastery.words_mastered} of {student.vocab_mastery.total_grade_level_words} {student.assigned_grade}th grade words ({student.vocab_mastery.mastery_percent.toFixed(1)}%)
                </span>
              </div>
              <Progress value={student.vocab_mastery.mastery_percent} className="h-3" />
            </div>

            {student.missing_words.length > 0 ? (
              <Collapsible>
                <CollapsibleTrigger className="flex items-center justify-between w-full text-left text-sm font-medium hover:text-foreground transition-colors">
                  <span>{student.missing_words.length} missing words</span>
                  <span className="text-muted-foreground">▼</span>
                </CollapsibleTrigger>
                <CollapsibleContent className="mt-2">
                  <div className="border rounded-md p-4 bg-muted/50">
                    <div className="flex flex-wrap gap-2">
                      {student.missing_words.map((word, index) => (
                        <span
                          key={index}
                          className="inline-block px-2 py-1 text-xs bg-background border rounded-md"
                        >
                          {word}
                        </span>
                      ))}
                    </div>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            ) : (
              <p className="text-sm text-muted-foreground">
                All grade-level vocabulary words have been mastered! 🎉
              </p>
            )}
          </CardContent>
        </Card>

        {/* Section 4: Vocabulary Issues */}
        <Card>
          <CardHeader>
            <CardTitle>Words Used Incorrectly</CardTitle>
            <CardDescription>
              Vocabulary words that need attention
            </CardDescription>
          </CardHeader>
          <CardContent>
            {student.misused_words.length === 0 ? (
              <p className="text-muted-foreground">No misused words found. Great job! 🎉</p>
            ) : (
              <div className="space-y-4">
                {student.misused_words.map((misused, index) => (
                  <Card key={index} className="border-orange-200 dark:border-orange-900">
                    <CardHeader>
                      <CardTitle className="text-lg">{misused.word}</CardTitle>
                      <CardDescription>
                        Correct: {misused.correct_count} | Incorrect: {misused.incorrect_count}
                      </CardDescription>
                    </CardHeader>
                    {misused.example && (
                      <CardContent>
                        <p className="text-sm">
                          <span className="text-muted-foreground">Example: </span>
                          <span className="italic">
                            {(() => {
                              const regex = new RegExp(`\\b${misused.word}\\b`, 'gi');
                              const parts = misused.example.split(regex);
                              const matches = misused.example.match(regex) || [];
                              const result = [];
                              for (let i = 0; i < parts.length; i++) {
                                result.push(<span key={`part-${i}`}>{parts[i]}</span>);
                                if (i < matches.length) {
                                  result.push(
                                    <span key={`match-${i}`} className="font-bold text-orange-600 dark:text-orange-400 underline">
                                      {matches[i]}
                                    </span>
                                  );
                                }
                              }
                              return result;
                            })()}
                          </span>
                        </p>
                      </CardContent>
                    )}
                  </Card>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

