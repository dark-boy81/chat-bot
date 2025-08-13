from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from pymongo import MongoClient
from datetime import datetime

app = FastAPI()

# فعال کردن CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# پیکربندی Google Generative AI
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# اتصال به MongoDB
mongo_client = MongoClient(os.environ.get("MONGO_URI"))
db = mongo_client["ai_chat_db"]   # نام دیتابیس
collection = db["qa_history"]     # نام کالکشن

@app.post("/api/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "")

    if not question.strip():
        return {"answer": "❌ لطفاً سوال خود را وارد کنید."}

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(question)
        answer = response.text

        # ذخیره در MongoDB
        collection.insert_one({
            "question": question,
            "answer": answer,
            "timestamp": datetime.utcnow()
        })

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"⚠ خطا: {str(e)}"}
