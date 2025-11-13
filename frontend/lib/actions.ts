"use server";

/**
 * Server action to fetch book details from Open Library API
 * Uses Next.js fetch caching to reduce API calls
 */
export async function getBookDetails(
  title: string,
  author: string | null
): Promise<{
  coverUrl: string | null;
  summary: string | null;
  pageCount: number | null;
}> {
  try {
    // Search for the book
    const searchQuery = author
      ? `${title} ${author}`.trim()
      : title;
    const searchUrl = `https://openlibrary.org/search.json?q=${encodeURIComponent(searchQuery)}&limit=1`;
    
    // Use Next.js fetch with caching - cache for 7 days (book covers don't change often)
    const searchResponse = await fetch(searchUrl, {
      next: { revalidate: 604800 }, // 7 days in seconds
    });
    
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
        // Cache work details for 7 days as well
        const workResponse = await fetch(workUrl, {
          next: { revalidate: 604800 },
        });
        
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
}

