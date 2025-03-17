import sqlite3  # ייבוא מודול לניהול מסד נתונים SQLite

class PortfolioModel: # מחלקה שמנהלת את מסד הנתונים
    def __init__(self):
        self.conn = sqlite3.connect("investments.db")  # חיבור למסד הנתונים
        self.cursor = self.conn.cursor()  # יצירת אובייקט לביצוע פקודות SQL
        self.create_tables()  # יצירת הטבלאות אם הן לא קיימות
    
    def create_tables(self): # יצירת טבלה אם לא קיימת בDB
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- מזהה ייחודי לכל נייר ערך
                name TEXT UNIQUE,  -- שם המניה/אג"ח 
                price REAL,  -- מחיר המניה
                amount REAL,  -- כמות המניה
                industry TEXT,  -- הענף אליו שייך המניה או אג״ח
                variance TEXT,  -- רמת השינויים במחיר
                security_type TEXT  -- סוג השירות (מניה/אג"ח)
            )
        ''')
        self.conn.commit()  # שמירת השינויים במסד הנתונים

    def add_security(self, name, price, industry, variance, security_type):
        #הוספת נייר ערך למסד הנתונים"
        try:
            self.cursor.execute("INSERT INTO investments (name, price, industry, variance, security_type) VALUES (?, ?, ?, ?, ?)",
                                (name, price, industry, variance, security_type))
            self.conn.commit()#שמירת שינויים בDB
        except sqlite3.IntegrityError: # הדפסת שגיאה אם קיים בDB
            print("נייר הערך כבר קיים בתיק ההשקעות.")

    def remove_security(self, name): # מחיקת נייר ערך מהתיק 
        self.cursor.execute("DELETE FROM investments WHERE name = ?", (name,)) #מחיקת רשומה
        self.conn.commit() # שמירת שינוי

    def get_securities(self): # שליפת כל ניירות הערך
        self.cursor.execute("SELECT name, price FROM investments")
        return self.cursor.fetchall()
