# pgcorpus/gutenberg Setup Guide

This guide documents the setup process for the pgcorpus/gutenberg dataset, which provides pre-computed word counts for Project Gutenberg books. This dataset is essential for extracting vocabulary matches between books and our master vocabulary list without having to process full book texts.

> **⚠️ Size Warning**: The full download is 50-80 GB. If this is too large, see **[pgcorpus-alternatives.md](./pgcorpus-alternatives.md)** for lighter-weight options (including a 21 GB pre-processed dataset).

## Overview

The pgcorpus/gutenberg repository provides:
- Pre-computed word counts for Project Gutenberg books
- Metadata CSV with book information (title, author, category, language, etc.)
- Standardized preprocessing pipeline for consistent data format

**Repository**: https://github.com/pgcorpus/gutenberg

## Prerequisites

- Python 3.x installed
- Git installed
- Sufficient disk space (downloads can be large - see below)
- Stable internet connection (download may take hours)

## Setup Steps

### 1. Clone the Repository

**Recommended Location**: Clone the repository at the **project root** (in the `guten-vocab` directory):

```bash
# From the project root directory
git clone https://github.com/pgcorpus/gutenberg.git
cd gutenberg
```

This creates a `gutenberg/` directory at the project root, which is where the verification script expects it.

**Alternative Locations**: You can clone it anywhere and specify the path when running scripts:
- Outside the project: `/path/to/datasets/gutenberg`
- In a parent directory: `../gutenberg`
- In the project root: `./gutenberg` (recommended)

**Note**: The `gutenberg/` directory is automatically excluded from git (see `.gitignore`) since it contains large datasets that shouldn't be committed.

**Expected Repository Structure:**
```
gutenberg/
├── get_data.py          # Script to download books
├── process_data.py      # Script to process books into counts
├── requirements.txt     # Python dependencies
├── README.md            # Repository documentation
└── ...                  # Other repository files
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies** (typical):
- Python standard library modules
- Data processing libraries (pandas, numpy, etc.)
- Text processing utilities

**Note**: Review `requirements.txt` for the complete list of dependencies.

### 3. Download the Data

```bash
python get_data.py
```

**What This Does:**
- Downloads all available Project Gutenberg books
- Stores books in a hidden `.mirror` folder
- Creates symlinks in the `data/raw` directory for easier access

**Important Notes:**
- ⏱️ **Duration**: This process may take **several hours** depending on your internet connection
- 💾 **Disk Space Requirements**:
  - **Full dataset (all books)**: Approximately **50-80 GB** total
    - Raw books (`.mirror/`): ~30-50 GB
    - Processed counts (`data/counts/`): ~3-5 GB
    - Processed tokens (`data/tokens/`): ~20-30 GB
    - Metadata: <100 MB
  - **For this project**: You only need counts for ~100 books, but the download script fetches all books
  - **Alternative**: Consider using the pre-processed 2018 Zenodo dataset (~21 GB) if you don't need the latest books
- 🌐 **Internet**: Requires stable internet connection for downloading thousands of books
- ⚠️ **Time**: This is a long-running process - do not interrupt it
- 📊 **Scale**: Project Gutenberg has grown from ~55,000 books (2018) to ~75,999+ books (2025)

**Expected Output:**
- `.mirror/` folder containing downloaded book files
- `data/raw/` directory with symlinks to book files

### 4. Process the Data

```bash
python process_data.py
```

**What This Does:**
- Preprocesses downloaded texts:
  - Removes boilerplate content (headers, footers, legal text)
  - Tokenizes text into words
  - Filters and cleans tokens
  - Lowercases tokens
  - Counts word occurrences
- Populates relevant directories within the `data` folder with processed corpus

**Expected Output:**
- `data/counts/` folder containing word count files
- `data/metadata.csv` (or similar) containing book metadata

**Processing Time:**
- Depends on number of books downloaded
- Typically takes less time than downloading, but can still take 30+ minutes

## File Locations and Structure

### Counts Folder

**Location**: `gutenberg/data/counts/`

**File Naming Convention:**
- Files are typically named by Gutenberg ID
- Example: `76.txt` or `gutenberg_76.txt` (format may vary)
- Each file contains word counts for one book

**Data Format** (typical):
```
word1 count1
word2 count2
word3 count3
...
```

Or as JSON:
```json
{
  "word1": count1,
  "word2": count2,
  "word3": count3,
  ...
}
```

**Note**: Exact format may vary - check the repository documentation or inspect a sample file.

### Metadata CSV

**Location**: `gutenberg/data/metadata.csv` (or similar path)

**Expected Columns** (typical):
- `gutenberg_id`: Unique identifier for the book
- `title`: Book title
- `author`: Author name
- `category`: Book category (e.g., "Children's Literature", "Children's Fiction")
- `language`: Language code (e.g., "en" for English)
- `download_count`: Number of downloads (popularity metric)
- Other metadata fields as available

**CSV Format Example:**
```csv
gutenberg_id,title,author,category,language,download_count
76,Adventures of Huckleberry Finn,Mark Twain,Children's Fiction,en,50000
...
```

**Note**: Column names and structure may vary - inspect the actual CSV file to confirm.

## Integration with Guten Vocab

### Workflow Overview

1. **Download & Process**: Download all books and process into counts (one-time setup)
2. **Filter & Select**: Use `seed_books.py` to filter and select 100 children's books
3. **Extract Vocabulary**: Extract vocabulary counts for selected books
4. **Cleanup**: Remove unneeded data (saves ~40-50 GB of disk space)

### Usage in seed_books.py

The pgcorpus dataset is used in the book seeding process:

1. **Metadata Loading**: Load `metadata.csv` to filter books by:
   - Category: "Children's Literature" OR "Children's Fiction"
   - Language: English
   - Availability: Has counts file available

2. **Counts Loading**: For each selected book:
   - Load the corresponding counts file from `data/counts/`
   - Extract vocabulary matches with our master vocabulary list
   - Calculate total word counts

3. **Save Selection**: Selected books are saved to `data/books/selected_books.json`

### Cleanup After Book Selection

After selecting and processing the 100 books, you can clean up unneeded data:

```bash
# First, verify all selected books have counts files (dry run)
python scripts/cleanup_pgcorpus.py gutenberg data/books/selected_books.json --dry-run

