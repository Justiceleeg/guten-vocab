"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { StudentListResponse } from "@/lib/types";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { cn } from "@/lib/utils";

export default function StudentsPage() {
  const router = useRouter();
  const [students, setStudents] = useState<StudentListResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.getStudents();
        setStudents(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load students");
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

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

  const handleRowClick = (studentId: number) => {
    router.push(`/students/${studentId}`);
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">Students</h1>
        <div className="text-muted-foreground">Loading students...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">Students</h1>
        <div className="text-red-600 dark:text-red-400 mb-4">
          Error: {error}
        </div>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
        >
          Retry
        </button>
      </div>
    );
  }

  if (students.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-4">Students</h1>
        <div className="text-muted-foreground">
          No students found. Please add students to get started.
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Students</h1>
      <div className="rounded-md border overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Reading Level</TableHead>
              <TableHead>Grade Mastery %</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {students.map((student) => (
              <TableRow
                key={student.id}
                onClick={() => handleRowClick(student.id)}
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
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

