"use client";

import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MisusedWordResponse } from "@/lib/types";
import { DismissVocabularyButton } from "./DismissVocabularyButton";

interface MisusedWordsSectionProps {
  misusedWords: MisusedWordResponse[];
  studentId: number;
  onWordDismissed: (wordId: number) => void;
}

export function MisusedWordsSection({
  misusedWords,
  studentId,
  onWordDismissed,
}: MisusedWordsSectionProps) {
  const [dismissedWords, setDismissedWords] = useState<Set<number>>(new Set());

  const handleDismissed = (wordId: number) => {
    setDismissedWords((prev) => new Set(prev).add(wordId));
    onWordDismissed(wordId);
  };

  const visibleWords = misusedWords.filter((w) => !dismissedWords.has(w.word_id));

  if (visibleWords.length === 0 && misusedWords.length > 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Words Used Incorrectly</CardTitle>
          <CardDescription>
            Vocabulary words that need attention
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No misused words found. Great job! 🎉</p>
        </CardContent>
      </Card>
    );
  }

  if (visibleWords.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Words Used Incorrectly</CardTitle>
          <CardDescription>
            Vocabulary words that need attention
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">No misused words found. Great job! 🎉</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Words Used Incorrectly</CardTitle>
        <CardDescription>
          Vocabulary words that need attention
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {visibleWords.map((misused, index) => (
            <Card key={index} className="border-orange-200 dark:border-orange-900 relative">
              <CardHeader className="pr-16">
                <CardTitle className="text-lg">{misused.word}</CardTitle>
                <CardDescription>
                  Correct: {misused.correct_count} | Incorrect: {misused.incorrect_count}
                </CardDescription>

                <div className="absolute top-4 right-4">
                  <DismissVocabularyButton
                    wordId={misused.word_id}
                    studentId={studentId}
                    onDismissed={() => handleDismissed(misused.word_id)}
                  />
                </div>
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
      </CardContent>
    </Card>
  );
}

