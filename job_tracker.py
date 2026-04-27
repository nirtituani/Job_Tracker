#!/usr/bin/env python3
"""
Job Application Tracker - A Python tool to track your job search process
Features:
- Add new job applications
- Update application status (interview stages, rejections, offers)
- View all applications in a table
- Export to Excel
- Filter and search applications
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
from pathlib import Path

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Job Application Tracker")
        self.root.geometry("1200x700")
        
        # Initialize database
        self.db_path = Path(__file__).parent / "job_applications.db"
        self.init_database()
        
        # Create UI
        self.create_widgets()
        self.load_applications()
        
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                location TEXT,
                date_applied TEXT NOT NULL,
                status TEXT DEFAULT 'Applied',
                salary_range TEXT,
                job_link TEXT,
                contact_person TEXT,
                contact_email TEXT,
                job_match INTEGER,
                notes TEXT,
                last_updated TEXT NOT NULL
            )
        ''')
        
        # Add job_match column to existing tables (if they don't have it)
        try:
            cursor.execute('ALTER TABLE applications ADD COLUMN job_match INTEGER')
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_stages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER,
                stage_name TEXT NOT NULL,
                stage_date TEXT,
                notes TEXT,
                FOREIGN KEY (application_id) REFERENCES applications (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def create_widgets(self):
        """Create the main UI components"""
        # Configure button styles
        self.style = ttk.Style()
        self.style.theme_use('default')  # Use default theme for better compatibility
        
        # Top frame - Add/Edit application
        top_frame = tk.LabelFrame(self.root, text="Add/Update Application", padx=10, pady=10)
        top_frame.pack(fill="x", padx=10, pady=5)
        
        # Form fields
        row = 0
        # Company Name
        tk.Label(top_frame, text="Company Name:").grid(row=row, column=0, sticky="w", pady=3)
        self.company_entry = tk.Entry(top_frame, width=30)
        self.company_entry.grid(row=row, column=1, padx=5, pady=3)
        
        # Job Title
        tk.Label(top_frame, text="Job Title:").grid(row=row, column=2, sticky="w", pady=3)
        self.job_title_entry = tk.Entry(top_frame, width=30)
        self.job_title_entry.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        # Location
        tk.Label(top_frame, text="Location:").grid(row=row, column=0, sticky="w", pady=3)
        self.location_entry = tk.Entry(top_frame, width=30)
        self.location_entry.grid(row=row, column=1, padx=5, pady=3)
        
        # Date Applied
        tk.Label(top_frame, text="Date Applied:").grid(row=row, column=2, sticky="w", pady=3)
        self.date_entry = tk.Entry(top_frame, width=30)
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.date_entry.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        # Status
        tk.Label(top_frame, text="Status:").grid(row=row, column=0, sticky="w", pady=3)
        self.status_var = tk.StringVar(value="Applied")
        status_options = ["Applied", "Phone Screen", "First Interview", "Second Interview", 
                         "Third Interview", "Final Interview", "Offer Received", "Rejected", "Ghosted", "Withdrawn"]
        self.status_combo = ttk.Combobox(top_frame, textvariable=self.status_var, values=status_options, width=28)
        self.status_combo.grid(row=row, column=1, padx=5, pady=3)
        
        # Salary Range
        tk.Label(top_frame, text="Salary Range:").grid(row=row, column=2, sticky="w", pady=3)
        self.salary_entry = tk.Entry(top_frame, width=30)
        self.salary_entry.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        # Job Link
        tk.Label(top_frame, text="Job Link:").grid(row=row, column=0, sticky="w", pady=3)
        self.link_entry = tk.Entry(top_frame, width=30)
        self.link_entry.grid(row=row, column=1, padx=5, pady=3)
        
        # Contact Person
        tk.Label(top_frame, text="Contact Person:").grid(row=row, column=2, sticky="w", pady=3)
        self.contact_person_entry = tk.Entry(top_frame, width=30)
        self.contact_person_entry.grid(row=row, column=3, padx=5, pady=3)
        
        row += 1
        # Contact Email
        tk.Label(top_frame, text="Contact Email:").grid(row=row, column=0, sticky="w", pady=3)
        self.contact_email_entry = tk.Entry(top_frame, width=30)
        self.contact_email_entry.grid(row=row, column=1, padx=5, pady=3)
        
        # Job Match (1-5)
        tk.Label(top_frame, text="Job Match (1-5):").grid(row=row, column=2, sticky="w", pady=3)
        self.job_match_var = tk.StringVar(value="")
        job_match_combo = ttk.Combobox(top_frame, textvariable=self.job_match_var, 
                                       values=["", "1", "2", "3", "4", "5"], 
                                       width=5)
        job_match_combo.grid(row=row, column=3, padx=5, pady=3, sticky="w")
        
        row += 1
        # Notes
        tk.Label(top_frame, text="Notes:").grid(row=row, column=0, sticky="nw", pady=3)
        self.notes_text = tk.Text(top_frame, width=70, height=3)
        self.notes_text.grid(row=row, column=1, columnspan=3, padx=5, pady=3)
        
        row += 1
        # Buttons - Using labels that look like buttons for better macOS compatibility
        button_frame = tk.Frame(top_frame, bg='#2b2b2b')
        button_frame.grid(row=row, column=0, columnspan=4, pady=10)
        
        # Create button-like labels with visible text (works better on macOS)
        # Add Application - Green
        add_frame = tk.Frame(button_frame, bg='#4CAF50', relief='raised', bd=3)
        add_frame.pack(side="left", padx=5)
        add_btn = tk.Label(add_frame, text="➕ Add Application", 
                          bg="#4CAF50", fg="white", 
                          font=('Helvetica', 12, 'bold'),
                          padx=10, pady=8, cursor="hand2")
        add_btn.pack()
        add_btn.bind('<Button-1>', lambda e: self.add_application())
        
        # Update Selected - Blue
        update_frame = tk.Frame(button_frame, bg='#2196F3', relief='raised', bd=3)
        update_frame.pack(side="left", padx=5)
        update_btn = tk.Label(update_frame, text="✏️ Update Selected",
                             bg="#2196F3", fg="white",
                             font=('Helvetica', 12, 'bold'),
                             padx=10, pady=8, cursor="hand2")
        update_btn.pack()
        update_btn.bind('<Button-1>', lambda e: self.update_application())
        
        # Delete Selected - Red
        delete_frame = tk.Frame(button_frame, bg='#f44336', relief='raised', bd=3)
        delete_frame.pack(side="left", padx=5)
        delete_btn = tk.Label(delete_frame, text="🗑️ Delete Selected",
                             bg="#f44336", fg="white",
                             font=('Helvetica', 12, 'bold'),
                             padx=10, pady=8, cursor="hand2")
        delete_btn.pack()
        delete_btn.bind('<Button-1>', lambda e: self.delete_application())
        
        # Clear Form - Gray
        clear_frame = tk.Frame(button_frame, bg='#757575', relief='raised', bd=3)
        clear_frame.pack(side="left", padx=5)
        clear_btn = tk.Label(clear_frame, text="🔄 Clear Form",
                            bg="#757575", fg="white",
                            font=('Helvetica', 12, 'bold'),
                            padx=10, pady=8, cursor="hand2")
        clear_btn.pack()
        clear_btn.bind('<Button-1>', lambda e: self.clear_form())
        
        # Middle frame - Search/Filter
        filter_frame = tk.Frame(self.root, padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10)
        
        tk.Label(filter_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = tk.Entry(filter_frame, width=40)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_applications())
        
        tk.Label(filter_frame, text="Filter by Status:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                    values=["All", "Applied", "Phone Screen", "First Interview", 
                                           "Second Interview", "Third Interview", "Final Interview",
                                           "Offer Received", "Rejected", "Ghosted", "Withdrawn"], 
                                    width=15)
        filter_combo.pack(side="left", padx=5)
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.load_applications())
        
        # Export button as label for better visibility
        export_frame = tk.Frame(filter_frame, bg='#FF9800', relief='raised', bd=3)
        export_frame.pack(side="right", padx=5)
        export_btn = tk.Label(export_frame, text="💾 Export to CSV",
                             bg="#FF9800", fg="white",
                             font=('Helvetica', 11, 'bold'),
                             padx=10, pady=5, cursor="hand2")
        export_btn.pack()
        export_btn.bind('<Button-1>', lambda e: self.export_to_csv())
        
        # Bottom frame - Applications table
        table_frame = tk.LabelFrame(self.root, text="Applications", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(table_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        # Treeview
        columns = ("ID", "Company", "Job Title", "Location", "Date Applied", 
                  "Status", "Salary", "Match", "Last Updated")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                yscrollcommand=tree_scroll_y.set,
                                xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Company", text="Company")
        self.tree.heading("Job Title", text="Job Title")
        self.tree.heading("Location", text="Location")
        self.tree.heading("Date Applied", text="Date Applied")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Salary", text="Salary Range")
        self.tree.heading("Match", text="Match")
        self.tree.heading("Last Updated", text="Last Updated")
        
        # Column widths
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Company", width=150)
        self.tree.column("Job Title", width=200)
        self.tree.column("Location", width=120)
        self.tree.column("Date Applied", width=100, anchor="center")
        self.tree.column("Status", width=120, anchor="center")
        self.tree.column("Salary", width=100)
        self.tree.column("Match", width=60, anchor="center")
        self.tree.column("Last Updated", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Bind selection event
        self.tree.bind('<ButtonRelease-1>', self.on_select)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
        
    def add_application(self):
        """Add a new application to the database"""
        # Validate required fields
        if not self.company_entry.get() or not self.job_title_entry.get():
            messagebox.showerror("Error", "Company Name and Job Title are required!")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Get job_match value (convert to int or None)
        job_match_val = self.job_match_var.get()
        job_match = int(job_match_val) if job_match_val and job_match_val.isdigit() else None
        
        cursor.execute('''
            INSERT INTO applications 
            (company_name, job_title, location, date_applied, status, salary_range,
             job_link, contact_person, contact_email, job_match, notes, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.company_entry.get(),
            self.job_title_entry.get(),
            self.location_entry.get(),
            self.date_entry.get(),
            self.status_var.get(),
            self.salary_entry.get(),
            self.link_entry.get(),
            self.contact_person_entry.get(),
            self.contact_email_entry.get(),
            job_match,
            self.notes_text.get("1.0", "end-1c"),
            now
        ))
        
        conn.commit()
        conn.close()
        
        self.status_bar.config(text=f"Application added successfully at {now}")
        self.clear_form()
        self.load_applications()
        
    def update_application(self):
        """Update the selected application"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an application to update!")
            return
        
        app_id = self.tree.item(selected[0])['values'][0]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Get job_match value (convert to int or None)
        job_match_val = self.job_match_var.get()
        job_match = int(job_match_val) if job_match_val and job_match_val.isdigit() else None
        
        cursor.execute('''
            UPDATE applications
            SET company_name=?, job_title=?, location=?, date_applied=?, status=?,
                salary_range=?, job_link=?, contact_person=?, contact_email=?, 
                job_match=?, notes=?, last_updated=?
            WHERE id=?
        ''', (
            self.company_entry.get(),
            self.job_title_entry.get(),
            self.location_entry.get(),
            self.date_entry.get(),
            self.status_var.get(),
            self.salary_entry.get(),
            self.link_entry.get(),
            self.contact_person_entry.get(),
            self.contact_email_entry.get(),
            job_match,
            self.notes_text.get("1.0", "end-1c"),
            now,
            app_id
        ))
        
        conn.commit()
        conn.close()
        
        self.status_bar.config(text=f"Application updated successfully at {now}")
        self.clear_form()
        self.load_applications()
        
    def delete_application(self):
        """Delete the selected application"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an application to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            app_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM applications WHERE id=?', (app_id,))
            cursor.execute('DELETE FROM interview_stages WHERE application_id=?', (app_id,))
            
            conn.commit()
            conn.close()
            
            self.status_bar.config(text="Application deleted successfully")
            self.clear_form()
            self.load_applications()
    
    def load_applications(self):
        """Load applications from database and display in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build query with filters
        query = 'SELECT id, company_name, job_title, location, date_applied, status, salary_range, job_match, last_updated FROM applications WHERE 1=1'
        params = []
        
        # Search filter
        search_term = self.search_entry.get()
        if search_term:
            query += ' AND (company_name LIKE ? OR job_title LIKE ? OR location LIKE ?)'
            params.extend([f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'])
        
        # Status filter
        status_filter = self.filter_var.get()
        if status_filter != "All":
            query += ' AND status = ?'
            params.append(status_filter)
        
        query += ' ORDER BY id DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Insert into treeview
        for row in rows:
            # Color code by status
            tags = ()
            if row[5] == "Offer Received":
                tags = ('offer',)
            elif row[5] == "Rejected":
                tags = ('rejected',)
            elif "Interview" in row[5]:
                tags = ('interview',)
            
            # Display job_match or empty string
            display_row = list(row)
            if display_row[7] is None:
                display_row[7] = ''
            
            self.tree.insert('', 'end', values=display_row, tags=tags)
        
        # Configure tag colors
        self.tree.tag_configure('offer', background='#C8E6C9')
        self.tree.tag_configure('rejected', background='#FFCDD2')
        self.tree.tag_configure('interview', background='#BBDEFB')
        
        conn.close()
        
        # Update status bar
        self.status_bar.config(text=f"Showing {len(rows)} application(s)")
    
    def on_select(self, event):
        """Handle treeview selection"""
        selected = self.tree.selection()
        if selected:
            app_id = self.tree.item(selected[0])['values'][0]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM applications WHERE id=?', (app_id,))
            row = cursor.fetchone()
            
            if row:
                self.company_entry.delete(0, 'end')
                self.company_entry.insert(0, row[1])
                
                self.job_title_entry.delete(0, 'end')
                self.job_title_entry.insert(0, row[2])
                
                self.location_entry.delete(0, 'end')
                self.location_entry.insert(0, row[3] or '')
                
                self.date_entry.delete(0, 'end')
                self.date_entry.insert(0, row[4])
                
                self.status_var.set(row[5])
                
                self.salary_entry.delete(0, 'end')
                self.salary_entry.insert(0, row[6] or '')
                
                self.link_entry.delete(0, 'end')
                self.link_entry.insert(0, row[7] or '')
                
                self.contact_person_entry.delete(0, 'end')
                self.contact_person_entry.insert(0, row[8] or '')
                
                self.contact_email_entry.delete(0, 'end')
                self.contact_email_entry.insert(0, row[9] or '')
                
                self.notes_text.delete("1.0", "end")
                self.notes_text.insert("1.0", row[10] or '')
                
                # Job Match (at position 12 due to ALTER TABLE adding it at the end)
                job_match_value = str(row[12]) if len(row) > 12 and row[12] is not None else ''
                self.job_match_var.set(job_match_value)
            
            conn.close()
    
    def clear_form(self):
        """Clear all form fields"""
        self.company_entry.delete(0, 'end')
        self.job_title_entry.delete(0, 'end')
        self.location_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.status_var.set("Applied")
        self.salary_entry.delete(0, 'end')
        self.link_entry.delete(0, 'end')
        self.contact_person_entry.delete(0, 'end')
        self.contact_email_entry.delete(0, 'end')
        self.job_match_var.set('')
        self.notes_text.delete("1.0", "end")
        
        # Clear selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
    
    def export_to_csv(self):
        """Export all applications to CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"job_applications_{datetime.now().strftime('%d%m%Y')}.csv"
        )
        
        if not file_path:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT company_name, job_title, location, date_applied, status, 
                   salary_range, job_link, contact_person, contact_email, job_match, notes, last_updated
            FROM applications
            ORDER BY id DESC
        ''')
        
        rows = cursor.fetchall()
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Company Name', 'Job Title', 'Location', 'Date Applied', 'Status',
                           'Salary Range', 'Job Link', 'Contact Person', 'Contact Email', 'Job Match', 'Notes', 'Last Updated'])
            writer.writerows(rows)
        
        conn.close()
        
        messagebox.showinfo("Success", f"Exported {len(rows)} application(s) to:\n{file_path}")
        self.status_bar.config(text=f"Exported to {file_path}")

def main():
    root = tk.Tk()
    app = JobTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
