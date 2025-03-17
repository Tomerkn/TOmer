import requests  # ייבוא ספריית בקשות HTTP
import ollama

class AI_Agent:
    def __init__(self):
        print("""אתחול מחלקה לחיבור ל-AI""")
        self.ollama_api_url = "http://localhost:11434/api/generate"  # כתובת השרת המקומי

    def get_advice(self, symbol):
    
        response = ollama.generate(model='llama3', prompt=f"האם כדאי להשקיע ב {symbol}? use only 250 chars in your answer")
        return response['response']
