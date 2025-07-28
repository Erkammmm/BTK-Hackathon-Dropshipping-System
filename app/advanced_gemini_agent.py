import os
import httpx
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

class AdvancedGeminiAgent:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.api_url = GEMINI_API_URL
    
    async def analyze_book_and_generate_content(self, search_results: Dict, best_offer: Dict) -> Dict:
        """
        Kitap analizi yap ve gelişmiş içerik üret
        """
        try:
            # Tüm sonuçları analiz et
            analysis_prompt = self.create_analysis_prompt(search_results, best_offer)
            
            # Gemini'den analiz al
            analysis_result = await self.call_gemini_api(analysis_prompt)
            
            # SEO açıklaması üret
            seo_prompt = self.create_seo_prompt(best_offer, analysis_result)
            seo_result = await self.call_gemini_api(seo_prompt)
            
            # Satış önerisi üret
            sales_prompt = self.create_sales_prompt(best_offer, analysis_result)
            sales_result = await self.call_gemini_api(sales_prompt)
            
            # Özet oluştur
            summary_result = await self.create_summary(best_offer, analysis_result)
            
            return {
                'analysis': analysis_result,
                'seo_content': seo_result,
                'sales_recommendation': sales_result,
                'best_offer_summary': summary_result
            }
            
        except Exception as e:
            print(f"❌ Gemini analiz hatası: {str(e)}")
            return self.get_fallback_content(best_offer)
    
    def create_analysis_prompt(self, search_results: Dict, best_offer: Dict) -> str:
        """Kitap analizi için prompt oluştur"""
        
        # Tüm sonuçları formatla
        all_results = []
        for platform, results in search_results.items():
            if platform != 'best_offer' and isinstance(results, list):
                for result in results:
                    all_results.append({
                        'title': result.get('title', ''),
                        'price': result.get('price', 0),
                        'platform': result.get('platform', ''),
                        'url': result.get('url', '')
                    })
        
        prompt = f"""
Sen bir kitap analiz uzmanısın. Aşağıdaki kitap arama sonuçlarını analiz et:

KİTAP ADI: {best_offer.get('title', '')}
EN İYİ TEKLİF: {best_offer.get('platform', '')} - {best_offer.get('price', 0)} TL

TÜM SONUÇLAR:
"""
        
        for i, result in enumerate(all_results, 1):
            prompt += f"{i}. {result['title']} - {result['platform']} - {result['price']} TL\n"
        
        prompt += f"""

Bu kitap hakkında kısa bir analiz yaz:
- Kitabın popülerliği
- Fiyat durumu
- Hangi platformlarda bulunabilir
- En iyi fırsat nerede
- Hedef kitle kimdir

Türkçe olarak 3-4 cümlelik analiz yaz.
"""
        
        return prompt
    
    def create_seo_prompt(self, best_offer: Dict, analysis: str) -> str:
        """SEO içeriği için prompt oluştur"""
        
        prompt = f"""
Sen bir SEO uzmanısın. Aşağıdaki kitap için SEO uyumlu içerik üret:

KİTAP: {best_offer.get('title', '')}
PLATFORM: {best_offer.get('platform', '')}
FİYAT: {best_offer.get('price', 0)} TL

Bu kitap için SEO uyumlu içerik yaz:
- Başlık (60 karakter)
- Meta açıklama (160 karakter) 
- Ürün açıklaması (2-3 paragraf)
- Anahtar kelimeler (5 adet)
- Neden almalısınız (3 madde)

Türkçe olarak yaz.
"""
        
        return prompt
    
    def create_sales_prompt(self, best_offer: Dict, analysis: str) -> str:
        """Satış önerisi için prompt oluştur"""
        
        prompt = f"""
Sen bir satış stratejisi uzmanısın. Aşağıdaki kitap için satış önerileri üret:

KİTAP: {best_offer.get('title', '')}
PLATFORM: {best_offer.get('platform', '')}
FİYAT: {best_offer.get('price', 0)} TL

Bu kitap için satış önerileri yaz:
- Nerede listeleyebilirsiniz?
- Hangi fiyatla satabilirsiniz?
- Hedef kitle kimdir?
- Satış stratejisi nedir?

Türkçe olarak 3-4 cümlelik öneri yaz.
"""
        
        return prompt
    
    async def create_summary(self, best_offer: Dict, analysis: str) -> str:
        """Özet oluştur"""
        
        prompt = f"""
Aşağıdaki kitap için kısa özet oluştur:

KİTAP: {best_offer.get('title', '')}
PLATFORM: {best_offer.get('platform', '')}
FİYAT: {best_offer.get('price', 0)} TL

Bu kitap hakkında 2-3 cümlelik özet yaz:
- Kitabın durumu
- En iyi fırsat
- Öneri

Türkçe olarak yaz.
"""
        
        return await self.call_gemini_api(prompt)
    
    async def call_gemini_api(self, prompt: str) -> str:
        """Gemini API'yi çağır"""
        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH", 
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE"
                    }
                ]
            }
            
            print(f"🔍 Gemini API çağrılıyor: {self.api_url}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url, 
                    headers=headers, 
                    json=data, 
                    timeout=30.0
                )
                
                print(f"📡 Gemini API Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    if 'candidates' in result and len(result['candidates']) > 0:
                        return result['candidates'][0]['content']['parts'][0]['text']
                    else:
                        print(f"❌ Gemini API boş sonuç: {result}")
                        return "API boş sonuç döndü"
                else:
                    print(f"❌ Gemini API hatası: {response.status_code}")
                    print(f"❌ Response: {response.text}")
                    return f"API hatası: {response.status_code}"
                    
        except Exception as e:
            print(f"❌ Gemini API çağrı hatası: {str(e)}")
            return f"API çağrısı başarısız: {str(e)}"
    
    def get_fallback_content(self, best_offer: Dict) -> Dict:
        """Fallback içerik"""
        return {
            'analysis': f"{best_offer.get('title', '')} kitabı analiz edildi.",
            'seo_content': f"SEO içeriği: {best_offer.get('title', '')} - {best_offer.get('price', 0)} TL",
            'sales_recommendation': f"Satış önerisi: {best_offer.get('platform', '')} platformunda {best_offer.get('price', 0)} TL fiyatla satabilirsiniz.",
            'best_offer_summary': f"{best_offer.get('title', '')} kitabı {best_offer.get('platform', '')} platformunda {best_offer.get('price', 0)} TL fiyatla bulunabilir."
        } 