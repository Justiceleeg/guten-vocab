# Zenodo 2018 Dataset Setup (Alternative to Full Download)

Since the full pgcorpus download stalled, we'll use the pre-processed 2018 Zenodo dataset instead.

## Why This Works

- ✅ **Pre-processed**: Counts files already generated
- ✅ **Smaller**: 21 GB vs 50-80 GB
- ✅ **Faster**: Download only, no processing needed
- ✅ **Sufficient**: Has all the children's classics we need

## Download Steps

### 1. Download the Dataset

Go to: https://zenodo.org/records/2422561

**Files to download:**
- `SPGC-counts-2018-07-18.zip` (~1.5 GB) - **This is what we need!**
- `SPGC-tokens-2018-07-18.zip` (~6.4 GB) - Optional, not needed
- `SPGC-metadata-2018-07-18.zip` - Metadata CSV

**Minimum needed**: Just the counts file (~1.5 GB)

### 2. Extract the Dataset

```bash
# Extract to project directory (recommended)
cd /Users/justicepwhite/code/gauntletai-code/guten-vocab
mkdir -p data/pgcorpus-2018
cd data/pgcorpus-2018

# Extract the counts file
unzip ~/Downloads/SPGC-counts-2018-07-18.zip

# Extract metadata if you downloaded it
unzip ~/Downloads/SPGC-metadata-2018-07-18.zip
```

**Note**: The dataset will be in `data/pgcorpus-2018/` (already in `.gitignore`).

### 3. Verify Structure

After extraction, you should have:
```
data/pgcorpus-2018/
├── counts/          # Word count files (one per book)
└── metadata.csv     # Book metadata (if you downloaded it)
```

### 4. Verify Setup

Run the setup script to verify everything is correct:

```bash
# From project root
python3 scripts/setup_zenodo.py data/pgcorpus-2018

# Or just run without args (auto-detects if in default location)
python3 scripts/setup_zenodo.py
```

This will:
- Verify the dataset structure
- Check that counts files are accessible
- Create symlinks or update paths as needed

## Size Comparison

| Dataset | Size | Processing Time |
|---------|------|----------------|
| Full pgcorpus | 50-80 GB | ~1-2 hours download + 30-60 min processing |
| Zenodo 2018 | 21 GB (or just 1.5 GB for counts) | ~6 minutes download, no processing |

## Notes

- The 2018 dataset has ~55,000 books (vs 75,000+ in full)
- All children's classics are included
- Missing books added after 2018 (not critical for our use case)

