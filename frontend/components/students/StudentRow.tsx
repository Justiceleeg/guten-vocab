"use client";

import { useRouter } from "next/navigation";
import { TableRow, TableCell } from "@/components/ui/table";
import { StudentListResponse } from "@/lib/types";
import { cn } from "@/lib/utils";

interface StudentRowProps {
  student: StudentListResponse;
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

const getMasteryBgColor = (percent: number) => {
  if (percent < 50) {
    return "bg-red-50 dark:bg-red-950/20";
  } else if (percent < 75) {
    return "bg-yellow-50 dark:bg-yellow-950/20";
  } else {
    return "bg-green-50 dark:bg-green-950/20";
  }
};

export function StudentRow({ student }: StudentRowProps) {
  const router = useRouter();

  const handleRowClick = () => {
    router.push(`/students/${student.id}`);
  };

  return (
    <TableRow
      onClick={handleRowClick}
      className="cursor-pointer hover:bg-muted/50"
    >
      <TableCell className="font-medium">{student.name}</TableCell>
      <TableCell>{student.reading_level.toFixed(1)}</TableCell>
      <TableCell>
        <div
          className={cn(
            "inline-flex items-center px-2 py-1 rounded-md font-medium",
            getMasteryBgColor(student.vocab_mastery_percent),
            getMasteryColor(student.vocab_mastery_percent)
          )}
        >
          {student.vocab_mastery_percent.toFixed(1)}%
        </div>
      </TableCell>
    </TableRow>
  );
}

