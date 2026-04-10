import os
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# HTML fayllar uchun papka
templates = Jinja2Templates(directory="templates")

# AI Sozlamalari (API kalitlarni keyin Railway'da kiritamiz)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

genai.configure(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "code": ""})

@app.post("/generate")
async def generate(request: Request, prompt: str = Form(...)):
    # Biz Google Gemini modelini ishlatamiz (Tez va ko'p hollarda tekin)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    system_instruction = (
        "Sen UzBuild AI yordamchisisan. Foydalanuvchi o'zbek tilida dasturlash bo'yicha topshiriq beradi. "
        "Sen unga eng optimal, xatosiz va professional kodni qaytarishing kerak. "
        "Faqat kodni o'zini qaytar, ortiqcha gapirma. Kod Markdown formatida bo'lsin."
    )
    
    full_prompt = f"{system_instruction}\n\nFoydalanuvchi topshirig'i: {prompt}"
    
    try:
        response = model.generate_content(full_prompt)
        ai_code = response.text
    except Exception as e:
        ai_code = f"Xatolik yuz berdi: {str(e)}"

    return templates.TemplateResponse("index.html", {"request": request, "code": ai_code, "prompt": prompt})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
