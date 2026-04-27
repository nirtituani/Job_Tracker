#!/usr/bin/env python3
"""
Fix ID Gaps - Reorganize all job application IDs to be sequential (1, 2, 3, ...)
This script removes all gaps in your ID sequence.
"""

import sqlite3
from pathlib import Path

def fix_id_gaps(db_path):
    """
    Reorganize all IDs to be sequential starting from 1
    """
    print("🔧 Starting ID Gap Fix...")
    print(f"📂 Database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all applications sorted by current ID
    cursor.execute('SELECT * FROM applications ORDER BY id ASC')
    all_apps = cursor.fetchall()
    
    if not all_apps:
        print("❌ No applications found in database!")
        conn.close()
        return
    
    print(f"\n📊 Found {len(all_apps)} applications")
    print(f"   Current ID range: {all_apps[0][0]} to {all_apps[-1][0]}")
    
    # Show current IDs
    current_ids = [app[0] for app in all_apps]
    print(f"   Current IDs: {current_ids}")
    
    # Calculate gaps
    expected_ids = list(range(1, len(all_apps) + 1))
    gaps = [i for i in range(1, all_apps[-1][0] + 1) if i not in current_ids]
    
    if not gaps:
        print("\n✅ No gaps found! IDs are already sequential.")
        conn.close()
        return
    
    print(f"   Gaps found at: {gaps}")
    print(f"   Target ID range: 1 to {len(all_apps)}")
    
    # Ask for confirmation
    print("\n⚠️  This will renumber ALL applications to be sequential!")
    print("   Example:")
    print(f"      Old IDs: {current_ids[:5]}... → New IDs: [1, 2, 3, 4, 5]...")
    
    response = input("\n   Continue? (yes/no): ").lower().strip()
    
    if response != 'yes':
        print("❌ Cancelled. No changes made.")
        conn.close()
        return
    
    print("\n🔄 Renumbering applications...")
    
    # Create temporary table with new IDs
    cursor.execute('''
        CREATE TABLE applications_temp AS 
        SELECT * FROM applications ORDER BY id ASC
    ''')
    
    # Drop the original table
    cursor.execute('DROP TABLE applications')
    
    # Recreate applications table (without AUTOINCREMENT to allow manual IDs)
    cursor.execute('''
        CREATE TABLE applications (
            id INTEGER PRIMARY KEY,
            company_name TEXT NOT NULL,
            job_title TEXT NOT NULL,
            location TEXT,
            date_applied TEXT NOT NULL,
            status TEXT DEFAULT 'Pre-Applied',
            salary_range TEXT,
            job_link TEXT,
            contact_person TEXT,
            contact_email TEXT,
            notes TEXT,
            last_updated TEXT NOT NULL,
            job_match INTEGER
        )
    ''')
    
    # Get column info from temp table
    cursor.execute('PRAGMA table_info(applications_temp)')
    columns = cursor.fetchall()
    
    # Insert data with new sequential IDs
    cursor.execute('SELECT * FROM applications_temp ORDER BY id ASC')
    old_apps = cursor.fetchall()
    
    new_id = 1
    old_to_new_id_map = {}
    
    for old_app in old_apps:
        old_id = old_app[0]
        old_to_new_id_map[old_id] = new_id
        
        # Insert with new ID
        cursor.execute('''
            INSERT INTO applications 
            (id, company_name, job_title, location, date_applied, status, salary_range,
             job_link, contact_person, contact_email, notes, last_updated, job_match)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            new_id,           # New sequential ID
            old_app[1],       # company_name
            old_app[2],       # job_title
            old_app[3],       # location
            old_app[4],       # date_applied
            old_app[5],       # status
            old_app[6],       # salary_range
            old_app[7],       # job_link
            old_app[8],       # contact_person
            old_app[9],       # contact_email
            old_app[10],      # notes
            old_app[11],      # last_updated
            old_app[12] if len(old_app) > 12 else None  # job_match
        ))
        
        print(f"   ✓ Renumbered: #{old_id} → #{new_id} ({old_app[1]} - {old_app[2]})")
        new_id += 1
    
    # Drop temporary table
    cursor.execute('DROP TABLE applications_temp')
    
    # Update interview_stages table if it exists
    try:
        cursor.execute('SELECT COUNT(*) FROM interview_stages')
        interview_count = cursor.fetchone()[0]
        
        if interview_count > 0:
            print(f"\n🔄 Updating {interview_count} interview stage references...")
            
            for old_id, new_id in old_to_new_id_map.items():
                cursor.execute('''
                    UPDATE interview_stages 
                    SET application_id = ? 
                    WHERE application_id = ?
                ''', (new_id, old_id))
            
            print("   ✓ Interview stages updated")
    except sqlite3.OperationalError:
        pass  # Table doesn't exist
    
    conn.commit()
    
    # Verify results
    cursor.execute('SELECT id FROM applications ORDER BY id')
    new_ids = [row[0] for row in cursor.fetchall()]
    
    print(f"\n✅ ID Gap Fix Complete!")
    print(f"   Total applications: {len(new_ids)}")
    print(f"   New ID range: {new_ids[0]} to {new_ids[-1]}")
    print(f"   New IDs: {new_ids}")
    print(f"\n   All IDs are now sequential with NO gaps! 🎉")
    
    conn.close()

if __name__ == "__main__":
    # Try to find the database
    possible_paths = [
        Path.home() / "Downloads" / "job_tracker_new" / "job_applications.db",
        Path.home() / "job_tracker_new" / "job_applications.db",
        Path(__file__).parent / "job_applications.db",
    ]
    
    db_path = None
    for path in possible_paths:
        if path.exists():
            db_path = path
            break
    
    if not db_path:
        print("❌ Error: Could not find job_applications.db!")
        print("   Searched in:")
        for path in possible_paths:
            print(f"   - {path}")
        print("\n   Please specify the database path:")
        db_input = input("   Path: ").strip()
        db_path = Path(db_input)
        
        if not db_path.exists():
            print(f"❌ Database not found at: {db_path}")
            exit(1)
    
    fix_id_gaps(db_path)
