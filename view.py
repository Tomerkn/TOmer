import tkinter as tk
from tkinter import messagebox
import requests
from controller import PortfolioController
from dbmodel import PortfolioModel as DatabaseManager
from securitiesmodel import Stock, Bond
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tabulate import tabulate

class PortfolioView:
    def __init__(self, root):
        """ אתחול הממשק הגרפי """
        self.root = root
        self.root.title("ניהול תיק השקעות")
        
        # יצירת אובייקט שמנהל את מסד הנתונים
        self.portfolio_model = DatabaseManager()
        # יצירת בקר לניהול הפעולות בתיק ההשקעות
        self.controller = PortfolioController(self.portfolio_model)
        
        self.create_widgets()
    
    def create_widgets(self):
        """ יצירת כפתורים וקלט לממשק """
        tk.Label(self.root, text="שם נייר ערך:").pack()
        self.symbol_entry = tk.Entry(self.root)
        self.symbol_entry.pack()
        
        tk.Label(self.root, text="כמות:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()
        
        tk.Button(self.root, text="קנייה", command=self.buy_stock).pack()
        tk.Button(self.root, text="מכירה", command=self.sell_stock).pack()
        tk.Button(self.root, text="בדיקת מחיר מניה", command=self.get_stock_price).pack()
        tk.Button(self.root, text="הצג תיק השקעות", command=self.display_portfolio).pack()
        tk.Button(self.root, text="הצג גרף תיק השקעות", command=self.show_portfolio_graph).pack()
        tk.Button(self.root, text="יציאה", command=self.root.quit).pack()
    
    def buy_stock(self):
        """ קניית נייר ערך והוספתו לתיק """
        symbol = self.symbol_entry.get().strip()
        amount = self.amount_entry.get().strip()
        
        if not symbol or not amount.isdigit():
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות .")
            return
        
        amount = int(amount)
        stock = Stock(symbol, amount)
        result = self.controller.buy_security(stock)
        messagebox.showinfo("פעולה", result)
        self.display_portfolio()
    
    def sell_stock(self):
        """ מכירת נייר ערך והוצאתו מהתיק """
        symbol = self.symbol_entry.get().strip()
        amount = self.amount_entry.get().strip()
        
        if not symbol or not amount.isdigit():
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות.")
            return
        
        amount = int(amount)
        result = self.controller.sell_security(symbol, amount)
        messagebox.showinfo("פעולה", result)
        self.display_portfolio()
    
    def get_stock_price(self):
        """ קבלת מחיר מניה ממקור חיצוני (Alpha Vantage) """
        symbol = self.symbol_entry.get().strip()
        if not symbol:
            messagebox.showerror("שגיאה", "הזן שם מניה וכמות.")
            return
        
        api_key = "87RYKHP1CUPBGWY1"
        url = f"https://www.alphavantage.com/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            response = requests.get(url, timeout=5).json()
            price = float(response.get("Global Quote", {}).get("05. price", 0))
            if price == 0:
                raise ValueError("מחיר לא נמצא")
            messagebox.showinfo("מחיר מניה", f"המחיר של {symbol}: {price} $")
        except (requests.exceptions.RequestException, KeyError, ValueError, TypeError):
            messagebox.showinfo("מחיר מניה", f"המחיר של {symbol} לא נמצא. ודא שהשם נכון ונסה שוב.")
    
    def show_portfolio_graph(self):
        """ הצגת גרף תיק ההשקעות """
        securities = self.controller.get_portfolio()
        if not securities:
            messagebox.showinfo("תיק השקעות", "אין ניירות ערך בתיק!")
            return
        
        labels = [sec['name'] for sec in securities]
        values = [sec['price'] * sec['amount'] for sec in securities]
        
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        
        graph_window = tk.Toplevel(self.root)
        graph_window.title("גרף תיק ההשקעות")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack()
        canvas.draw()
    
    def display_portfolio(self):
        """ הצגת התיק הנוכחי בטבלה """
        portfolio = self.controller.get_portfolio()
        if not portfolio:
            messagebox.showinfo("תיק השקעות", "אין ניירות ערך בתיק!")
            return
        
        headers = ["שם", "כמות", "מחיר"]
        table_data = [[sec['name'], sec['amount'], sec['price']] for sec in portfolio]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioView(root)
    root.mainloop()
