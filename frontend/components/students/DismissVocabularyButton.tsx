"use client";

import { useState } from "react";
import { api } from "@/lib/api";

interface DismissVocabularyButtonProps {
  wordId: number;
  studentId: number;
  onDismissed: () => void;
}

export function DismissVocabularyButton({
  wordId,
  studentId,
  onDismissed,
}: DismissVocabularyButtonProps) {
  const [dismissingWordId, setDismissingWordId] = useState<number | null>(null);
  const [isDismissing, setIsDismissing] = useState(false);
  const [showButtons, setShowButtons] = useState(false);

  const handleDismissClick = () => {
    setShowButtons(true);
  };

  const handleDismiss = async (reason: 'addressed' | 'ai_error') => {
    try {
      setIsDismissing(true);
      setDismissingWordId(wordId);
      await api.dismissVocabulary(studentId, wordId, reason);
      onDismissed();
      setShowButtons(false);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to dismiss";
      alert(`Error: ${errorMessage}`);
      setIsDismissing(false);
      setDismissingWordId(null);
    }
  };

  const handleCancel = () => {
    setShowButtons(false);
  };

  if (isDismissing) {
    return (
      <div className="text-xs text-muted-foreground">Dismissing...</div>
    );
  }

  if (showButtons) {
    return (
      <div className="flex gap-1 animate-in fade-in slide-in-from-left-2 duration-200">
        <button
          onClick={() => handleDismiss('addressed')}
          className="px-2 py-1 text-xs bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
          title="I've corrected the student"
        >
          Addressed
        </button>
        <button
          onClick={() => handleDismiss('ai_error')}
          className="px-2 py-1 text-xs bg-orange-600 hover:bg-orange-700 text-white rounded transition-colors"
          title="This is an AI detection error"
        >
          AI Error
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={handleDismissClick}
      className="text-muted-foreground hover:text-foreground transition-colors p-1"
      aria-label="Dismiss this vocabulary issue"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  );
}

