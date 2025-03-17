import requests  # ייבוא ספריית בקשות HTTP

#API_KEY = '87RYKHP1CUPBGWY1'  # מפתח API לשימוש ב-Alpha Vantage
API_KEY = '451FPPPSEOOZIDV4'  # API KEY 2 למטרת בדיקות עקב הגבלת פניות
#API_KEY = 'XX4SBD1SXLFLUSV2'  # API KEY 3 למטרת בדיקות עקב הגבלת פניות


class Broker:
    @staticmethod
    def update_price(symbol):
        """שליפת מחיר מניה בזמן אמת מ-Alpha Vantage"""
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()
        print(data)
        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            return float(data["Global Quote"]["05. price"])  # החזרת המחיר המעודכן
        
        raise ValueError("לא ניתן לעדכן מחיר המניה - בדוק את הסימול או את החיבור ל-API.")
