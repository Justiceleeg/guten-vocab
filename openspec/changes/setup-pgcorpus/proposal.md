# Change: Setup pgcorpus/gutenberg Dataset

## Why
Research and document the setup process for pgcorpus/gutenberg, which provides pre-computed word counts for Project Gutenberg books. This dataset is essential for extracting vocabulary matches between books and our master vocabulary list without having to process full book texts.

## What Changes
- Research and document pgcorpus/gutenberg setup process:
  - Clone repository: `git clone https://github.com/pgcorpus/gutenberg.git`
  - Install dependencies: `pip install -r requirements.txt`
  - Run `python get_data.py` (downloads books - may take hours)
  - Run `python process_data.py` (processes books into counts)
  - Document location of `counts/` folder and metadata CSV
- Create setup documentation in `docs/pgcorpus-setup.md`
- Document expected file structure and data format

## Impact
- Affected specs: None (external dataset setup)
- Affected code: Documentation only, no code changes

