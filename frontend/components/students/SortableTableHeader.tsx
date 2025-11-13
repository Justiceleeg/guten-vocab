"use client";

import { useState } from "react";
import { ArrowUp, ArrowDown } from "lucide-react";

type SortDirection = "asc" | "desc";

interface SortableTableHeaderProps {
  defaultDirection?: SortDirection;
  onSortChange?: (direction: SortDirection) => void;
}

export function SortableTableHeader({
  defaultDirection = "desc",
  onSortChange,
}: SortableTableHeaderProps) {
  const [sortDirection, setSortDirection] = useState<SortDirection>(defaultDirection);

  const handleClick = () => {
    const newDirection = sortDirection === "desc" ? "asc" : "desc";
    setSortDirection(newDirection);
    onSortChange?.(newDirection);
  };

  return (
    <button
      onClick={handleClick}
      className="flex items-center gap-2 hover:text-foreground transition-colors"
    >
      Grade Mastery %
      {sortDirection === "desc" ? (
        <ArrowDown className="h-4 w-4" />
      ) : (
        <ArrowUp className="h-4 w-4" />
      )}
    </button>
  );
}

