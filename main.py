from view import PortfolioView  # ייבוא הממשק הגרפי
import tkinter as tk  # ייבוא הספרייה שתאפשר את הממשק הגרפי 

if __name__ == "__main__":
    root = tk.Tk() # יצירת חלון של ממשק גרפי
    app = PortfolioView(root)  # הפעלת הממשק הגרפי
    root.mainloop() # לולאה שמשאירה את הממשק הגרפי פתוח
