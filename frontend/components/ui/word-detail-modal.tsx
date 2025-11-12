"use client";

import { useState, useEffect } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { dictionaryApi } from "@/lib/api";
import { WordDefinition } from "@/lib/types";
import { Loader2, BookOpen } from "lucide-react";

interface WordDetailModalProps {
  word: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function WordDetailModal({ word, open, onOpenChange }: WordDetailModalProps) {
  const [loading, setLoading] = useState(false);
  const [wordData, setWordData] = useState<WordDefinition | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (open && word) {
      fetchWordDefinition();
    }
  }, [open, word]);

  const fetchWordDefinition = async () => {
    setLoading(true);
    setError(null);
    setWordData(null);
    try {
      const definition = await dictionaryApi.getWordDefinition(word);
      if (definition) {
        setWordData(definition);
      } else {
        setError("Word definition not found");
      }
    } catch (err) {
      setError("Failed to load word definition");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="text-2xl capitalize">{word}</DialogTitle>
          {wordData?.phonetic && (
            <DialogDescription className="text-base">{wordData.phonetic}</DialogDescription>
          )}
        </DialogHeader>

        <div className="space-y-6 mt-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
            </div>
          ) : error ? (
            <div className="text-center py-8">
              <BookOpen className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <p className="text-muted-foreground">{error}</p>
            </div>
          ) : wordData ? (
            <>
              {/* Meanings */}
              {wordData.meanings && wordData.meanings.length > 0 && (
                <div className="space-y-4">
                  {wordData.meanings.map((meaning, index) => (
                    <div key={index} className="border-b pb-4 last:border-0">
                      <h3 className="text-lg font-semibold mb-3 capitalize italic">
                        {meaning.partOfSpeech}
                      </h3>
                      <div className="space-y-3">
                        {meaning.definitions.map((def, defIndex) => (
                          <div key={defIndex} className="space-y-2">
                            <p className="text-sm leading-relaxed">
                              <span className="font-medium">{defIndex + 1}.</span> {def.definition}
                            </p>
                            {def.example && (
                              <p className="text-sm text-muted-foreground italic pl-4">
                                "{def.example}"
                              </p>
                            )}
                            {def.synonyms && def.synonyms.length > 0 && (
                              <div className="pl-4">
                                <span className="text-xs font-medium text-muted-foreground">
                                  Synonyms:{" "}
                                </span>
                                <span className="text-xs text-muted-foreground">
                                  {def.synonyms.slice(0, 5).join(", ")}
                                  {def.synonyms.length > 5 && "..."}
                                </span>
                              </div>
                            )}
                            {def.antonyms && def.antonyms.length > 0 && (
                              <div className="pl-4">
                                <span className="text-xs font-medium text-muted-foreground">
                                  Antonyms:{" "}
                                </span>
                                <span className="text-xs text-muted-foreground">
                                  {def.antonyms.slice(0, 5).join(", ")}
                                  {def.antonyms.length > 5 && "..."}
                                </span>
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Origin */}
              {wordData.origin && (
                <div className="pt-4 border-t">
                  <h3 className="text-sm font-semibold mb-2">Origin</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    {wordData.origin}
                  </p>
                </div>
              )}
            </>
          ) : null}
        </div>
      </DialogContent>
    </Dialog>
  );
}

