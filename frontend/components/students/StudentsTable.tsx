"use client";

import { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { StudentListResponse } from "@/lib/types";
import { SortableTableHeader } from "./SortableTableHeader";
import { StudentRow } from "./StudentRow";

interface StudentsTableProps {
  students: StudentListResponse[];
}

type SortDirection = "asc" | "desc";

export function StudentsTable({ students }: StudentsTableProps) {
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc");

  const sortedStudents = useMemo(() => {
    const sorted = [...students];
    sorted.sort((a, b) => {
      if (sortDirection === "desc") {
        return b.vocab_mastery_percent - a.vocab_mastery_percent;
      } else {
        return a.vocab_mastery_percent - b.vocab_mastery_percent;
      }
    });
    return sorted;
  }, [students, sortDirection]);

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Reading Level</TableHead>
            <TableHead>
              <SortableTableHeader
                defaultDirection={sortDirection}
                onSortChange={setSortDirection}
              />
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedStudents.map((student) => (
            <StudentRow key={student.id} student={student} />
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

