from view import PortfolioView  # ייבוא הממשק הגרפי
import tkinter as tk  # ייבוא Tkinter להפעלת היישום

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioView(root)  # הפעלת הממשק הגרפי
    root.mainloop()
