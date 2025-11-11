# pgcorpus Alternatives - Lighter Weight Options

Since the full pgcorpus download is 50-80 GB, here are lighter alternatives that still work for this project.

## What We Actually Need

For the Guten Vocab project, we only need:
1. **Metadata CSV** - To filter and select ~100 children's books
2. **Counts files** - For those ~100 selected books only (not all 75,999+ books)

## Alternative Approaches

### Option 1: Use 2018 Zenodo Dataset (Recommended) ⭐

**Size**: ~21 GB (much smaller than full download)

**Pros:**
- Pre-processed and ready to use
- Contains counts files for ~55,000 books (2018 snapshot)
- Includes metadata CSV
- No processing needed

**Cons:**
- Books from 2018 only (missing newer books)
- Still larger than needed, but manageable

**Steps:**
1. Download from Zenodo: https://zenodo.org/records/2422561
2. Extract the dataset
3. Use the `counts/` folder and metadata CSV
4. Filter for children's books (should have plenty from 2018)

**For this project**: This is probably sufficient since children's literature classics don't change much.

---

### Option 2: Download Metadata Only, Then Individual Books

**Size**: ~100 MB (metadata) + ~50-100 MB (100 books) = **~200 MB total**

**Pros:**
- Minimal download size
- Get latest books
- Only download what you need

**Cons:**
- Need to process books yourself (generate counts)
- More complex setup
- Requires implementing word counting logic

**Steps:**
1. Download just the metadata CSV (can be extracted from pgcorpus or found separately)
2. Filter for children's books using metadata
3. Download individual books from Project Gutenberg (via API or direct download)
4. Process each book to generate word counts
5. Match vocabulary words

**Implementation:**
- Use `gutenbergr` R package or Python `gutenbergpy` library
- Or download directly from Project Gutenberg website
- Process with spaCy to generate counts

---

### Option 3: Use Pre-Processed Hugging Face Dataset

**Size**: ~34 GB (but can query/stream specific books)

**Pros:**
- Well-maintained dataset
- Can access specific books without full download
- Includes metadata

**Cons:**
- Still large if downloading full dataset
- May need to process counts yourself
- Different format than pgcorpus

**Access**: https://huggingface.co/datasets/Navanjana/Gutenberg_books

---

### Option 4: Manual Book Selection + Processing

**Size**: ~50-100 MB (just the 100 books you need)

**Pros:**
- Smallest possible download
- Full control over selection
- Can use latest books

**Cons:**
- Need to manually curate book list
- Need to implement full processing pipeline
- More work upfront

**Steps:**
1. Manually select 100 children's books (use Project Gutenberg website)
2. Download books individually
3. Process each book:
   - Clean text
   - Tokenize and count words
   - Match to vocabulary list
4. Store results in database

---

## Recommendation for This Project

### Best Option: **2018 Zenodo Dataset** (Option 1)

**Why:**
- ✅ 21 GB is manageable (vs 50-80 GB)
- ✅ Pre-processed counts ready to use
- ✅ Includes metadata for filtering
- ✅ Children's literature classics are all there
- ✅ No processing needed
- ✅ Well-documented and tested

**Trade-off:**
- Missing books added after 2018 (probably not critical for children's classics)

### If You Want Latest Books: **Option 2** (Metadata + Individual Downloads)

**Why:**
- ✅ Smallest download (~200 MB)
- ✅ Get latest books
- ✅ Only download what you need

**Trade-off:**
- Need to implement word counting yourself
- More complex setup

---

## Implementation Notes

### If Using Zenodo Dataset (Option 1):

1. Download from: https://zenodo.org/records/2422561
2. Extract to a location (e.g., `~/datasets/pgcorpus-2018/`)
3. Update `seed_books.py` to point to:
   - Metadata: `~/datasets/pgcorpus-2018/metadata.csv`
   - Counts: `~/datasets/pgcorpus-2018/counts/`

### If Using Individual Downloads (Option 2):

You'll need to:
1. Get metadata CSV (can extract from pgcorpus repo or find online)
2. Implement book download logic
3. Implement word counting logic (similar to `process_data.py` but simpler)
4. Match vocabulary words

---

## Size Comparison

| Option | Total Size | What You Get |
|--------|-----------|--------------|
| Full pgcorpus | 50-80 GB | All 75,999+ books, latest |
| Zenodo 2018 | 21 GB | 55,000 books from 2018 |
| Individual Downloads | ~200 MB | Just 100 books you need |
| Hugging Face | 34 GB | All books, queryable |

---

## Next Steps

1. **Decide which approach** based on your needs
2. **If Zenodo**: Download and extract, update paths in scripts
3. **If Individual**: Implement download and processing logic
4. **Update `seed_books.py`** to work with chosen approach

For an MVP/demo, the **Zenodo 2018 dataset (21 GB)** is probably the best balance of size vs. completeness.

