import httpx
import os
from typing import Dict, List, Optional

class RapidAPITrendyol:
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.base_url = "https://trendyol-scraper.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "trendyol-scraper.p.rapidapi.com"
        }
    
    async def search_book_sales_data(self, book_title: str) -> Dict:
        """RapidAPI ile Trendyol'dan kitap verisi getir"""
        try:
            if not self.api_key:
                print("⚠️ RapidAPI key bulunamadı")
                return self._get_default_data(book_title)
            
            # Ürün arama
            search_results = await self._search_products(book_title)
            
            if not search_results:
                return self._get_default_data(book_title)
            
            # En uygun ürünü seç
            best_product = self._select_best_product(search_results, book_title)
            
            # Ürün detaylarını getir
            product_details = await self._get_product_details(best_product['id'])
            
            return {
                'product_name': best_product['title'],
                'product_url': best_product['url'],
                'current_price': best_product['price'],
                'sales_data': product_details,
                'source': 'rapidapi_trendyol'
            }
            
        except Exception as e:
            print(f"❌ RapidAPI hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    async def _search_products(self, book_title: str) -> List[Dict]:
        """RapidAPI ile ürün ara"""
        try:
            url = f"{self.base_url}/search"
            params = {
                "query": book_title,
                "country": "tr",
                "category": "kitap"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('products', [])
                else:
                    print(f"❌ RapidAPI arama hatası: {response.status_code}")
                    return []
                    
        except Exception as e:
            print(f"❌ RapidAPI arama hatası: {str(e)}")
            return []
    
    def _select_best_product(self, products: List[Dict], book_title: str) -> Dict:
        """En uygun ürünü seç"""
        if not products:
            return {}
        
        best_match = products[0]
        best_score = 0
        
        for product in products:
            score = self._calculate_similarity(product.get('title', ''), book_title)
            if score > best_score:
                best_score = score
                best_match = product
        
        return best_match
    
    def _calculate_similarity(self, product_title: str, search_title: str) -> float:
        """Başlık benzerliği hesapla"""
        product_words = set(product_title.lower().split())
        search_words = set(search_title.lower().split())
        
        intersection = product_words.intersection(search_words)
        union = product_words.union(search_words)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    async def _get_product_details(self, product_id: str) -> Dict:
        """Ürün detaylarını getir"""
        try:
            url = f"{self.base_url}/product"
            params = {
                "productId": product_id,
                "country": "tr"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    return self._parse_product_data(data)
                else:
                    print(f"❌ RapidAPI ürün detay hatası: {response.status_code}")
                    return self._get_default_product_data()
                    
        except Exception as e:
            print(f"❌ RapidAPI ürün detay hatası: {str(e)}")
            return self._get_default_product_data()
    
    def _parse_product_data(self, data: Dict) -> Dict:
        """Ürün verilerini parse et"""
        try:
            return {
                'sales_count': data.get('salesCount', 0),
                'rating_count': data.get('ratingCount', 0),
                'rating_score': data.get('ratingScore', 0.0),
                'review_count': data.get('reviewCount', 0),
                'popularity_score': self._calculate_popularity_score(data)
            }
        except Exception as e:
            print(f"❌ Veri parse hatası: {str(e)}")
            return self._get_default_product_data()
    
    def _calculate_popularity_score(self, data: Dict) -> float:
        """Popülerlik skoru hesapla"""
        score = 0.0
        
        rating_count = data.get('ratingCount', 0)
        rating_score = data.get('ratingScore', 0.0)
        review_count = data.get('reviewCount', 0)
        sales_count = data.get('salesCount', 0)
        
        # Değerlendirme sayısı etkisi
        if rating_count > 0:
            score += min(rating_count / 100, 1.0) * 0.4
        
        # Değerlendirme puanı etkisi
        if rating_score > 0:
            score += (rating_score / 5.0) * 0.3
        
        # Yorum sayısı etkisi
        if review_count > 0:
            score += min(review_count / 50, 1.0) * 0.2
        
        # Satış sayısı etkisi
        if sales_count > 0:
            score += min(sales_count / 100, 1.0) * 0.1
        
        return min(score, 1.0)
    
    def _get_default_data(self, book_title: str) -> Dict:
        """Varsayılan veri"""
        return {
            'product_name': book_title,
            'product_url': '',
            'current_price': 0,
            'sales_data': self._get_default_product_data(),
            'source': 'default'
        }
    
    def _get_default_product_data(self) -> Dict:
        """Varsayılan ürün verisi"""
        return {
            'sales_count': 0,
            'rating_count': 0,
            'rating_score': 0.0,
            'review_count': 0,
            'popularity_score': 0.5
        } 