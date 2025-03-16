import sqlite3  # ייבוא מודול לניהול מסד נתונים SQLite

class PortfolioModel:
    def __init__(self):
        self.conn = sqlite3.connect("investments.db")  # חיבור למסד הנתונים
        self.cursor = self.conn.cursor()  # יצירת אובייקט לביצוע פקודות SQL
        self.create_tables()  # יצירת הטבלאות אם הן לא קיימות
    
    def create_tables(self):
        """יצירת טבלת ניירות ערך אם אינה קיימת"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- מזהה ייחודי לכל נייר ערך
                name TEXT UNIQUE,  -- שם המניה/אג"ח (חייב להיות ייחודי)
                price REAL,  -- מחיר הנייר ערך
                industry TEXT,  -- הענף אליו שייך נייר הערך
                variance TEXT,  -- רמת השינויים במחיר
                security_type TEXT  -- סוג הנייר (מניה/אג"ח)
            )
        ''')
        self.conn.commit()  # שמירת השינויים במסד הנתונים

    def add_security(self, name, price, industry, variance, security_type):
        """הוספת נייר ערך למסד הנתונים"""
        try:
            self.cursor.execute("INSERT INTO investments (name, price, industry, variance, security_type) VALUES (?, ?, ?, ?, ?)",
                                (name, price, industry, variance, security_type))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("נייר הערך כבר קיים בתיק ההשקעות.")

    def remove_security(self, name):
        """מחיקת נייר ערך מהתיק לפי השם"""
        self.cursor.execute("DELETE FROM investments WHERE name = ?", (name,))
        self.conn.commit()

    def get_securities(self):
        """שליפת כל ניירות הערך מהתיק"""
        self.cursor.execute("SELECT name, price FROM investments")
        return self.cursor.fetchall()
