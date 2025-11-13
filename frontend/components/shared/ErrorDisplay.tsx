"use client";

import { RetryButton } from "./RetryButton";

interface ErrorDisplayProps {
  error: string;
  onRetry?: () => void;
}

export function ErrorDisplay({ error, onRetry }: ErrorDisplayProps) {
  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      window.location.reload();
    }
  };

  return (
    <div>
      <div className="text-red-600 dark:text-red-400 mb-4">
        Error: {error}
      </div>
      <RetryButton onRetry={handleRetry} />
    </div>
  );
}

