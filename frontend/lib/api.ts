import axios, { AxiosError, AxiosInstance } from "axios";
import {
  StudentListResponse,
  StudentDetailResponse,
  ClassStatsResponse,
  ClassRecommendationResponse,
} from "./types";

// Create axios instance with base configuration
const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 seconds
});

// Request interceptor for logging (optional, can be removed in production)
apiClient.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed in the future
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle common error cases
    if (error.response) {
      // Server responded with error status
      const status = error.response.status;
      const message =
        (error.response.data as { detail?: string })?.detail ||
        error.message ||
        "An error occurred";

      switch (status) {
        case 400:
          throw new Error(`Bad Request: ${message}`);
        case 401:
          throw new Error(`Unauthorized: ${message}`);
        case 403:
          throw new Error(`Forbidden: ${message}`);
        case 404:
          throw new Error(`Not Found: ${message}`);
        case 500:
          throw new Error(`Server Error: ${message}`);
        default:
          throw new Error(`Error ${status}: ${message}`);
      }
    } else if (error.request) {
      // Request was made but no response received
      throw new Error(
        "Network error: Unable to reach the server. Please check your connection."
      );
    } else {
      // Something else happened
      throw new Error(`Request error: ${error.message}`);
    }
  }
);

// API methods
export const api = {
  // Health check
  health: async () => {
    const response = await apiClient.get("/health");
    return response.data;
  },

  // Student endpoints
  getStudents: async (): Promise<StudentListResponse[]> => {
    try {
      const response = await apiClient.get<StudentListResponse[]>("/api/students");
      return response.data;
    } catch (error) {
      // Error is already handled by the interceptor, but we rethrow for clarity
      throw error;
    }
  },

  getStudentById: async (id: number): Promise<StudentDetailResponse> => {
    try {
      const response = await apiClient.get<StudentDetailResponse>(`/api/students/${id}`);
      return response.data;
    } catch (error) {
      // Error is already handled by the interceptor
      // 404 errors will be thrown as "Not Found: ..." messages
      throw error;
    }
  },

  dismissVocabulary: async (
    studentId: number,
    wordId: number,
    reason: 'addressed' | 'ai_error'
  ): Promise<{ success: boolean; dismissed_at: string }> => {
    try {
      const response = await apiClient.post(
        `/api/students/${studentId}/vocabulary/${wordId}/dismiss`,
        { reason }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Class endpoints
  getClassStats: async (): Promise<ClassStatsResponse> => {
    try {
      const response = await apiClient.get<ClassStatsResponse>("/api/class/stats");
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getClassRecommendations: async (): Promise<ClassRecommendationResponse[]> => {
    try {
      const response = await apiClient.get<ClassRecommendationResponse[]>("/api/class/recommendations");
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// External API clients (Open Library and DictionaryAPI.dev)
// These don't use the apiClient instance since they're external APIs

/**
 * Open Library API client
 * Documentation: https://openlibrary.org/developers/api
 */
export const openLibraryApi = {
  /**
   * Search for a book by title and author, then fetch details
   * Returns book cover URL, summary, and page count
   */
  getBookDetails: async (
    title: string,
    author: string | null
  ): Promise<{
    coverUrl: string | null;
    summary: string | null;
    pageCount: number | null;
  }> => {
    try {
      // Search for the book
      const searchQuery = author
        ? `${title} ${author}`.trim()
        : title;
      const searchUrl = `https://openlibrary.org/search.json?q=${encodeURIComponent(searchQuery)}&limit=1`;
      
      const searchResponse = await fetch(searchUrl);
      
      if (!searchResponse.ok) {
        throw new Error(`Open Library search failed: ${searchResponse.status}`);
      }
      
      const searchData = await searchResponse.json();
      
      if (!searchData.docs || searchData.docs.length === 0) {
        return { coverUrl: null, summary: null, pageCount: null };
      }
      
      const book = searchData.docs[0];
      const coverId = book.cover_i;
      const workKey = book.key || book.works?.[0]?.key;
      
      // Get cover URL
      let coverUrl: string | null = null;
      if (coverId) {
        coverUrl = `https://covers.openlibrary.org/b/id/${coverId}-L.jpg`;
      }
      
      // Get page count
      const pageCount = book.number_of_pages_median || book.number_of_pages || null;
      
      // Get summary/description from work details
      let summary: string | null = null;
      if (workKey) {
        try {
          const workUrl = `https://openlibrary.org${workKey}.json`;
          const workResponse = await fetch(workUrl);
          
          if (workResponse.ok) {
            const workData = await workResponse.json();
            // Try different fields for description
            summary =
              workData.description?.value ||
              workData.description ||
              (typeof workData.description === 'string' ? workData.description : null);
          }
        } catch (err) {
          // Ignore errors fetching work details
        }
      }
      
      return { coverUrl, summary, pageCount };
    } catch (error) {
      // Return null values on error (will show placeholder)
      console.error('Error fetching book details from Open Library:', error);
      return { coverUrl: null, summary: null, pageCount: null };
    }
  },
};

/**
 * DictionaryAPI.dev client
 * Documentation: https://dictionaryapi.dev/
 * Free, no API key required
 */
export const dictionaryApi = {
  /**
   * Get word definition, usage examples, and origin
   */
  getWordDefinition: async (word: string): Promise<{
    word: string;
    phonetic?: string;
    meanings: Array<{
      partOfSpeech: string;
      definitions: Array<{
        definition: string;
        example?: string;
        synonyms?: string[];
        antonyms?: string[];
      }>;
    }>;
    origin?: string;
  } | null> => {
    try {
      const url = `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word.toLowerCase())}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        if (response.status === 404) {
          return null; // Word not found
        }
        throw new Error(`Dictionary API failed: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!data || !Array.isArray(data) || data.length === 0) {
        return null;
      }
      
      const entry = data[0];
      
      return {
        word: entry.word || word,
        phonetic: entry.phonetic || entry.phonetics?.[0]?.text,
        meanings: entry.meanings?.map((meaning: any) => ({
          partOfSpeech: meaning.partOfSpeech,
          definitions: meaning.definitions?.map((def: any) => ({
            definition: def.definition,
            example: def.example,
            synonyms: def.synonyms,
            antonyms: def.antonyms,
          })) || [],
        })) || [],
        origin: entry.origin,
      };
    } catch (error) {
      console.error('Error fetching word definition:', error);
      return null;
    }
  },
};

export default apiClient;

