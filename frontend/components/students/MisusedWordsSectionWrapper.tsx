"use client";

import { useRouter } from "next/navigation";
import { MisusedWordsSection } from "./MisusedWordsSection";
import { MisusedWordResponse } from "@/lib/types";

interface MisusedWordsSectionWrapperProps {
  misusedWords: MisusedWordResponse[];
  studentId: number;
}

export function MisusedWordsSectionWrapper({
  misusedWords,
  studentId,
}: MisusedWordsSectionWrapperProps) {
  const router = useRouter();

  const handleWordDismissed = () => {
    // Refresh the page to show updated data
    router.refresh();
  };

  return (
    <MisusedWordsSection
      misusedWords={misusedWords}
      studentId={studentId}
      onWordDismissed={handleWordDismissed}
    />
  );
}

