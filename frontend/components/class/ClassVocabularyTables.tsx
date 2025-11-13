"use client";

import { useState } from "react";
import { VocabularyTableCard } from "@/components/ui/vocabulary-table-card";
import { WordDetailModal } from "@/components/ui/word-detail-modal";
import { ClassStatsResponse } from "@/lib/types";
import { cn } from "@/lib/utils";

interface ClassVocabularyTablesProps {
  classStats: ClassStatsResponse;
}

export function ClassVocabularyTables({ classStats }: ClassVocabularyTablesProps) {
  const [selectedWord, setSelectedWord] = useState<string | null>(null);

  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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

      {selectedWord && (
        <WordDetailModal
          word={selectedWord}
          open={selectedWord !== null}
          onOpenChange={(open) => !open && setSelectedWord(null)}
        />
      )}
    </>
  );
}