# Then actually clean up (removes ~40-50 GB)
python scripts/cleanup_pgcorpus.py gutenberg data/books/selected_books.json
```

**What gets removed:**
- All counts files except the 100 selected books
- Raw book text files (`data/raw/`)
- Tokenized text files (`data/tokens/`)
- Processed text files (`data/text/`)
- Downloaded mirror folder (`data/.mirror/`)

**What gets kept:**
- Selected books' counts files (100 files, ~50-100 MB)
- Metadata CSV (needed for reference)
- Repository scripts (for future updates)

**Space savings**: Typically frees up 40-50 GB while keeping only what you need.

### Expected Paths

When integrating with the Guten Vocab project, you may need to:

1. **Reference the counts folder**:
   ```python
   counts_path = "/path/to/gutenberg/data/counts/{gutenberg_id}.txt"
   ```

2. **Load metadata CSV**:
   ```python
   metadata_path = "/path/to/gutenberg/data/metadata.csv"
   ```

3. **Verify file existence** before processing:
   ```python
   import os
   if os.path.exists(counts_file_path):
       # Process the file
   ```

## Troubleshooting

### Common Issues

1. **Download Fails or Times Out**
   - Check internet connection
   - Ensure sufficient disk space
   - Try running `get_data.py` again (may resume partial downloads)

2. **Processing Errors**
   - Verify all dependencies are installed
   - Check that `get_data.py` completed successfully
   - Review error messages for specific issues

3. **File Not Found Errors**
   - Verify the counts folder exists: `gutenberg/data/counts/`
   - Check metadata CSV location: `gutenberg/data/metadata.csv`
   - Confirm file naming conventions match expectations

4. **Disk Space Issues**
   - Monitor disk usage during download
   - Consider downloading a subset if full dataset is too large
   - Clean up `.mirror` folder if needed (after processing)

### Verification

To verify the setup is complete and working correctly, you can either:

1. **Use the automated verification script** (recommended):
   ```bash
   python scripts/verify_pgcorpus.py [path_to_gutenberg_repo]
   ```
   
   If no path is provided, it assumes `./gutenberg`. This script will check all aspects of the setup and provide a summary.

2. **Manual verification** - Follow the steps below:

#### Step 1: Verify Repository Structure

```bash
cd gutenberg
ls -la
```

**Expected**: Should see `get_data.py`, `process_data.py`, `requirements.txt`, and `data/` directory.

#### Step 2: Verify Dependencies Installed

```bash
pip list | grep -E "(pandas|numpy|requests)"
```

**Expected**: Should show installed packages. If empty, run `pip install -r requirements.txt` again.

#### Step 3: Verify Data Download Completed

```bash
# Check if .mirror folder exists and has content
ls -la .mirror/ | head -10

