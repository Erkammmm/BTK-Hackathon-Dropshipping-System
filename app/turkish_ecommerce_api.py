import httpx
import re
from typing import Dict, List
import os

class TurkishEcommerceAPI:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY', '446147d13dmshf8ac457d3b45074p117d0ejsn5e226696f69a')
        self.base_url = "https://turkish-price-comparation-and-ecommerce-data.p.rapidapi.com"
        self.headers = {
            'x-rapidapi-host': 'turkish-price-comparation-and-ecommerce-data.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }
    
    async def search_book_data(self, book_title: str) -> Dict:
        """Kitap verilerini ara"""
        try:
            print(f"🔍 Türk E-ticaret API'den veri alınıyor: {book_title}")
            
            # Önce crawler endpoint'ini dene
            crawler_data = await self._get_crawler_data(book_title)
            if crawler_data and crawler_data.get('source') != 'default':
                return crawler_data
            
            # Sonra search endpoint'ini dene
            search_data = await self._get_search_data(book_title)
            if search_data and search_data.get('source') != 'default':
                return search_data
            
            # Hiçbiri çalışmazsa varsayılan veri
            return self._get_default_data(book_title)
                    
        except Exception as e:
            print(f"❌ Türk E-ticaret API hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    async def _get_crawler_data(self, book_title: str) -> Dict:
        """Crawler endpoint'inden veri al"""
        try:
            print("🔍 Crawler endpoint deneniyor...")
            
            # Farklı crawler endpoint'leri dene
            crawler_urls = [
                f"{self.base_url}/v1/api/crawler",
                f"{self.base_url}/v1/api/crawler?page=1",
                f"{self.base_url}/v1/api/crawler?limit=10",
                f"{self.base_url}/v1/api/crawler?page=1&limit=10"
            ]
            
            for url in crawler_urls:
                try:
                    print(f"🔍 URL deneniyor: {url}")
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            url, 
                            headers=self.headers, 
                            timeout=15.0
                        )
                        
                        print(f"📊 Response Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            data = response.json()
                            print(f"📊 Data: {data}")
                            return self._parse_crawler_results(data, book_title)
                        elif response.status_code == 403:
                            print("⚠️ 403 hatası, farklı URL deneniyor...")
                            continue
                        elif response.status_code == 429:
                            print("⚠️ 429 hatası, bekleniyor...")
                            import asyncio
                            await asyncio.sleep(2)
                            continue
                            
                except Exception as e:
                    print(f"⚠️ URL hatası: {str(e)}")
                    continue
            
            print("❌ Tüm crawler URL'leri başarısız")
            return None
                    
        except Exception as e:
            print(f"❌ Crawler hatası: {str(e)}")
            return None
    
    async def _get_search_data(self, book_title: str) -> Dict:
        """Search endpoint'inden veri al"""
        try:
            print("🔍 Search endpoint deneniyor...")
            
            # Farklı search parametreleri dene
            search_params = [
                {'query': book_title},
                {'query': book_title[:30]},
                {'query': book_title.split()[0] if book_title.split() else book_title},
                {'q': book_title},
                {'search': book_title}
            ]
            
            for params in search_params:
                try:
                    print(f"🔍 Parametre deneniyor: {params}")
                    
                    search_url = f"{self.base_url}/v1/api/search"
                    
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            search_url, 
                            headers=self.headers, 
                            params=params,
                            timeout=15.0
                        )
                        
                        print(f"📊 Response Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            data = response.json()
                            print(f"📊 Data: {data}")
                            return self._parse_search_results(data, book_title)
                        elif response.status_code == 403:
                            print("⚠️ 403 hatası, farklı parametre deneniyor...")
                            continue
                        elif response.status_code == 429:
                            print("⚠️ 429 hatası, bekleniyor...")
                            import asyncio
                            await asyncio.sleep(2)
                            continue
                            
                except Exception as e:
                    print(f"⚠️ Parametre hatası: {str(e)}")
                    continue
            
            print("❌ Tüm search parametreleri başarısız")
            return None
                    
        except Exception as e:
            print(f"❌ Search hatası: {str(e)}")
            return None
    
    def _parse_crawler_results(self, data: Dict, book_title: str) -> Dict:
        """Crawler sonuçlarını parse et"""
        try:
            print(f"📊 Crawler verisi parse ediliyor: {data}")
            
            # Veri yapısını kontrol et
            if not data or not isinstance(data, dict):
                return self._get_default_data(book_title)
            
            # En iyi eşleşmeyi bul
            best_match = self._find_best_match_from_data(data, book_title)
            
            if not best_match:
                return self._get_default_data(book_title)
            
            # Satış verilerini hesapla
            sales_data = self._calculate_sales_data(best_match)
            
            return {
                'product_name': best_match.get('title', book_title),
                'product_url': best_match.get('url', ''),
                'current_price': best_match.get('price', 0),
                'sales_data': sales_data,
                'source': 'turkish_ecommerce_crawler',
                'raw_data': best_match
            }
            
        except Exception as e:
            print(f"❌ Crawler parse hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    def _parse_search_results(self, data: Dict, book_title: str) -> Dict:
        """Search sonuçlarını parse et"""
        try:
            print(f"📊 Search verisi parse ediliyor: {data}")
            
            # Veri yapısını kontrol et
            if not data or not isinstance(data, dict):
                return self._get_default_data(book_title)
            
            # En iyi eşleşmeyi bul
            best_match = self._find_best_match_from_data(data, book_title)
            
            if not best_match:
                return self._get_default_data(book_title)
            
            # Satış verilerini hesapla
            sales_data = self._calculate_sales_data(best_match)
            
            return {
                'product_name': best_match.get('title', book_title),
                'product_url': best_match.get('url', ''),
                'current_price': best_match.get('price', 0),
                'sales_data': sales_data,
                'source': 'turkish_ecommerce_search',
                'raw_data': best_match
            }
            
        except Exception as e:
            print(f"❌ Search parse hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    def _find_best_match_from_data(self, data: Dict, book_title: str) -> Dict:
        """Veriden en iyi eşleşmeyi bul"""
        try:
            # Veri yapısını kontrol et
            results = []
            
            # Farklı veri yapılarını dene
            if 'results' in data:
                results = data['results']
            elif 'data' in data:
                results = data['data']
            elif 'items' in data:
                results = data['items']
            elif isinstance(data, list):
                results = data
            else:
                # Tek ürün olabilir
                if 'title' in data or 'name' in data:
                    results = [data]
            
            if not results:
                return None
            
            # En iyi eşleşmeyi bul
            scored_results = []
            for result in results:
                if not isinstance(result, dict):
                    continue
                    
                title = result.get('title', result.get('name', ''))
                similarity = self._calculate_similarity(title.lower(), book_title.lower())
                scored_results.append((similarity, result))
            
            # En yüksek skorlu sonucu döndür
            if scored_results:
                scored_results.sort(key=lambda x: x[0], reverse=True)
                return scored_results[0][1]
            
            return None
            
        except Exception as e:
            print(f"❌ Eşleşme bulma hatası: {str(e)}")
            return None
    
    def _calculate_similarity(self, title1: str, title2: str) -> float:
        """Başlık benzerliği hesapla"""
        if not title1 or not title2:
            return 0.0
        
        # Ortak kelimeleri say
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _calculate_sales_data(self, product: Dict) -> Dict:
        """Satış verilerini hesapla"""
        try:
            # API'den gelen verileri kullan
            rating_count = product.get('rating_count', product.get('reviews_count', 0))
            rating_score = product.get('rating_score', product.get('rating', 0.0))
            review_count = product.get('review_count', product.get('comments_count', 0))
            sales_count = product.get('sales_count', product.get('sold_count', 0))
            
            # Popülerlik skoru hesapla
            popularity_score = self._calculate_popularity_score({
                'rating_count': rating_count,
                'rating_score': rating_score,
                'review_count': review_count,
                'sales_count': sales_count
            })
            
            return {
                'sales_count': sales_count,
                'rating_count': rating_count,
                'rating_score': rating_score,
                'review_count': review_count,
                'popularity_score': popularity_score
            }
            
        except Exception as e:
            print(f"❌ Satış verisi hesaplama hatası: {str(e)}")
            return self._get_default_sales_data()
    
    def _calculate_popularity_score(self, data: Dict) -> float:
        """Popülerlik skoru hesapla"""
        score = 0.0
        
        # Değerlendirme sayısı etkisi
        if data['rating_count'] > 0:
            score += min(data['rating_count'] / 100, 1.0) * 0.4
        
        # Değerlendirme puanı etkisi
        if data['rating_score'] > 0:
            score += (data['rating_score'] / 5.0) * 0.3
        
        # Yorum sayısı etkisi
        if data['review_count'] > 0:
            score += min(data['review_count'] / 50, 1.0) * 0.2
        
        # Satış sayısı etkisi
        if data['sales_count'] > 0:
            score += min(data['sales_count'] / 100, 1.0) * 0.1
        
        return min(score, 1.0)
    
    def _get_default_data(self, book_title: str) -> Dict:
        """Varsayılan veri"""
        return {
            'product_name': book_title,
            'product_url': '',
            'current_price': 0,
            'sales_data': self._get_default_sales_data(),
            'source': 'default'
        }
    
    def _get_default_sales_data(self) -> Dict:
        """Varsayılan satış verisi"""
        return {
            'sales_count': 0,
            'rating_count': 0,
            'rating_score': 0.0,
            'review_count': 0,
            'popularity_score': 0.5
        } 