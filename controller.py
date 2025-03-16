import sqlite3
from dbmodel import PortfolioModel
from ollamamodel import AI_Agent

class PortfolioController:
    def __init__(self, model):
        self.model = model
        self.ollama_model = AI_Agent()

    def buy_security(self, security):
        """רכישת נייר ערך והוספתו למסד הנתונים"""
        try:
            self.model.cursor.execute(
                "INSERT INTO investments (name, basevalue, ammont) VALUES (?, ?, ?)",
                (security.name, security.price, security.amount)
            )
            self.model.conn.commit()
            return f"נייר ערך {security.name} נוסף בהצלחה!"
        except sqlite3.IntegrityError:
            return "נייר הערך כבר קיים בתיק ההשקעות."

    def sell_security(self, name, amount):
        """מכירת נייר ערך והפחתת כמות ממסד הנתונים"""
        self.model.cursor.execute(
            "UPDATE investments SET ammont = ammont - ? WHERE name = ? AND ammont >= ?",
            (amount, name, amount)
        )
        self.model.conn.commit()
        return f"מכרת {amount} מניות של {name}"

    def get_portfolio(self):
        """שליפת כל ניירות הערך בתיק ההשקעות"""
        self.model.cursor.execute("SELECT name, basevalue, ammont FROM investments")
        rows = self.model.cursor.fetchall()
        return [{"name": row[0], "price": row[1], "amount": row[2]} for row in rows]
    
    def get_advice(self, question):
        """קבלת ייעוץ מסוכן AI"""
        return self.ollama_model.get_advice(question)
