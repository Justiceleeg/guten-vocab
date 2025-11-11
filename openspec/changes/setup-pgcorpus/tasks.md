## 1. pgcorpus/gutenberg Setup

### 1.1 Research pgcorpus Repository
- [x] Review pgcorpus/gutenberg GitHub repository
- [x] Understand repository structure and purpose
- [x] Identify required dependencies
- [x] Understand data download and processing workflow
- [x] Note expected file formats and locations

### 1.2 Document Setup Process
- [x] Create `docs/pgcorpus-setup.md`
- [x] Document cloning repository:
  - [x] Command: `git clone https://github.com/pgcorpus/gutenberg.git`
  - [x] Expected repository structure
- [x] Document dependency installation:
  - [x] Command: `pip install -r requirements.txt`
  - [x] List key dependencies
- [x] Document data download:
  - [x] Command: `python get_data.py`
  - [x] Expected duration (may take hours)
  - [x] Disk space requirements
  - [x] What data is downloaded
- [x] Document data processing:
  - [x] Command: `python process_data.py`
  - [x] What processing does
  - [x] Expected output format
- [x] Document file locations:
  - [x] Location of `counts/` folder
  - [x] Location of metadata CSV
  - [x] File naming conventions
  - [x] Data format examples

### 1.3 Verify Setup (Optional - if user runs it)
- [x] Clone repository (if user wants to test) - Used Zenodo alternative instead
- [x] Install dependencies - Installed in venv
- [x] Run get_data.py (if user wants to download) - Used Zenodo pre-processed dataset instead
- [x] Run process_data.py (if user wants to process) - Used Zenodo pre-processed dataset instead
- [x] Verify counts folder and metadata CSV exist - Verified: 55,906 counts files + metadata.csv
- [x] Document any issues or gotchas encountered - Documented in pgcorpus-alternatives.md and zenodo-setup.md
- [x] Clean up unused data after book selection - Removed 55,805 unneeded counts files, freed 3.31 GB (kept 100 selected books)

**Acceptance Criteria:**
- ✅ Complete setup documentation in `docs/pgcorpus-setup.md`
- ✅ All setup steps clearly documented
- ✅ File locations and formats documented
- ✅ Expected data structure documented
- ✅ Setup process can be followed by another developer

