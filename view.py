import tkinter as tk # ייבוא מחלקה לעיצוב גרפי בפייתון
from tkinter import messagebox # ייבוא של חלונית צפה 
import requests # ייבוא של בקשות 443 
from ollamamodel import AI_Agent # ייבוא מודל בינה מלאכותית 
from controller import PortfolioController,RiskManager # ייבוא מחלקות ניהול סיכון וניהול
from dbmodel import PortfolioModel as DatabaseManager # ייבוא מסד הנתונים
from securitiesmodel import Stock, Bond # ייבוא כל המחלקות הרלוונטיות
import matplotlib.pyplot as plt # ייבוא ספריה לגרפים
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # שילוב גרפים בספרייה גרפית
from tabulate import tabulate # הצגת טבלאות בהדפסה - ספרייה מותאמת

class PortfolioView: # הצגת מחלקה גרפית 
    def __init__(self, root): # אתחול ממשק
        self.root = root # שמירת החלון הראשי הצף 
        self.root.title("ניהול תיק השקעות") # כותרת החלןו 
        
        # יצירת אובייקט שמנהל את מסד הנתונים
        self.portfolio_model = DatabaseManager()
        # יצירת בקר לניהול הפעולות בתיק ההשקעות
        self.controller = PortfolioController(self.portfolio_model)
        
        self.create_widgets()
    
    def create_widgets(self): # יצירת כפתורים וקלט לממשק הגרפי
        # הגדרת שדות ממשק
        tk.Label(self.root, text="שם נייר ערך:").pack() 
        self.symbol_entry = tk.Entry(self.root) # ה
        self.symbol_entry.pack()

        # הגדרת שדות ממשק
        tk.Label(self.root, text="כמות:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        # הגדרת שדות ממשק
        tk.Label(self.root, text="קטגוריה:").pack()
        self.sector_entry = tk.Entry(self.root)
        self.sector_entry.pack()

        # הגדרת שדות ממשק
        tk.Label(self.root, text="סוג:").pack()
        self.security_type_entry = tk.Entry(self.root)
        self.security_type_entry.pack()

        # הגדרת שדות ממשק
        tk.Label(self.root, text="שונות:").pack()
        self.variation_entry = tk.Entry(self.root)
        self.variation_entry.pack()     

        # הגדרת כפתורים ממשק
        tk.Button(self.root, text="קנייה", command=self.buy_stock).pack()
        tk.Button(self.root, text="מכירה", command=self.sell_stock).pack()
        tk.Button(self.root, text="בדיקת מחיר מניה", command=self.get_stock_price).pack()
        tk.Button(self.root, text="הצג תיק השקעות", command=self.display_portfolio).pack()
        tk.Button(self.root, text="הצג גרף תיק השקעות", command=self.show_portfolio_graph).pack()
        tk.Button(self.root, text="התייעץ עם הבינה", command=self.ask_ollama).pack()
        tk.Button(self.root, text="חשב סיכון", command=self.calculate_risk).pack()
        tk.Button(self.root, text="יציאה", command=self.root.quit).pack()

    
  def buy_stock(self): # קניית ניר ערך והוספה לתיק 
        symbol = self.symbol_entry.get().strip() # קבלת שם מנייה מהמשתמש
        amount = self.amount_entry.get().strip() # קבלת כמות מהמשתמש
        
        if not symbol or not amount.isdigit(): # בדיקת תקינות נתונים
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות .") # הדפסת הודעה אם יש שגיאות
            return
        
        amount = int(amount) # המרה ממחרוזת למספר בכמות 
        stock = Stock(symbol, amount) # יצירת אובייקט מניה
        result = self.controller.buy_security(stock) # ביצוע קניה 
        messagebox.showinfo("פעולה", result) #הדפסת הודעה 
        self.display_portfolio() #עדכון תיק לאחר רכישה 
    
    def sell_stock(self): # פונקציה למכירת ניירות ערך
        """ מכירת נייר ערך והוצאתו מהתיק """
        symbol = self.symbol_entry.get().strip() # קבלת שם מנייה מהמשתמש
        amount = self.amount_entry.get().strip() # קבלת כמות מהמשתמש
        
        if not symbol or not amount.isdigit(): # בדיקת תקינות קלט
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות.") # הדפסת שגיאה אם לא  
            return
        
        amount = int(amount) # המרה מחרוזת למספר
        result = self.controller.sell_security(symbol, amount) # ביצוע מכירה
        messagebox.showinfo("פעולה", result) # הדפסת פעולה
        self.display_portfolio() # עדכון התיק לאחר מכירה
    
    def get_stock_price(self): # מקבלת את המחירים של המנייה מ API
        """ קבלת מחיר מניה ממקור חיצוני (Alpha Vantage) """
        symbol = self.symbol_entry.get().strip() # מקבלת שם מנייה מהמשתמש
        if not symbol: #אם המשתמש לא הזין כלום 
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות.") # תדפיס שגיאה
            return
        
        api_key = "451FPPPSEOOZIDV4" # tokenAPI
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            response = requests.get(url, timeout=5).json() # שלח 443 לבקשת המידע ואז תמיר לקבצים
            price = float(response.get("Global Quote", {}).get("05. price", 0)) # חילוץ מחירים
            if price == 0:
                raise ValueError("מחיר לא נמצא") # תדפיס שגיאה אם לא קיבלת מחיר
            messagebox.showinfo("מחיר מניה", f"המחיר של {symbol}: {price} $") # תדפיס למשתמש תשובה
        except (requests.exceptions.RequestException, KeyError, ValueError, TypeError):# במידה שהייתה שגיאה תדפיס
            messagebox.showinfo("מחיר מניה", f"המחיר של {symbol} לא נמצא. ודא שהשם נכון ונסה שוב.")

    def ask_ollama(self): # פונקציה שמקבלת מידע מהבינה
        symbol = self.symbol_entry.get().strip() # מקבלת ממשתמש שם מנייה
        if not symbol: # אם לא מקבלת מנייה 
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות.") # תדפיס שגיאה
            return
        advice = self.controller.get_advice(symbol) # תשלח את שם המניה למחלקה לקבלת תשובה
        messagebox.showinfo("עצה חשובה",advice) # תדפיס תשובה 
    
    def show_portfolio_graph(self):# פונקציה להצגת גרף השקעות
        """ הצגת גרף תיק ההשקעות """
        securities = self.controller.get_portfolio() # מייבאת נתונים מתיק ההשקעות
        if not securities: # אם אין ניירות ערך בתיק תדפיס
            messagebox.showinfo("תיק השקעות", "אין ניירות ערך בתיק!")
            return
        
        labels = [sec['name'] for sec in securities] # שמות מניות בתיק
        values = [sec['price'] * sec['amount'] for sec in securities] # חישוב ערך לכל מניה
        
        fig, ax = plt.subplots() # יצירת גרף 
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90) # ציור גרף עוגה
        ax.axis('equal') # שמירת יחס בתוך הגרף
        
        graph_window = tk.Toplevel(self.root) # צור חלונית חדשה לגרף
        graph_window.title("גרף תיק ההשקעות") # כותרת 
        canvas = FigureCanvasTkAgg(fig, master=graph_window) # שילוב גרף בממשק
        canvas.get_tk_widget().pack() # הצגת גרף
        canvas.draw() # עדכון תצוגה
    
    
    def calculate_risk(self): # חישוב סיכון בתיק 
        sector = self.sector_entry.get().strip() # קבלת ערך קטגוריה או סקטור ממשתמש
        security_type = self.security_type_entry.get().strip() # קבלת נייר ערך
        variation = self.variation_entry.get().strip() # קבלת שונות 
        if not sector: # אם לא קטגוריה או סקטור 
            messagebox.showerror("שגיאה", "הזן קטגוריות.") # תדפיס 
            return
        if not security_type: # אם לא סוג נייר ערך 
            messagebox.showerror("שגיאה", "הזן סוג.") # תדפיס
            return
        if not variation: # אם לא סוג שונות 
            messagebox.showerror("שגיאה", "הזן שונות.") # תדפיס
            return
        risk = RiskManager.calculate_risk(security_type,sector,variation) # חישוב רמת סיכון
        messagebox.showinfo("עצה חשובה",risk) # תצוגה למשתמש

    
    
    
    
    def display_portfolio(self): # פונקציה שמציגה את תיק ההשקעטת בטבלה
        """ הצגת התיק הנוכחי בטבלה """
        portfolio = self.controller.get_portfolio() # מביאים ניירות ערך מהתיק
        if not portfolio: # אם אין תעשה
            messagebox.showinfo("תיק השקעות", "אין ניירות ערך בתיק!") # תדפיס הודעה
            return
        
        headers = ["שם", "כמות", "מחיר"]
        headers_rev = ["םש", "תומכ", "ריחמ"]
        table_data = [[sec['name'], sec['amount'], sec['price']] for sec in portfolio]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        messagebox.showinfo("תיק השקעות",tabulate(table_data, headers=headers_rev, tablefmt="fancy_grid"))
    
if __name__ == "__main__":
    root = tk.Tk() # יצירת חלון ראשי 
    app = PortfolioView(root) # יצירת מופע ממשק משתמש
    root.mainloop() # משאיר את החלונית פתוחה
