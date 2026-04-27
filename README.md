# 📋 Job Application Tracker

A powerful desktop application built with Python and Tkinter to help you manage your job search process efficiently. Track applications, monitor interview stages, and analyze your job search strategy all in one place.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## ✨ Features

### Core Functionality
- **📝 Comprehensive Application Tracking** - Store all job application details in one place
- **🔄 12 Status Types** - Track your entire application journey:
  - Pre-Applied → Applied → Online Assessment → Phone Screen
  - First Interview → Second Interview → Third Interview → Final Interview
  - Offer Received → Rejected → Ghosted → Withdrawn
- **⭐ Job Match Rating** - Rate positions 1-5 stars to prioritize opportunities
- **📲 Application Source Tracking** - Know which channels work best:
  - Company Website, LinkedIn, Recruiter, Direct Email, Referral, Headhunter

### Data Management
- **🔍 Smart Search & Filter** - Find applications by company, title, location, or status
- **📊 CSV Export** - Export your data for analysis or backup
- **🔢 Sequential ID System** - Automatic gap-filling ensures clean, sequential record numbers
- **💾 SQLite Database** - Reliable local storage with no external dependencies

### User Experience
- **🎨 Clean, Professional UI** - Intuitive Tkinter interface
- **📱 Detailed Record View** - All information at a glance
- **✏️ Easy Updates** - Click to select, modify, and save changes
- **🗑️ Safe Deletion** - Remove records with confirmation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- No additional packages required (uses Python standard library)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nirtituani/Job_Tracker.git
   cd Job_Tracker
   ```

2. **Run the application**
   ```bash
   python3 job_tracker.py
   ```

That's it! The app will automatically create a `job_applications.db` file in the same directory.

## 📖 How to Use

### Adding a New Application

1. Click the form at the top of the window
2. Fill in the details:
   - **Company Name** & **Job Title** (required)
   - **Location** - City, State, or Remote
   - **Date Applied** - Format: YYYY-MM-DD
   - **Status** - Select from 12 status options
   - **Salary Range** - e.g., "$80,000 - $100,000"
   - **Job Link** - URL to the job posting
   - **Contact Person** & **Email** - Recruiter or hiring manager info
   - **Applied Via** - Track your application source
   - **Job Match** - Rate 1-5 stars based on how well the job fits
   - **Notes** - Any additional information
3. Click **Add Application**

### Updating an Application

1. Click on any row in the table to select it
2. Modify the fields in the form
3. Click **Update Selected**

### Searching & Filtering

- Use the **Search** box to find applications by company, title, or location
- Use the **Status** dropdown to filter by application stage
- Click **Clear Filter** to show all applications

### Exporting Data

1. Click **Export to CSV**
2. Choose a location to save the file
3. Open in Excel, Google Sheets, or any spreadsheet application

## 🛠️ Additional Tools

### ID Gap Fixer (`fix_id_gaps.py`)

If you've deleted records and want to renumber all IDs sequentially:

```bash
python3 fix_id_gaps.py
```

**Warning:** This tool renumbers ALL application IDs. Always backup your database first:
```bash
cp job_applications.db job_applications_BACKUP.db
```

## 📁 Project Structure

```
Job_Tracker/
├── job_tracker.py          # Main application
├── fix_id_gaps.py          # ID renumbering utility
├── README.md               # This file
├── LICENSE                 # MIT License
├── .gitignore              # Git ignore rules
└── job_applications.db     # SQLite database (created on first run)
```

## 💾 Database Schema

The application uses a single SQLite table with the following structure:

| Column          | Type    | Description                          |
|-----------------|---------|--------------------------------------|
| id              | INTEGER | Auto-incrementing primary key        |
| company_name    | TEXT    | Company name (required)              |
| job_title       | TEXT    | Position title (required)            |
| location        | TEXT    | Job location                         |
| date_applied    | TEXT    | Application date (YYYY-MM-DD)        |
| status          | TEXT    | Current application status           |
| salary_range    | TEXT    | Expected salary range                |
| job_link        | TEXT    | URL to job posting                   |
| contact_person  | TEXT    | Recruiter/hiring manager name        |
| contact_email   | TEXT    | Contact email address                |
| applied_via     | TEXT    | Application source/channel           |
| job_match       | INTEGER | Rating 1-5 stars                     |
| notes           | TEXT    | Additional notes                     |
| last_updated    | TEXT    | Auto-updated timestamp               |

## 🎯 Use Cases

### Job Search Strategy Analysis
Track which application sources yield the best results:
- **LinkedIn**: 15 applications → 8 interviews (53% response rate)
- **Referrals**: 5 applications → 4 interviews (80% response rate)
- **Company Website**: 10 applications → 2 interviews (20% response rate)

### Interview Pipeline Management
See exactly where you are in each process:
- 5 applications in "Pre-Applied" stage
- 12 active "Applied" applications
- 3 "Phone Screen" scheduled
- 2 "Second Interview" this week

### Weekly Planning
- Add 10 "Pre-Applied" positions on Monday
- Follow up and move 5 to "Applied" by Friday
- Filter by "Phone Screen" to prepare for upcoming calls

## 🔒 Privacy & Data Security

- All data is stored **locally** on your machine
- No cloud storage or external connections
- Your job search information stays private
- Database file is portable - take it anywhere

## 🤝 Contributing

This is a personal project, but suggestions are welcome! Feel free to:
- Open an issue for bugs or feature requests
- Fork the repo and submit pull requests
- Share your use cases and feedback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nir Tituani**
- GitHub: [@nirtituani](https://github.com/nirtituani)

## 🙏 Acknowledgments

- Built with Python's tkinter for cross-platform compatibility
- Uses SQLite for reliable local data storage
- Designed for job seekers who want full control of their data

---

**⭐ If you find this helpful, please star the repository!**

*Built by a job seeker, for job seekers.* 🚀
