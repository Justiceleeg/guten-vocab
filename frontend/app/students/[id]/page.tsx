import { notFound } from "next/navigation";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { StudentDetailResponse } from "@/lib/types";
import { StudentBookRecommendations } from "@/components/students/StudentBookRecommendations";
import { MissingWordsSection } from "@/components/students/MissingWordsSection";
import { MisusedWordsSectionWrapper } from "@/components/students/MisusedWordsSectionWrapper";
import { cn } from "@/lib/utils";

async function getStudent(id: number): Promise<StudentDetailResponse | null> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${apiUrl}/api/students/${id}`, {
    next: { revalidate: 600 }, // Cache for 10 minutes
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    throw new Error(`Failed to fetch student: ${response.status} ${response.statusText}`);
  }

  return response.json();
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

export default async function StudentDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const studentId = parseInt(id, 10);

  if (isNaN(studentId)) {
    notFound();
  }

  let student: StudentDetailResponse | null = null;
  let error: string | null = null;

  try {
    student = await getStudent(studentId);
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load student";
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <nav className="mb-4" aria-label="Breadcrumb">
          <ol className="flex items-center space-x-2 text-sm text-muted-foreground">
            <li>
              <Link href="/" className="hover:text-foreground">
                Home
              </Link>
            </li>
            <li>/</li>
            <li>
              <Link href="/students" className="hover:text-foreground">
                Students
              </Link>
            </li>
            <li>/</li>
            <li className="text-foreground">Error</li>
          </ol>
        </nav>
        <div className="text-red-600 dark:text-red-400 mb-4">
          <h1 className="text-2xl font-bold mb-2">Error</h1>
          <p>{error}</p>
        </div>
        <Link
          href="/students"
          className="inline-block px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
        >
          Back to Students
        </Link>
      </div>
    );
  }

  if (!student) {
    notFound();
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Breadcrumbs */}
      <nav className="mb-6" aria-label="Breadcrumb">
        <ol className="flex items-center space-x-2 text-sm text-muted-foreground">
          <li>
            <Link href="/" className="hover:text-foreground">
              Home
            </Link>
          </li>
          <li>/</li>
          <li>
            <Link href="/students" className="hover:text-foreground">
              Students
            </Link>
          </li>
          <li>/</li>
          <li className="text-foreground">{student.name}</li>
        </ol>
      </nav>

      <div className="space-y-6">
        {/* Section 1: Student Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Student Overview</CardTitle>
            <CardDescription>
              Basic information and vocabulary mastery
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h2 className="text-2xl font-bold mb-2">{student.name}</h2>
              <div className="text-muted-foreground space-y-1">
                <p>Reading Level: {student.reading_level.toFixed(1)}</p>
                <p>Assigned Grade: {student.assigned_grade}</p>
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Grade Mastery</span>
                <span className={cn("text-sm font-semibold", getMasteryColor(student.vocab_mastery.mastery_percent))}>
                  {student.vocab_mastery.mastery_percent.toFixed(1)}%
                </span>
              </div>
              <Progress value={student.vocab_mastery.mastery_percent} className="h-3" />
              <p className="text-sm text-muted-foreground">
                {student.vocab_mastery.words_mastered} of {student.vocab_mastery.total_grade_level_words} words mastered
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Section 2: Book Recommendations */}
        <StudentBookRecommendations
          books={student.book_recommendations}
          studentName={student.name}
        />

        {/* Section 3: Vocabulary Progress */}
        <MissingWordsSection
          totalWords={student.vocab_mastery.total_grade_level_words}
          wordsMastered={student.vocab_mastery.words_mastered}
          masteryPercent={student.vocab_mastery.mastery_percent}
          assignedGrade={student.assigned_grade}
          missingWords={student.missing_words}
        />

        {/* Section 4: Vocabulary Issues */}
        <MisusedWordsSectionWrapper
          misusedWords={student.misused_words}
          studentId={student.id}
        />
      </div>
    </div>
  );
}
