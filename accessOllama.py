import ollama # ייבוא ספרייה של מודל בינה מלאכותית

def getanswer( question): # פונקציה שמקבלת שאלה ומחזירה תשובה שזו תוצאת השאילתא של המודל  
    response = ollama.generate(model='deepseek-r1:latest', prompt=question)
    return response['response'] 
if __name__ == "__main__":
     question = input("ask a question:")
     print(getanswer(question)) 