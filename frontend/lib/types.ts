// API Response Types

export interface HealthResponse {
  status: string;
}

export interface ApiError {
  detail?: string;
  message?: string;
}

// Student Types - matching backend Pydantic schemas
export interface VocabMasteryResponse {
  total_grade_level_words: number;
  words_mastered: number;
  mastery_percent: number;
}

export interface MisusedWordResponse {
  word_id: number;
  word: string;
  correct_count: number;
  incorrect_count: number;
  example: string | null;
}

export interface BookRecommendationResponse {
  book_id: number;
  title: string;
  author: string | null;
  reading_level: number | null;
  match_score: number;
  known_words_percent: number;
  new_words_count: number;
}

export interface StudentListResponse {
  id: number;
  name: string;
  reading_level: number;
  assigned_grade: number;
  vocab_mastery_percent: number;
}

export interface StudentDetailResponse {
  id: number;
  name: string;
  reading_level: number;
  assigned_grade: number;
  vocab_mastery: VocabMasteryResponse;
  missing_words: string[];
  misused_words: MisusedWordResponse[];
  book_recommendations: BookRecommendationResponse[];
}

// Class-wide types
export interface TopMissingWordResponse {
  word: string;
  students_missing: number;
}

export interface CommonlyMisusedWordResponse {
  word: string;
  misuse_count: number;
  students_affected?: number;
}

export interface ClassRecommendationResponse {
  book_id: number;
  title: string;
  author: string | null;
  reading_level: number | null;
  students_recommended_count: number;
  avg_match_score: number;
}

export interface ReadingLevelDistribution {
  [key: string]: number; // e.g., "5": 3, "6": 5, "7": 8, "8": 4
}

export interface ClassStatsResponse {
  total_students: number;
  avg_vocab_mastery_percent: number;
  reading_level_distribution: ReadingLevelDistribution;
  top_missing_words: TopMissingWordResponse[];
  commonly_misused_words: CommonlyMisusedWordResponse[];
}

// Legacy types (kept for backward compatibility if needed)
export interface Student {
  id: number;
  name: string;
}

// Vocabulary Types (to be expanded as API is developed)
export interface VocabularyWord {
  id: number;
  word: string;
  definition?: string;
  // Add more fields as needed
}

// Book Types (to be expanded as API is developed)
export interface Book {
  id: number;
  title: string;
  author?: string;
  // Add more fields as needed
}

// Book Detail Types (from Open Library API)
export interface BookDetail {
  coverUrl: string | null;
  summary: string | null;
  pageCount: number | null;
  title: string;
  author: string | null;
}

// Word Detail Types (from DictionaryAPI.dev)
export interface WordDefinition {
  word: string;
  phonetic?: string;
  meanings: WordMeaning[];
  origin?: string;
}

export interface WordMeaning {
  partOfSpeech: string;
  definitions: {
    definition: string;
    example?: string;
    synonyms?: string[];
    antonyms?: string[];
  }[];
}

