"""
Script to import parts catalog from a CSV file or add parts manually.
Usage:
    python import_parts_catalog.py parts.csv
    or
    python import_parts_catalog.py --add "PART123" "Part Description"
"""

import sqlite3
import sys
import csv
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "service.db")

def init_catalog_table():
    """Ensure the parts_catalog table exists"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS parts_catalog (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def import_from_csv(csv_file):
    """Import parts from a CSV file. Handles BARUDAN format: STOCK CODE,DESCRIPTION,..."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    imported = 0
    skipped = 0
    errors = 0
    
    # Try different encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    file_content = None
    
    for encoding in encodings:
        try:
            with open(csv_file, 'r', encoding=encoding) as f:
                file_content = list(csv.reader(f))
            break
        except UnicodeDecodeError:
            continue
    
    if file_content is None:
        print(f"Error: Could not read file with any encoding")
        conn.close()
        return
    
    # Skip header row (STOCK CODE, DESCRIPTION, etc.)
    start_row = 1
    
    for row in file_content[start_row:]:
        if len(row) < 1:
            continue
        
        # BARUDAN format: STOCK CODE (col 0), DESCRIPTION (col 1)
        part_number = str(row[0]).strip() if len(row) > 0 and row[0] else ""
        description = str(row[1]).strip() if len(row) > 1 and row[1] else ""
        
        # Skip empty rows or header-like rows
        if not part_number or part_number.upper() in ['STOCK CODE', 'PART NUMBER', 'PART_NUMBER', 'PART', '']:
            continue
        
        try:
            cur.execute("""
                INSERT INTO parts_catalog (part_number, description)
                VALUES (?, ?)
            """, (part_number, description))
            imported += 1
        except sqlite3.IntegrityError:
            # Part number already exists, update description
            cur.execute("""
                UPDATE parts_catalog 
                SET description = ?
                WHERE part_number = ?
            """, (description, part_number))
            skipped += 1
        except Exception as e:
            errors += 1
            if errors <= 5:  # Only show first 5 errors
                print(f"Error importing row {part_number}: {e}")
    
    conn.commit()
    conn.close()
    print(f"Import complete: {imported} new parts, {skipped} updated, {errors} errors")

def add_part(part_number, description):
    """Add a single part to the catalog"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO parts_catalog (part_number, description)
            VALUES (?, ?)
        """, (part_number, description))
        conn.commit()
        print(f"Added part: {part_number} - {description}")
    except sqlite3.IntegrityError:
        cur.execute("""
            UPDATE parts_catalog 
            SET description = ?
            WHERE part_number = ?
        """, (description, part_number))
        conn.commit()
        print(f"Updated part: {part_number} - {description}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_catalog_table()
    
    if len(sys.argv) == 2:
        # CSV file import
        csv_file = sys.argv[1]
        if os.path.exists(csv_file):
            import_from_csv(csv_file)
        else:
            print(f"Error: File {csv_file} not found")
    elif len(sys.argv) == 4 and sys.argv[1] == "--add":
        # Manual add
        part_number = sys.argv[2]
        description = sys.argv[3]
        add_part(part_number, description)
    else:
        print("Usage:")
        print("  python import_parts_catalog.py <csv_file>")
        print("  python import_parts_catalog.py --add <part_number> <description>")
        print("\nCSV format: part_number,description")

