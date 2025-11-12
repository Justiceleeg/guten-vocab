"use client";

import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface VocabularyTableCardProps {
  title: string;
  description: string;
  emptyMessage: string;
  columns: Array<{ header: string; align?: "left" | "right" }>;
  rows: Array<{
    key: string | number;
    cells: Array<{ content: React.ReactNode; className?: string }>;
    onClick?: () => void;
    rowClassName?: string;
  }>;
}

export function VocabularyTableCard({
  title,
  description,
  emptyMessage,
  columns,
  rows,
}: VocabularyTableCardProps) {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <Card>
        <CardContent className="pt-6">
          {rows.length > 0 ? (
            <>
              <p className="text-sm text-muted-foreground mb-4">{description}</p>
              <Table>
                <TableHeader>
                  <TableRow>
                    {columns.map((col, index) => (
                      <TableHead
                        key={index}
                        className={col.align === "right" ? "text-right" : ""}
                      >
                        {col.header}
                      </TableHead>
                    ))}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rows.map((row) => (
                    <TableRow
                      key={row.key}
                      className={row.rowClassName}
                      onClick={row.onClick}
                    >
                      {row.cells.map((cell, cellIndex) => (
                        <TableCell
                          key={cellIndex}
                          className={cell.className}
                        >
                          {cell.content}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          ) : (
            <div className="py-12 text-center">
              <p className="text-muted-foreground">{emptyMessage}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