# Check if data/raw has symlinks
ls -la data/raw/ | head -10
```

**Expected**: Should see downloaded book files in `.mirror/` and symlinks in `data/raw/`.

#### Step 4: Verify Processing Completed

```bash
# Check counts folder exists and has files
ls -la data/counts/ | head -20

# Count number of count files
ls data/counts/ | wc -l
```

**Expected**: Should see multiple count files (typically hundreds or thousands).

#### Step 5: Verify Metadata CSV

```bash
# Check metadata CSV exists
ls -lh data/metadata.csv

# View first few rows
head -5 data/metadata.csv

# Count total books in metadata
wc -l data/metadata.csv
```

**Expected**: 
- CSV file should exist and have reasonable size (not empty)
- First row should be headers (gutenberg_id, title, author, etc.)
- Should have multiple rows of data

#### Step 6: Inspect Counts File Format

```bash
# Pick a sample counts file (adjust filename based on actual naming)
# Common patterns: 76.txt, gutenberg_76.txt, etc.
ls data/counts/ | head -1 | xargs -I {} head -20 data/counts/{}
```

**Expected**: Should see word count data in one of these formats:
- Space-separated: `word count`
- Tab-separated: `word\tcount`
- JSON: `{"word": count, ...}`

#### Step 7: Verify Specific Book Files (Optional)

For books you plan to use (e.g., Gutenberg ID 76), verify the counts file exists:

```bash
# Try different naming patterns
ls data/counts/ | grep -E "^76\.|^gutenberg_76|^76_"
```

**Expected**: Should find a counts file for the book.

#### Step 8: Test Reading Metadata CSV (Python)

Create a quick test script to verify the CSV can be read:

```python
import pandas as pd
import os

# Adjust path as needed
csv_path = "data/metadata.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print(f"✅ Metadata CSV loaded: {len(df)} books")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst book:")
    print(df.iloc[0])
else:
    print("❌ Metadata CSV not found")
```

**Expected**: Should successfully load and display book information.

#### Step 9: Test Reading Counts File (Python)

Test that counts files can be parsed:

```python
import os
import json

# Get first counts file
counts_dir = "data/counts"
files = [f for f in os.listdir(counts_dir) if os.path.isfile(os.path.join(counts_dir, f))]
if files:
    sample_file = os.path.join(counts_dir, files[0])
    print(f"Testing file: {sample_file}")
    
    # Try reading first few lines
    with open(sample_file, 'r') as f:
        lines = [f.readline().strip() for _ in range(5)]
        print("First 5 lines:")
        for line in lines:
            print(f"  {line}")
else:
    print("❌ No counts files found")
```

**Expected**: Should successfully read and display word count data.

#### Complete Verification Checklist

- [ ] Repository cloned successfully
- [ ] Dependencies installed (`pip install -r requirements.txt` completed)
- [ ] Data downloaded (`.mirror/` folder has content)
- [ ] Data processed (`data/counts/` folder exists with files)
- [ ] Metadata CSV exists and is readable
- [ ] Counts files exist and have correct format
- [ ] Can read metadata CSV programmatically
- [ ] Can read counts files programmatically

If all checks pass, the setup is complete and ready to use!

## Additional Resources

- **Repository**: https://github.com/pgcorpus/gutenberg
- **Original Publication**: [MDPI Paper](https://www.mdpi.com/1099-4300/22/1/126)
- **Project Gutenberg**: https://www.gutenberg.org/

## Notes

- The dataset is large and download/processing takes significant time
- Consider running setup overnight or during off-hours
- The pre-computed counts save significant processing time compared to processing books from scratch
- Standardized preprocessing ensures consistent data format across all books

