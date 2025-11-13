import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { ClassStatsResponse, ClassRecommendationResponse } from "@/lib/types";
import { ClassBookRecommendations } from "@/components/class/ClassBookRecommendations";
import { ClassVocabularyTables } from "@/components/class/ClassVocabularyTables";
import { ReadingLevelChart } from "@/components/class/ReadingLevelChart";
import { ErrorAlert } from "@/components/shared/ErrorAlert";
import { TrendingUp, Users } from "lucide-react";

async function getClassStats(): Promise<ClassStatsResponse> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${apiUrl}/api/class/stats`, {
    next: { revalidate: 300 }, // Cache for 5 minutes
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch class stats: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

async function getClassRecommendations(): Promise<ClassRecommendationResponse[]> {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
  const response = await fetch(`${apiUrl}/api/class/recommendations`, {
    next: { revalidate: 900 }, // Cache for 15 minutes
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch class recommendations: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return data.slice(0, 2); // Take only top 2
}

export default async function ClassOverviewPage() {
  let classStats: ClassStatsResponse | null = null;
  let classRecommendations: ClassRecommendationResponse[] = [];
  let errorStats: string | null = null;
  let errorRecommendations: string | null = null;

  try {
    classStats = await getClassStats();
  } catch (err) {
    errorStats = err instanceof Error ? err.message : "Failed to load class statistics";
  }

  try {
    classRecommendations = await getClassRecommendations();
  } catch (err) {
    errorRecommendations = err instanceof Error ? err.message : "Failed to load class recommendations";
  }

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Class Overview</h1>
        <p className="text-muted-foreground">
          View class-wide statistics, book recommendations, and vocabulary insights
        </p>
      </div>

      {/* Section 1: Class Statistics */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Class Statistics</h2>
        {errorStats ? (
          <ErrorAlert error={errorStats} />
        ) : classStats ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Total Students Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Total Students
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold">{classStats.total_students}</div>
                <p className="text-muted-foreground mt-2">students in the class</p>
              </CardContent>
            </Card>

            {/* Average Vocabulary Mastery Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Average Vocabulary Mastery
                </CardTitle>
                <CardDescription>Across all students</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-4xl font-bold mb-4">
                  {classStats.avg_vocab_mastery_percent.toFixed(1)}%
                </div>
                <Progress value={classStats.avg_vocab_mastery_percent} className="h-3" />
                <p className="text-sm text-muted-foreground mt-2">
                  Words mastered correctly in context
                </p>
              </CardContent>
            </Card>

            {/* Reading Level Distribution Chart */}
            <Card className="md:col-span-2">
              <CardHeader>
                <CardTitle>Reading Level Distribution</CardTitle>
                <CardDescription>Number of students at each grade level</CardDescription>
              </CardHeader>
              <CardContent>
                <ReadingLevelChart distribution={classStats.reading_level_distribution} />
              </CardContent>
            </Card>
          </div>
        ) : null}
      </section>

      {/* Section 2: Class-Wide Book Recommendations */}
      <section>
        <h2 className="text-2xl font-semibold mb-4">Recommended Books for the Class</h2>
        {errorRecommendations ? (
          <ErrorAlert error={errorRecommendations} />
        ) : (
          <ClassBookRecommendations
            recommendations={classRecommendations}
            totalStudents={classStats?.total_students}
          />
        )}
      </section>

      {/* Sections 3 & 4: Vocabulary Gaps and Common Mistakes */}
      {classStats && (
        <section>
          <ClassVocabularyTables classStats={classStats} />
        </section>
      )}
    </div>
  );
}
