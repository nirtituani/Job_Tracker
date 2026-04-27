# 🚀 Setup Guide for Job Application Tracker

This guide will help you get the Job Tracker running on your machine, whether you're using it yourself or reviewing it as part of an interview process.

## Table of Contents
- [For Developers/Interviewers](#for-developersinterviewers)
- [For End Users](#for-end-users)
- [Creating Standalone Executables](#creating-standalone-executables)
- [Troubleshooting](#troubleshooting)

---

## For Developers/Interviewers

### Quick Start (5 minutes)

1. **Clone the repository**
   ```bash
   git clone https://github.com/nirtituani/Job_Tracker.git
   cd Job_Tracker
   ```

2. **Run the application**
   ```bash
   python3 job_tracker.py
   ```

3. **Test the features**
   - Add a sample job application
   - Try searching and filtering
   - Export to CSV
   - Update and delete records

### What to Look For (Code Review Checklist)

✅ **Code Quality**
- Clean, readable Python code
- Proper class structure and organization
- Good variable naming conventions
- Comments where needed

✅ **Database Design**
- SQLite schema with proper data types
- Auto-incrementing ID system with gap-filling
- ALTER TABLE logic to handle schema updates
- Timestamp tracking for record changes

✅ **Error Handling**
- Database connection management
- User input validation
- Graceful error messages via messagebox

✅ **UI/UX Design**
- Tkinter GUI with ttk widgets for modern look
- Responsive table with scrollbars
- Form validation before submission
- Clear button states and feedback

✅ **Features**
- CRUD operations (Create, Read, Update, Delete)
- Search and filter functionality
- CSV export capability
- Multiple status tracking
- Custom fields (Job Match, Applied Via)

---

## For End Users

### Prerequisites
- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
  - Check your version: `python3 --version`
  - Download Python: https://www.python.org/downloads/

### Installation Steps

#### Option 1: Run from Source (Recommended for Tech Users)

1. **Download the project**
   - Click the green "Code" button on GitHub
   - Select "Download ZIP"
   - Extract the ZIP file to your desired location

2. **Navigate to the folder**
   ```bash
   cd path/to/Job_Tracker
   ```

3. **Run the app**
   ```bash
   python3 job_tracker.py
   ```

#### Option 2: Standalone Executable (Coming Soon)

Pre-built executables for Windows and macOS will be available in the [Releases](https://github.com/nirtituani/Job_Tracker/releases) section.

---

## Creating Standalone Executables

If you want to create a standalone executable that doesn't require Python:

### For macOS

1. **Install PyInstaller**
   ```bash
   # Create virtual environment (recommended)
   python3 -m venv venv
   source venv/bin/activate
   
   # Install PyInstaller
   pip install pyinstaller
   ```

2. **Build the app**
   ```bash
   pyinstaller --onefile --windowed --name="JobTracker" job_tracker.py
   ```

3. **Find your app**
   - Location: `dist/JobTracker`
   - Size: ~50 MB
   - Double-click to run (no Python required)

4. **Package for distribution**
   ```bash
   cd dist
   zip -r JobTracker.zip JobTracker
   ```

5. **Handle macOS security**
   - If macOS blocks the app: Right-click → Open
   - Or run: `xattr -cr JobTracker`

### For Windows

1. **Install PyInstaller**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   venv\Scripts\activate
   
   # Install PyInstaller
   pip install pyinstaller
   ```

2. **Build the executable**
   ```bash
   pyinstaller --onefile --windowed --name="JobTracker" job_tracker.py
   ```

3. **Find your executable**
   - Location: `dist\JobTracker.exe`
   - Size: ~15-20 MB
   - Double-click to run (no Python required)

4. **Package for distribution**
   ```bash
   cd dist
   # Right-click JobTracker.exe → Send to → Compressed folder
   ```

### Cross-Platform Build Notes

**Important**: 
- Build on the target OS (macOS app on Mac, Windows exe on Windows)
- Linux executables can be created the same way
- Each platform requires its own build

**File Size**:
- macOS: ~50 MB (includes Python runtime)
- Windows: ~15-20 MB
- Compressed: ~50% smaller

---

## Troubleshooting

### Common Issues

#### "Python not found" or "Command not found"
**Solution**: Install Python 3.8+ from https://www.python.org/downloads/

#### "Permission denied" on macOS/Linux
**Solution**: 
```bash
chmod +x job_tracker.py
```

#### "Module not found" errors
**Solution**: The app uses only Python standard library - no additional packages needed. Make sure you're using Python 3.8+.

#### Database file location
- The `job_applications.db` file is created in the same folder as `job_tracker.py`
- On Windows: Usually in `C:\Users\YourName\...\Job_Tracker\`
- On macOS: Usually in `/Users/YourName/.../Job_Tracker/`
- You can move this file to backup or transfer your data

#### macOS "App is damaged and can't be opened"
**Solution**:
```bash
xattr -cr /path/to/JobTracker
```

#### Windows SmartScreen warning
**Solution**: Click "More info" → "Run anyway"
- This is normal for unsigned executables
- Your app is safe, it's just not code-signed

---

## Database Backup & Recovery

### Backup Your Data
```bash
# Create a backup before updates
cp job_applications.db job_applications_BACKUP.db
```

### Restore from Backup
```bash
# Restore if something goes wrong
cp job_applications_BACKUP.db job_applications.db
```

### Transfer Data to Another Computer
1. Copy `job_applications.db` to a USB drive or cloud storage
2. Place it in the same folder as `job_tracker.py` on the new computer
3. Run the app - your data will be there!

---

## Additional Tools

### ID Gap Fixer

If you want to renumber all application IDs sequentially (1, 2, 3... with no gaps):

```bash
# ALWAYS backup first!
cp job_applications.db job_applications_BACKUP.db

# Run the fixer
python3 fix_id_gaps.py

# Type 'yes' when prompted
```

**What it does**: Renumbers all IDs to be perfectly sequential
**When to use**: After deleting many records and you want clean numbering
**Safety**: Always creates a backup first

---

## Need Help?

- **Bug reports**: Open an issue on GitHub
- **Feature requests**: Open an issue with the "enhancement" label
- **Questions**: Check existing issues or open a new one

---

## For Interviewers

### Key Points About This Project

**Technical Skills Demonstrated**:
- Python programming (OOP, file I/O, database operations)
- GUI development with Tkinter
- SQLite database design and management
- Data export functionality (CSV)
- Version control with Git
- Documentation and code organization

**Problem Solving**:
- Implemented custom ID gap-filling algorithm
- Handled database schema migrations
- Created intuitive UI/UX for non-technical users
- Built standalone executables for easy distribution

**Project Management**:
- Iterative development based on user feedback
- Created comprehensive documentation
- Planned for cross-platform compatibility
- Considered end-user experience and privacy

**Time Investment**: 
- Core features: ~20-30 hours
- Additional features & refinement: ~10-15 hours
- Documentation & packaging: ~5-10 hours

Thank you for reviewing this project! 🙏
