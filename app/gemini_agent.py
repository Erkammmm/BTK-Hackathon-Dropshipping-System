import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY

async def generate_title_and_description(book_info: dict, language: str = 'tr'):
    prompt = f"""
Aşağıdaki kitap bilgilerine göre Trendyol'da satışa uygun, SEO dostu başlık ve açıklama üret:

Kitap Adı: {book_info.get('title','')}
Yazar: {book_info.get('author','')}
Fiyat: {book_info.get('price','')} TL

Başlık: [Kitap adını kullan, "Kitap" kelimesi ekle, SEO için anahtar kelimeler kullan]
Açıklama: [Kitap hakkında 3-4 paragraf açıklama yaz. İlk paragraf kitabın özeti, ikinci paragraf yazar hakkında, üçüncü paragraf neden okunmalı, dördüncü paragraf satış odaklı. "Kitap", "okuma", "edebiyat", "roman" gibi anahtar kelimeler kullan. Trendyol'da satışa yönelik olsun.]

Dil: {language}
"""
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(GEMINI_API_URL, headers=headers, json=data, timeout=20)
        if resp.status_code != 200:
            return {
                'title': f"{book_info.get('title', '')} Kitap",
                'description': f"{book_info.get('title', '')} - Bu kitap, edebiyat dünyasının önemli eserlerinden biridir. {book_info.get('author', 'Yazar')} tarafından kaleme alınan bu roman, okuyucuları derin bir okuma deneyimine davet ediyor. Kitap, günümüz edebiyatının en çok okunan eserleri arasında yer alıyor. Trendyol'da uygun fiyat ve hızlı kargo ile sizlerle buluşuyor."
            }
        try:
            result = resp.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            # Başlık ve açıklamayı ayır
            lines = text.split('\n')
            title = f"{book_info.get('title', '')} Kitap"
            description = text
            # Eğer "Başlık:" ve "Açıklama:" varsa ayır
            for i, line in enumerate(lines):
                if line.startswith('Başlık:'):
                    title = line.replace('Başlık:', '').strip()
                elif line.startswith('Açıklama:'):
                    description = '\n'.join(lines[i+1:]).strip()
                    break
            return {
                'title': title,
                'description': description
            }
        except Exception:
            return {
                'title': f"{book_info.get('title', '')} Kitap",
                'description': f"{book_info.get('title', '')} - Bu kitap, edebiyat dünyasının önemli eserlerinden biridir. {book_info.get('author', 'Yazar')} tarafından kaleme alınan bu roman, okuyucuları derin bir okuma deneyimine davet ediyor. Kitap, günümüz edebiyatının en çok okunan eserleri arasında yer alıyor. Trendyol'da uygun fiyat ve hızlı kargo ile sizlerle buluşuyor."
            } 