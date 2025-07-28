import os
import httpx
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class SerpAgent:
    def __init__(self):
        self.api_key = os.getenv('SERP_API_KEY')
        self.base_url = "https://serpapi.com/search"
        
    async def search_book(self, book_name: str) -> Dict:
        """
        Google Shopping'de kitap ara
        """
        try:
            # Google Shopping arama parametreleri
            params = {
                'api_key': self.api_key,
                'engine': 'google_shopping',
                'q': f"{book_name} kitap",
                'gl': 'tr',  # Türkiye
                'hl': 'tr',  # Türkçe
                'num': 10    # 10 sonuç
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    return self.parse_serp_results(data, book_name)
                else:
                    print(f"❌ SerpAPI hatası: {response.status_code}")
                    return self.get_fallback_results(book_name)
                    
        except Exception as e:
            print(f"❌ SerpAPI arama hatası: {str(e)}")
            return self.get_fallback_results(book_name)
    
    def parse_serp_results(self, data: Dict, book_name: str) -> Dict:
        """
        SerpAPI sonuçlarını parse et
        """
        try:
            shopping_results = data.get('shopping_results', [])
            
            if not shopping_results:
                return self.get_fallback_results(book_name)
            
            # En iyi 5 sonucu al
            best_results = []
            for result in shopping_results[:5]:
                if result.get('price') and result.get('title'):
                    # URL'yi düzelt
                    url = result.get('link', '')
                    if not url and result.get('source'):
                        # Eğer URL yoksa, platform URL'sini oluştur
                        url = self.generate_platform_url(result.get('source', ''), result.get('title', ''))
                    
                    # Fiyatı düzelt
                    price = self.extract_price(result.get('price', '0'))
                    if price == 0:
                        # Eğer fiyat 0 ise, orijinal fiyat metnini kullan
                        price_text = result.get('price', '0')
                        price = self.extract_price_from_text(price_text)
                    
                    best_results.append({
                        'title': result.get('title', ''),
                        'price': price,
                        'url': url,
                        'image_url': result.get('thumbnail', ''),
                        'platform': self.extract_platform(result.get('source', '')),
                        'source': 'serpapi',
                        'original_price': result.get('price', '0')
                    })
            
            # En iyi teklifi bul
            if best_results:
                best_offer = min(best_results, key=lambda x: x.get('price', float('inf')))
                
                return {
                    'search_results': {
                        'serpapi': best_results,
                        'best_offer': best_offer
                    },
                    'best_offer': best_offer
                }
            else:
                return self.get_fallback_results(book_name)
                
        except Exception as e:
            print(f"❌ Parse hatası: {str(e)}")
            return self.get_fallback_results(book_name)
    
    def extract_price(self, price_text: str) -> float:
        """Fiyat metninden sayısal değeri çıkar"""
        try:
            # Gelişmiş fiyat çıkarma fonksiyonunu kullan
            return self.extract_price_from_text(price_text)
        except Exception as e:
            print(f"❌ Ana fiyat çıkarma hatası: {str(e)} - Metin: {price_text}")
            return 0.0
    
    def extract_price_from_text(self, price_text: str) -> float:
        """Gelişmiş fiyat çıkarma"""
        try:
            import re
            
            # Önce orijinal metni temizle
            clean_text = str(price_text).replace(' ', '').replace('₺', '').replace('TL', '')
            
            # Nokta ve virgül kontrolü
            if ',' in clean_text and '.' in clean_text:
                # Hem nokta hem virgül varsa (örn: 1.850,00)
                if clean_text.index(',') > clean_text.index('.'):
                    # Virgül noktadan sonra geliyorsa (1.850,00)
                    clean_text = clean_text.replace('.', '').replace(',', '.')
                else:
                    # Nokta virgülden sonra geliyorsa (1,850.00)
                    clean_text = clean_text.replace(',', '')
            elif ',' in clean_text:
                # Sadece virgül varsa
                if clean_text.count(',') == 1:
                    # Tek virgül varsa (1,850)
                    parts = clean_text.split(',')
                    if len(parts[1]) <= 2:  # Kuruş kısmı
                        clean_text = clean_text.replace(',', '.')
                    else:  # Binlik ayırıcı
                        clean_text = clean_text.replace(',', '')
                else:
                    # Birden fazla virgül varsa (1,850,00)
                    clean_text = clean_text.replace(',', '')
            
            # Farklı fiyat formatlarını dene
            patterns = [
                r'(\d+\.\d{2})',  # 1850.00 formatı
                r'(\d+\.\d{1})',  # 1850.0 formatı
                r'(\d+)',         # 1850 formatı
            ]
            
            for pattern in patterns:
                match = re.search(pattern, clean_text)
                if match:
                    price_str = match.group(1)
                    price = float(price_str)
                    
                    # Fiyat mantık kontrolü
                    if price < 100 and '₺' in str(price_text) or 'TL' in str(price_text):
                        # Eğer fiyat 100'den küçükse ve TL işareti varsa, muhtemelen binlik ayırıcı eksik
                        # Orijinal metni tekrar kontrol et
                        original_match = re.search(r'(\d+[.,]\d+)', str(price_text))
                        if original_match:
                            original_price = original_match.group(1).replace(',', '.')
                            if float(original_price) > price * 10:
                                return float(original_price)
                    
                    return price
            
            return 0.0
        except Exception as e:
            print(f"❌ Fiyat çıkarma hatası: {str(e)} - Metin: {price_text}")
            return 0.0
    
    def generate_platform_url(self, source: str, title: str) -> str:
        """Platform URL'si oluştur"""
        source_lower = source.lower()
        title_slug = title.lower().replace(' ', '-').replace('/', '-')
        
        if 'kitapyurdu' in source_lower:
            return f'https://www.kitapyurdu.com/kitap/{title_slug}'
        elif 'idefix' in source_lower:
            return f'https://www.idefix.com/kitap/{title_slug}'
        elif 'dr' in source_lower:
            return f'https://www.dr.com.tr/kitap/{title_slug}'
        elif 'n11' in source_lower:
            return f'https://www.n11.com/arama?q={title_slug}'
        elif 'trendyol' in source_lower:
            return f'https://www.trendyol.com/sr?q={title_slug}'
        else:
            return f'https://www.google.com/search?q={title_slug}'
    
    def extract_platform(self, source: str) -> str:
        """Kaynak platformu çıkar"""
        source_lower = source.lower()
        if 'kitapyurdu' in source_lower:
            return 'Kitapyurdu'
        elif 'idefix' in source_lower:
            return 'İdefix'
        elif 'dr' in source_lower:
            return 'D&R'
        elif 'n11' in source_lower:
            return 'N11'
        elif 'trendyol' in source_lower:
            return 'Trendyol'
        else:
            return source or 'Bilinmeyen'
    
    def get_fallback_results(self, book_name: str) -> Dict:
        """
        Fallback sonuçları (SerpAPI çalışmazsa)
        """
        return {
            'search_results': {
                'serpapi': [
                    {
                        'title': f'{book_name} - Kitapyurdu',
                        'price': 35.90,
                        'url': f'https://www.kitapyurdu.com/kitap/{book_name.lower().replace(" ", "-")}',
                        'image_url': 'https://via.placeholder.com/300x400/8B4513/ffffff?text=Kitap',
                        'platform': 'Kitapyurdu',
                        'source': 'fallback'
                    },
                    {
                        'title': f'{book_name} - İdefix',
                        'price': 42.50,
                        'url': f'https://www.idefix.com/kitap/{book_name.lower().replace(" ", "-")}',
                        'image_url': 'https://via.placeholder.com/300x400/0066cc/ffffff?text=Kitap',
                        'platform': 'İdefix',
                        'source': 'fallback'
                    }
                ],
                'best_offer': {
                    'title': f'{book_name} - Kitapyurdu',
                    'price': 35.90,
                    'url': f'https://www.kitapyurdu.com/kitap/{book_name.lower().replace(" ", "-")}',
                    'image_url': 'https://via.placeholder.com/300x400/8B4513/ffffff?text=Kitap',
                    'platform': 'Kitapyurdu',
                    'source': 'fallback'
                }
            },
            'best_offer': {
                'title': f'{book_name} - Kitapyurdu',
                'price': 35.90,
                'url': f'https://www.kitapyurdu.com/kitap/{book_name.lower().replace(" ", "-")}',
                'image_url': 'https://via.placeholder.com/300x400/8B4513/ffffff?text=Kitap',
                'platform': 'Kitapyurdu',
                'source': 'fallback'
            }
        } 