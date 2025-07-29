import asyncio
import re
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TrendyolScraperSelenium:
    def __init__(self):
        self.base_url = "https://www.trendyol.com"
        self.driver = None
        
    def _setup_driver(self):
        """Chrome driver'ı ayarla"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Görünmez mod
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            return True
        except Exception as e:
            print(f"❌ Chrome driver hatası: {str(e)}")
            return False
    
    async def search_book_sales_data(self, book_title: str) -> Dict:
        """Trendyol'da kitap arama ve satış verilerini getir"""
        try:
            if not self._setup_driver():
                return self._get_default_data(book_title)
            
            # 1. Kitap arama
            search_results = await self._search_books(book_title)
            
            if not search_results:
                return self._get_default_data(book_title)
            
            # 2. En uygun ürünü seç
            best_product = self._select_best_product(search_results, book_title)
            
            # 3. Ürün detay sayfasından veri çek
            product_data = await self._get_product_details(best_product['url'])
            
            return {
                'product_name': best_product['title'],
                'product_url': best_product['url'],
                'current_price': best_product['price'],
                'sales_data': product_data,
                'source': 'trendyol_selenium'
            }
            
        except Exception as e:
            print(f"❌ Selenium scraping hatası: {str(e)}")
            return self._get_default_data(book_title)
        finally:
            if self.driver:
                self.driver.quit()
    
    async def _search_books(self, book_title: str) -> List[Dict]:
        """Trendyol'da kitap ara"""
        try:
            # Arama URL'i
            search_url = f"{self.base_url}/sr?q={book_title.replace(' ', '+')}&qt=kitap"
            
            print(f"🔍 Trendyol arama URL: {search_url}")
            self.driver.get(search_url)
            
            # Sayfanın yüklenmesini bekle
            time.sleep(3)
            
            # Ürün kartlarını bul
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="product-card"]')
            
            if not product_cards:
                # Alternatif selector'lar dene
                product_cards = self.driver.find_elements(By.CSS_SELECTOR, '.p-card-wrppr')
            
            if not product_cards:
                product_cards = self.driver.find_elements(By.CSS_SELECTOR, '[class*="product-card"]')
            
            print(f"📦 Bulunan ürün sayısı: {len(product_cards)}")
            
            products = []
            for card in product_cards[:10]:  # İlk 10 ürün
                try:
                    product_data = self._extract_product_data(card)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    print(f"❌ Ürün veri çıkarma hatası: {str(e)}")
                    continue
            
            return products
            
        except Exception as e:
            print(f"❌ Arama hatası: {str(e)}")
            return []
    
    def _extract_product_data(self, card) -> Optional[Dict]:
        """Ürün kartından veri çıkar"""
        try:
            # Ürün başlığı
            title_selectors = [
                '[data-testid="product-card-name"]',
                '.prdct-desc-cntnr-name',
                'span[class*="name"]',
                'h3',
                'span'
            ]
            
            title = ""
            for selector in title_selectors:
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, selector)
                    title = title_elem.text.strip()
                    if title and len(title) > 5:
                        break
                except:
                    continue
            
            # Ürün linki
            link_selectors = ['a', '[data-testid="product-card-link"]']
            url = ""
            for selector in link_selectors:
                try:
                    link_elem = card.find_element(By.CSS_SELECTOR, selector)
                    url = link_elem.get_attribute('href')
                    if url:
                        break
                except:
                    continue
            
            # Fiyat
            price_selectors = [
                '[data-testid="price-current-price"]',
                '.prc-box-dscntd',
                '[class*="price"]',
                'span[class*="price"]'
            ]
            
            price = 0.0
            for selector in price_selectors:
                try:
                    price_elem = card.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_elem.text.strip()
                    price = self._extract_price(price_text)
                    if price > 0:
                        break
                except:
                    continue
            
            # Değerlendirme sayısı
            rating_selectors = [
                '[data-testid="rating-count"]',
                '.ratingCount',
                'span[class*="rating"]'
            ]
            
            rating_count = 0
            for selector in rating_selectors:
                try:
                    rating_elem = card.find_element(By.CSS_SELECTOR, selector)
                    rating_text = rating_elem.text.strip()
                    rating_count = self._extract_number(rating_text)
                    if rating_count > 0:
                        break
                except:
                    continue
            
            if title and url:
                return {
                    'title': title,
                    'url': url,
                    'price': price,
                    'rating_count': rating_count
                }
            
        except Exception as e:
            print(f"❌ Veri çıkarma hatası: {str(e)}")
        
        return None
    
    def _select_best_product(self, products: List[Dict], book_title: str) -> Dict:
        """En uygun ürünü seç"""
        if not products:
            return {}
        
        # Basit eşleştirme algoritması
        best_match = products[0]
        best_score = 0
        
        for product in products:
            score = self._calculate_similarity(product['title'], book_title)
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
    
    async def _get_product_details(self, product_url: str) -> Dict:
        """Ürün detay sayfasından veri çek"""
        try:
            print(f"🔍 Ürün detay sayfası: {product_url}")
            self.driver.get(product_url)
            
            # Sayfanın yüklenmesini bekle
            time.sleep(3)
            
            # Sayfa içeriğini al
            page_source = self.driver.page_source
            
            return self._parse_product_details_from_source(page_source)
            
        except Exception as e:
            print(f"❌ Ürün detay hatası: {str(e)}")
            return self._get_default_product_data()
    
    def _parse_product_details_from_source(self, page_source: str) -> Dict:
        """Sayfa kaynağından ürün detaylarını parse et"""
        try:
            data = {
                'sales_count': 0,
                'rating_count': 0,
                'rating_score': 0.0,
                'review_count': 0,
                'popularity_score': 0.0
            }
            
            # Değerlendirme sayısı
            rating_patterns = [
                r'(\d+)\s*değerlendirme',
                r'(\d+)\s*kişi değerlendirdi',
                r'ratingCount["\']?\s*:\s*["\']?(\d+)',
                r'(\d+)\s*adet değerlendirme'
            ]
            
            for pattern in rating_patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    data['rating_count'] = int(match.group(1))
                    break
            
            # Değerlendirme puanı
            score_patterns = [
                r'(\d+\.?\d*)\s*\/\s*5',
                r'ratingScore["\']?\s*:\s*["\']?(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*yıldız'
            ]
            
            for pattern in score_patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    data['rating_score'] = float(match.group(1))
                    break
            
            # Yorum sayısı
            review_patterns = [
                r'(\d+)\s*yorum',
                r'(\d+)\s*adet yorum',
                r'reviewCount["\']?\s*:\s*["\']?(\d+)'
            ]
            
            for pattern in review_patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    data['review_count'] = int(match.group(1))
                    break
            
            # Satış göstergeleri
            sales_patterns = [
                r'(\d+)\s*(?:kez|adet)?\s*satıldı',
                r'son\s*\d+\s*günde\s*(\d+)\s*satıldı',
                r'(\d+)\s*adet\s*satıldı',
                r'satış\s*(\d+)'
            ]
            
            for pattern in sales_patterns:
                match = re.search(pattern, page_source, re.IGNORECASE)
                if match:
                    data['sales_count'] = int(match.group(1))
                    break
            
            # Popülerlik skoru hesapla
            data['popularity_score'] = self._calculate_popularity_score(data)
            
            print(f"📊 Çekilen veriler: {data}")
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
            numbers = re.findall(r'\d+', text.replace(' ', ''))
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0
    
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