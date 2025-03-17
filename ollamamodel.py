import requests  # ייבוא ספריית בקשות HTTP
import ollama # ייבוא הספרייה של המודל בינה

class AI_Agent: # מחלקה של סוכן בינה מלאכותית
    def __init__(self):
        print("""אתחול מחלקה לחיבור ל-AI""") # הדפסה שתגיד לנו שהסוכן מוכן
        self.ollama_api_url = "http://localhost:11434/api/generate"  # כתובת השרת המקומי

    def get_advice(self, symbol): # פונקצייה של ייעוץ 
    
        response = ollama.generate(model='llama3', prompt=f"האם כדאי להשקיע ב {symbol}? use only 250 chars in your answer")
        return response['response'] # מחזיר תשובה מהמודל
