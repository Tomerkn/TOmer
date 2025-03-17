import sqlite3 # ייבוא DB
from dbmodel import PortfolioModel # ייבוא ניהול ה DB
from ollamamodel import AI_Agent # ייבוא בינה מלאכותית
import broker # ייבוא מחלקת מניות

class PortfolioController:
    def __init__(self, model):
        self.model = model # שמירת מסד הנתונים
        self.ollama_model = AI_Agent()

    def buy_security(self, security): # פונקציית הרכישה
        """רכישת נייר ערך והוספתו למסד הנתונים"""
        try:
            price = broker.Broker.update_price(security.name) # אם המנייה קיימת בפונקציה עדכן כמות
            self.model.cursor.execute(
                "INSERT INTO investments (name, price, amount) VALUES (?, ?, ?) ON CONFLICT(name) "
                "DO UPDATE SET amount = amount + excluded.amount",
                (security.name, price, security.amount)
            )
            self.model.conn.commit() # שמור שינויים במסד הנתונים
            return f"נייר ערך {security.name} נוסף בהצלחה!"
        except sqlite3.IntegrityError: # הנתון קיים במסד הנתונים  
            return "נייר הערך כבר קיים בתיק ההשקעות."

    def sell_security(self, name, amount): # מכירת נייר ערך 
        """מכירת נייר ערך והפחתת כמות ממסד הנתונים"""
        self.model.cursor.execute( 
            "UPDATE investments SET amount = amount - ? WHERE name = ? AND amount >= ?",
            (amount, name, amount)
        )
        self.model.conn.commit() # עדכון מסד הנתונים
        return f"מכרת {amount} מניות של {name}" # הדפסה למשתמש על ביצוע מכירה

    def get_portfolio(self): # שליפה של כל ניירות הערך בתיק 
        """שליפת כל ניירות הערך בתיק ההשקעות"""
        self.model.cursor.execute("SELECT name, price, amount FROM investments") # השליפה ממסד הנתונים
        rows = self.model.cursor.fetchall() # החזרת רשימה + פלט מסודר בטבלה
        return [{"name": row[0], "price": row[1], "amount": row[2]} for row in rows]
    
    def get_advice(self, question): # קבלת עצה מהבינה 
        """קבלת ייעוץ מסוכן AI"""
        return self.ollama_model.get_advice(question) #קבלת תשובה חזרה מהבינה 
class RiskManager:# סולם סיכונים לפי תחום ההשקעה
    RISK_SCALE = {
        "טכנולוגיה": 6, "תחבורה": 5, "אנרגיה": 4, "בריאות": 4,
        "תעשייה": 3, "פיננסים": 3, "נדלן": 2, "צריכה פרטית": 1
    }
    
    VARIATION_SCALE = {"נמוך": 1, "גבוה": 2} # סולם השונות נמוך או גבוה 

    @staticmethod
    def calculate_risk(security_type, sector, variation): # חישוב הסיכון לפי סוג קטגוריה ורמת שונות
        base_risk = RiskManager.RISK_SCALE.get(sector, 1) # קבלת רמת סיכון סקטור (קטגוריה)
        variation_risk = RiskManager.VARIATION_SCALE.get(variation, 1) # קבלת רמת השונות 
        
        if security_type == "אגח ממשלתית":
            return base_risk * variation_risk * 0.5 # חישוב אגח ממשלתית
        elif security_type == "אגח קונצרנית":
            return base_risk * variation_risk * 0.1 # חישוב אגח קונצרנית
        return base_risk * variation_risk # חישוב מניה רגילה 
