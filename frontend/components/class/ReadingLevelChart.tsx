"use client";

import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { ReadingLevelDistribution } from "@/lib/types";

interface ReadingLevelChartProps {
  distribution: ReadingLevelDistribution;
}

export function ReadingLevelChart({ distribution }: ReadingLevelChartProps) {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    const checkDarkMode = () => {
      setIsDark(document.documentElement.classList.contains("dark"));
    };
    checkDarkMode();
    const observer = new MutationObserver(checkDarkMode);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, []);

  const chartData = Object.entries(distribution)
    .map(([level, count]) => ({
      level: `Grade ${level}`,
      students: count,
    }))
    .sort((a, b) => {
      const levelA = parseInt(a.level.replace("Grade ", ""));
      const levelB = parseInt(b.level.replace("Grade ", ""));
      return levelA - levelB;
    });

  if (chartData.length === 0) {
    return (
      <p className="text-muted-foreground text-center py-8">
        No reading level data available
      </p>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={chartData}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
          opacity={0.3}
        />
        <XAxis
          dataKey="level"
          tick={{ fill: isDark ? "oklch(0.7982 0.0243 82.1078)" : "oklch(0.5391 0.0387 71.1655)" }}
          stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
        />
        <YAxis
          tick={{ fill: isDark ? "oklch(0.7982 0.0243 82.1078)" : "oklch(0.5391 0.0387 71.1655)" }}
          stroke={isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: isDark ? "oklch(0.3237 0.0155 59.0603)" : "oklch(0.9914 0.0098 87.4695)",
            border: `1px solid ${isDark ? "oklch(0.3795 0.0181 57.128)" : "oklch(0.8606 0.0321 84.5881)"}`,
            borderRadius: "0.5rem",
            color: isDark ? "oklch(0.9239 0.019 83.0636)" : "oklch(0.376 0.0225 64.3434)",
          }}
          labelStyle={{
            color: isDark ? "oklch(0.9239 0.019 83.0636)" : "oklch(0.376 0.0225 64.3434)",
            fontWeight: 600,
          }}
        />
        <Bar
          dataKey="students"
          fill={isDark ? "oklch(0.7264 0.0581 66.6967)" : "oklch(0.618 0.0778 65.5444)"}
          radius={[4, 4, 0, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

