## 1. pgcorpus/gutenberg Setup

### 1.1 Research pgcorpus Repository
- [ ] Review pgcorpus/gutenberg GitHub repository
- [ ] Understand repository structure and purpose
- [ ] Identify required dependencies
- [ ] Understand data download and processing workflow
- [ ] Note expected file formats and locations

### 1.2 Document Setup Process
- [ ] Create `docs/pgcorpus-setup.md`
- [ ] Document cloning repository:
  - [ ] Command: `git clone https://github.com/pgcorpus/gutenberg.git`
  - [ ] Expected repository structure
- [ ] Document dependency installation:
  - [ ] Command: `pip install -r requirements.txt`
  - [ ] List key dependencies
- [ ] Document data download:
  - [ ] Command: `python get_data.py`
  - [ ] Expected duration (may take hours)
  - [ ] Disk space requirements
  - [ ] What data is downloaded
- [ ] Document data processing:
  - [ ] Command: `python process_data.py`
  - [ ] What processing does
  - [ ] Expected output format
- [ ] Document file locations:
  - [ ] Location of `counts/` folder
  - [ ] Location of metadata CSV
  - [ ] File naming conventions
  - [ ] Data format examples

### 1.3 Verify Setup (Optional - if user runs it)
- [ ] Clone repository (if user wants to test)
- [ ] Install dependencies
- [ ] Run get_data.py (if user wants to download)
- [ ] Run process_data.py (if user wants to process)
- [ ] Verify counts folder and metadata CSV exist
- [ ] Document any issues or gotchas encountered

**Acceptance Criteria:**
- ✅ Complete setup documentation in `docs/pgcorpus-setup.md`
- ✅ All setup steps clearly documented
- ✅ File locations and formats documented
- ✅ Expected data structure documented
- ✅ Setup process can be followed by another developer

