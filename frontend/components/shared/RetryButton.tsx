"use client";

import { Button } from "@/components/ui/button";

interface RetryButtonProps {
  onRetry: () => void;
  label?: string;
}

export function RetryButton({ onRetry, label = "Retry" }: RetryButtonProps) {
  return (
    <Button onClick={onRetry} variant="outline" size="sm">
      {label}
    </Button>
  );
}

