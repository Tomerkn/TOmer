# הגדרה נכונה של מחלקות ניירות ערך
class Security: # מחלקת בסיס לכל ניירות הערך
    def __init__(self, name="Unknown", amount=0): # אתחול כמות
        self.name = name # שם נייר הערך
        self.amount = amount # כמות ניירות הערך שמוחזקים

class Stock(Security):# מחלקה שיורשת ממחלקת האב הראשית, מייצגת מניות
    def __init__(self,name="Unknown", amount=0):
        super().__init__(name,amount) # אתחול מחלקת אב

class Bond(Security):# מחלקה שמייצגת אגח, יורשת ממחלקת האב הראשית
    def __init__(self, name="Unknown"):
        super().__init__(name) # אתחול מחלקת אב

class RegularStock(Stock): # תת מחלקה - מניה רגילה יורשת ממחלקת מניות
    def __init__(self, name="Regular Stock"):
        super().__init__(name) # אתחול מחלקת אב

class PreferredStock(Stock): # מחלקת מניה מועדפת, יורשת ממחלקת מניות
    def __init__(self, name="Preferred Stock"):
        super().__init__(name) # אתחול מחלקת אב

class CorporateBond(Bond): # מחלקת אגח קונצרני, יורשת ממחלקת אגח 
    def __init__(self, name="Corporate Bond"):
        super().__init__(name) # אתחול מחלקת אב

class GovernmentalBond(Bond): # מחלקת אגח ממשלתי, יורשת ממחלקת אגח
    def __init__(self, name="Governmental Bond"): 
        super().__init__(name) # אתחול מחלקת אב
