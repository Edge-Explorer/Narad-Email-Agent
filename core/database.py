import sqlite3
import os
from datetime import datetime

class NaradDatabase:
    """Manages the local CRM database for job applications."""
    def __init__(self, db_name="narad_crm.db"):
        self.db_path = os.path.abspath(db_name)
        self._init_db()

    def _init_db(self):
        """Initializes the database schema."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Applications Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recipient_email TEXT,
                    recipient_name TEXT,
                    company TEXT,
                    job_title TEXT,
                    status TEXT DEFAULT 'Sent',
                    sent_at DATETIME,
                    last_follow_up DATETIME,
                    jd_text TEXT,
                    thread_id TEXT
                )
            ''')
            # Profiles Table (for Multi-CV)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    cv_path TEXT,
                    focus_area TEXT
                )
            ''')
            conn.commit()

    def log_application(self, email, name, company, title, jd_text):
        """Logs a new sent application."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO applications (recipient_email, recipient_name, company, job_title, sent_at, jd_text)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, name, company, title, datetime.now().isoformat(), jd_text))
            conn.commit()

    def get_pending_followups(self, days=4):
        """Finds applications that haven't been followed up in X days."""
        # This will be used for the Ghost Protector logic
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM applications WHERE status = 'Sent'
            ''')
            return cursor.fetchall()

    def update_status(self, app_id, status):
        """Updates the status of an application."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE applications SET status = ? WHERE id = ?', (status, app_id))
            conn.commit()
