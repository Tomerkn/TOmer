import sqlite3
from dbmodel import PortfolioModel
from ollamamodel import AI_Agent
import broker

class PortfolioController:
    def __init__(self, model):
        self.model = model
        self.ollama_model = AI_Agent()

    def buy_security(self, security):
        """רכישת נייר ערך והוספתו למסד הנתונים"""
        try:
            price = broker.Broker.update_price(security.name)
            self.model.cursor.execute(
                "INSERT INTO investments (name, price, amount) VALUES (?, ?, ?) ON CONFLICT(name) "
                "DO UPDATE SET amount = amount + excluded.amount",
                (security.name, price, security.amount)
            )
            self.model.conn.commit()
            return f"נייר ערך {security.name} נוסף בהצלחה!"
        except sqlite3.IntegrityError:
            return "נייר הערך כבר קיים בתיק ההשקעות."

    def sell_security(self, name, amount):
        """מכירת נייר ערך והפחתת כמות ממסד הנתונים"""
        self.model.cursor.execute(
            "UPDATE investments SET amount = amount - ? WHERE name = ? AND amount >= ?",
            (amount, name, amount)
        )
        self.model.conn.commit()
        return f"מכרת {amount} מניות של {name}"

    def get_portfolio(self):
        """שליפת כל ניירות הערך בתיק ההשקעות"""
        self.model.cursor.execute("SELECT name, price, amount FROM investments")
        rows = self.model.cursor.fetchall()
        return [{"name": row[0], "price": row[1], "amount": row[2]} for row in rows]
    
    def get_advice(self, question):
        """קבלת ייעוץ מסוכן AI"""
        return self.ollama_model.get_advice(question)
class RiskManager:
    RISK_SCALE = {
        "טכנולוגיה": 6, "תחבורה": 5, "אנרגיה": 4, "בריאות": 4,
        "תעשייה": 3, "פיננסים": 3, "נדלן": 2, "צריכה פרטית": 1
    }
    
    VARIATION_SCALE = {"נמוך": 1, "גבוה": 2}

    @staticmethod
    def calculate_risk(security_type, sector, variation):
        base_risk = RiskManager.RISK_SCALE.get(sector, 1)
        variation_risk = RiskManager.VARIATION_SCALE.get(variation, 1)
        
        if security_type == "אגח ממשלתית":
            return base_risk * variation_risk * 0.5
        elif security_type == "אגח קונצרנית":
            return base_risk * variation_risk * 0.1
        return base_risk * variation_risk
