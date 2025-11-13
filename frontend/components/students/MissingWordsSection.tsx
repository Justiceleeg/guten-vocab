"use client";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Progress } from "@/components/ui/progress";

interface MissingWordsSectionProps {
  totalWords: number;
  wordsMastered: number;
  masteryPercent: number;
  assignedGrade: number;
  missingWords: string[];
}

export function MissingWordsSection({
  totalWords,
  wordsMastered,
  masteryPercent,
  assignedGrade,
  missingWords,
}: MissingWordsSectionProps) {
  return (
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
              Mastered {wordsMastered} of {totalWords} {assignedGrade}th grade words ({masteryPercent.toFixed(1)}%)
            </span>
          </div>
          <Progress value={masteryPercent} className="h-3" />
        </div>

        {missingWords.length > 0 ? (
          <Collapsible>
            <CollapsibleTrigger className="flex items-center justify-between w-full text-left text-sm font-medium hover:text-foreground transition-colors">
              <span>{missingWords.length} missing words</span>
              <span className="text-muted-foreground">▼</span>
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-2">
              <div className="border rounded-md p-4 bg-muted/50">
                <div className="flex flex-wrap gap-2">
                  {missingWords.map((word, index) => (
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
  );
}

