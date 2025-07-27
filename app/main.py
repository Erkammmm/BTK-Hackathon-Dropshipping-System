from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from app.fetch_price import fetch_kitapyurdu_price
from app.gemini_agent import generate_title_and_description
from app.trendyol_api import add_product_to_trendyol
import asyncio
import random

load_dotenv()

app = FastAPI()

class AddBookRequest(BaseModel):
    book_name: str

@app.post("/add-book")
async def add_book(request: AddBookRequest):
    # 1. Kitapyurdu'ndan fiyat ve ürün bilgisi çek
    book_info = await fetch_kitapyurdu_price(request.book_name)
    if not book_info or not book_info.get('title'):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya fiyat çekilemedi.")

    # 2. Otomatik fiyatlandırma (düzeltilmiş mantık)
    base_price = book_info.get('price')  # Cimri'den gelen temel fiyat
    if base_price is None:
        raise HTTPException(status_code=404, detail="Fiyat bulunamadı.")
    
    # Trendyol satış fiyatı hesaplama
    komisyon = base_price * 0.21
    kargo = 70
    kar = 100
    trendyol_price = round(base_price + komisyon + kargo + kar, 2)
    
    # Piyasa fiyatı = Trendyol fiyatından daha yüksek (biz daha ucuz satıyor gibi görünmeliyiz)
    market_price = trendyol_price + random.uniform(50, 100)

    # 3. Gemini ile başlık ve açıklama üret
    gemini_result = await generate_title_and_description(book_info, language='tr')

    # 4. Trendyol API ile ürünü ekle
    product_info = {
        'title': gemini_result['title'],
        'description': gemini_result['description'],
        'market_price': round(market_price, 2),  # Piyasa satış fiyatı (Trendyol'dan yüksek)
        'price': trendyol_price,       # Trendyol satış fiyatı (hesaplanan fiyat)
        'image_url': book_info.get('image_url'),
        'url': book_info.get('url'),
        'author': book_info.get('author')
    }
    trendyol_result = await add_product_to_trendyol(product_info)

    return {
        "book_info": book_info,
        "base_price": base_price,
        "market_price": round(market_price, 2),
        "trendyol_price": trendyol_price,
        "gemini_result": gemini_result,
        "trendyol_result": trendyol_result
    } 