import httpx
import re
from typing import Dict, List
from bs4 import BeautifulSoup
import random

class TrendyolScraper:
    def __init__(self):
        self.base_url = "https://www.trendyol.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Farklı User-Agent'lar
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
        ]
    
    async def search_book_sales_data(self, book_title: str) -> Dict:
        """Kitap satış verilerini ara"""
        try:
            print(f"🔍 Trendyol'da arama: {book_title}")
            
            # Kitap arama
            products = await self._search_books(book_title)
            if not products:
                print("❌ Ürün bulunamadı")
                return self._get_default_data(book_title)
            
            # En iyi ürünü seç
            best_product = self._select_best_product(products, book_title)
            if not best_product:
                print("❌ Uygun ürün bulunamadı")
                return self._get_default_data(book_title)
            
            # Ürün detaylarını al
            product_details = await self._get_product_details(best_product['url'])
            
            return {
                'product_name': best_product['title'],
                'product_url': best_product['url'],
                'current_price': best_product['price'],
                'sales_data': product_details,
                'source': 'trendyol_scraper'
            }
            
        except Exception as e:
            print(f"❌ Arama hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    async def _search_books(self, book_title: str) -> List[Dict]:
        """Kitap arama"""
        search_urls = [
            f"https://www.trendyol.com/sr?q={book_title.replace(' ', '+')}&qt=kitap",
            f"https://www.trendyol.com/sr?q={book_title.replace(' ', '+')}",
            f"https://www.trendyol.com/arama?q={book_title.replace(' ', '+')}"
        ]
        
        for url in search_urls:
            try:
                print(f"🔍 URL deneniyor: {url}")
                
                # Farklı User-Agent'lar dene
                for user_agent in self.user_agents:
                    try:
                        headers = self.headers.copy()
                        headers['User-Agent'] = user_agent
                        
                        async with httpx.AsyncClient() as client:
                            response = await client.get(url, headers=headers, timeout=10.0)
                            
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.content, 'html.parser')
                                products = self._parse_search_results(soup)
                                if products:
                                    print(f"✅ {len(products)} ürün bulundu")
                                    return products
                            elif response.status_code == 403:
                                print(f"⚠️ 403 hatası, farklı User-Agent deneniyor...")
                                continue
                            else:
                                print(f"⚠️ {response.status_code} hatası")
                                
                    except Exception as e:
                        print(f"⚠️ User-Agent hatası: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"⚠️ URL hatası: {str(e)}")
                continue
        
        print("❌ Tüm URL'ler başarısız")
        return []
    
    def _parse_search_results(self, soup: BeautifulSoup) -> List[Dict]:
        """Arama sonuçlarını parse et"""
        products = []
        
        try:
            # Ürün kartlarını bul
            product_cards = soup.find_all('div', class_='p-card-wrppr')
            
            for card in product_cards[:10]:  # İlk 10 ürün
                try:
                    # Başlık
                    title_elem = card.find('span', class_='prdct-desc-cntnr-name')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    
                    # Fiyat
                    price_elem = card.find('div', class_='prc-box-dscntd')
                    if not price_elem:
                        continue
                    price_text = price_elem.get_text(strip=True)
                    price = self._extract_price(price_text)
                    
                    # URL
                    link_elem = card.find('a')
                    if not link_elem:
                        continue
                    url = link_elem.get('href')
                    if url and not url.startswith('http'):
                        url = self.base_url + url
                    
                    products.append({
                        'title': title,
                        'price': price,
                        'url': url
                    })
                    
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"❌ Parse hatası: {str(e)}")
        
        return products
    
    def _select_best_product(self, products: List[Dict], book_title: str) -> Dict:
        """En iyi ürünü seç"""
        if not products:
            return None
        
        # Fiyata göre sırala
        products.sort(key=lambda x: x.get('price', 0))
        
        # En ucuz ürünü döndür
        return products[0]
    
    async def _get_product_details(self, product_url: str) -> Dict:
        """Ürün detay sayfasından veri çek"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(product_url, headers=self.headers, timeout=10.0)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    return self._parse_product_details(soup)
                else:
                    print(f"❌ Ürün detay hatası: {response.status_code}")
                    return self._get_default_product_data()
                    
        except Exception as e:
            print(f"❌ Ürün detay hatası: {str(e)}")
            return self._get_default_product_data()
    
    def _parse_product_details(self, soup: BeautifulSoup) -> Dict:
        """Ürün detaylarını parse et"""
        try:
            data = {
                'sales_count': 0,
                'rating_count': 0,
                'rating_score': 0.0,
                'review_count': 0,
                'popularity_score': 0.0
            }
            
            # Değerlendirme sayısı
            rating_elem = soup.find('span', class_='ratingCount')
            if rating_elem:
                rating_text = rating_elem.get_text(strip=True)
                data['rating_count'] = self._extract_number(rating_text)
            
            # Değerlendirme puanı
            score_elem = soup.find('span', class_='ratingScore')
            if score_elem:
                score_text = score_elem.get_text(strip=True)
                data['rating_score'] = self._extract_float(score_text)
            
            # Yorum sayısı
            review_elem = soup.find('span', class_='reviewCount')
            if review_elem:
                review_text = review_elem.get_text(strip=True)
                data['review_count'] = self._extract_number(review_text)
            
            # Satış göstergeleri (varsa)
            sales_indicators = [
                'son 30 günde',
                'satıldı',
                'kez satıldı',
                'adet satıldı'
            ]
            
            page_text = soup.get_text().lower()
            for indicator in sales_indicators:
                if indicator in page_text:
                    # Satış sayısını bul
                    pattern = r'(\d+)\s*(?:kez|adet)?\s*satıldı'
                    match = re.search(pattern, page_text)
                    if match:
                        data['sales_count'] = int(match.group(1))
                        break
            
            # Popülerlik skoru hesapla
            data['popularity_score'] = self._calculate_popularity_score(data)
            
            return data
            
        except Exception as e:
            print(f"❌ Detay parse hatası: {str(e)}")
            return self._get_default_product_data()
    
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
    
    def _extract_price(self, price_text: str) -> float:
        """Fiyat metninden sayısal değeri çıkar"""
        try:
            # Sayıları ve nokta/virgülü al
            price_match = re.search(r'[\d.,]+', price_text.replace(' ', ''))
            if price_match:
                price_str = price_match.group(0)
                # Virgülü noktaya çevir
                price_str = price_str.replace(',', '.')
                return float(price_str)
        except:
            pass
        return 0.0
    
    def _extract_number(self, text: str) -> int:
        """Metinden sayı çıkar"""
        try:
            match = re.search(r'\d+', text.replace(' ', ''))
            if match:
                return int(match.group(0))
        except:
            pass
        return 0
    
    def _extract_float(self, text: str) -> float:
        """Metinden ondalık sayı çıkar"""
        try:
            match = re.search(r'[\d.,]+', text.replace(' ', ''))
            if match:
                price_str = match.group(0).replace(',', '.')
                return float(price_str)
        except:
            pass
        return 0.0
    
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