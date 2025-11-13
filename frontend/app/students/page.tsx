import { StudentListResponse } from "@/lib/types";
import { StudentsTable } from "@/components/students/StudentsTable";
import { ErrorDisplay } from "@/components/shared/ErrorDisplay";

async function getStudents(): Promise<StudentListResponse[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${apiUrl}/api/students`, {
    next: { revalidate: 300 }, // Cache for 5 minutes
  });

  if (!response.ok) {
    if (response.status === 404) {
      return [];
    }
    throw new Error(`Failed to fetch students: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export default async function StudentsPage() {
  let students: StudentListResponse[] = [];
  let error: string | null = null;

  try {
    students = await getStudents();
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load students";
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Students</h1>
      
      {error ? (
        <ErrorDisplay error={error} />
      ) : students.length === 0 ? (
        <div className="text-muted-foreground">
          No students found. Please add students to get started.
        </div>
      ) : (
        <StudentsTable students={students} />
      )}
    </div>
  );
}
