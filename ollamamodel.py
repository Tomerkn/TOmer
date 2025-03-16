import requests  # ייבוא ספריית בקשות HTTP

class AI_Agent:
    def __init__(self):
        print("""אתחול מחלקה לחיבור ל-AI""")
        self.ollama_api_url = "http://localhost:11434/api/generate"  # כתובת השרת המקומי

    def get_advice(self, security):
        """שליחת בקשה ל-AI לקבלת המלצה"""
        data = {"prompt": f"האם כדאי להשקיע ב {security.name}?", "model": "finance-gpt"}
        try:
            response = requests.post(self.ollama_api_url, json=data, timeout=5)
            return response.json().get("response", "לא התקבלה תשובה מה-AI")
        except Exception as e:
            return f"שגיאה בהתחברות ל-Ollama: {e}"
