import os
import httpx
from datetime import datetime
from typing import Dict, Optional, List

class AmazonCommentsAPI:
    """Amazon ürün yorumlarını çeken API"""
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY', '446147d13dmshf8ac457d3b45074p117d0ejsn5e226696f69a')
        self.base_url = "https://real-time-amazon-data.p.rapidapi.com"
        self.headers = {
            'x-rapidapi-host': 'real-time-amazon-data.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }
    
    async def get_product_comments(self, asin: str, limit: int = 100) -> Dict:
        """
        Amazon'dan ürün yorumlarını ve detaylarını al (Çoklu sayfa desteği)
        
        Args:
            asin: Amazon ürün ASIN kodu
            limit: Kaç yorum alınacağı (varsayılan: 100)
            
        Returns:
            Dict: Yorum verileri ve ürün detayları
        """
        try:
            print(f"🔍 Amazon yorumları alınıyor... ASIN: {asin}, Limit: {limit}")
            
            all_reviews = []
            page = 1
            max_pages = 10  # Maksimum 10 sayfa (her sayfada ~10 yorum)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                while len(all_reviews) < limit and page <= max_pages:
                    url = f"{self.base_url}/product-reviews"
                    params = {
                        'asin': asin,
                        'country': 'US',
                        'page': page,
                        'sort_by': 'TOP_REVIEWS',
                        'star_rating': 'ALL',
                        'verified_purchases_only': 'false',
                        'images_or_videos_only': 'false',
                        'current_format_only': 'false'
                    }
                    
                    print(f"📄 Sayfa {page} alınıyor...")
                    response = await client.get(url, headers=self.headers, params=params)
                    
                    if response.status_code == 200:
                        data = response.json()
                        page_reviews = data.get('data', {}).get('reviews', [])
                        
                        if page_reviews:
                            all_reviews.extend(page_reviews)
                            print(f"✅ Sayfa {page}: {len(page_reviews)} yorum alındı")
                            page += 1
                        else:
                            print(f"⚠️ Sayfa {page}: Yorum yok, durduruluyor")
                            break
                    else:
                        print(f"❌ Sayfa {page} API Hatası: {response.status_code}")
                        break
                
                print(f"📊 Toplam {len(all_reviews)} yorum alındı")
                
                if all_reviews:
                    # Ürün detaylarını ve satış verilerini al
                    product_details = await self._get_product_details(asin)
                    
                    # Product Offers API'sinden satıcı bilgilerini al
                    offers_data = await self._get_product_offers(asin)
                    
                    # Satış verilerini birleştir
                    sales_data = self._extract_sales_data_from_product_details(product_details)
                    if offers_data:
                        sales_data.update(offers_data)
                    
                    # Veriyi işle ve formatla
                    processed_data = self._process_comments_data({'data': {'reviews': all_reviews}}, limit, product_details)
                    processed_data['sales_data'] = sales_data
                    return processed_data
                else:
                    print("⚠️ Hiç yorum bulunamadı")
                    return self._get_sample_comments_data()
                    
        except Exception as e:
            print(f"❌ Amazon yorumları alınırken hata: {str(e)}")
            return self._get_sample_comments_data()
    
    async def search_book_asin(self, book_title: str) -> Optional[str]:
        """Kitap adından ASIN bul"""
        try:
            print(f"🔍 Amazon'da kitap aranıyor: {book_title}")
            
            url = f"{self.base_url}/search"
            params = {
                'query': f"{book_title} book",
                'country': 'US',
                'page': 1
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    products = data.get('data', {}).get('products', [])
                    
                    if products:
                        # İlk ürünün ASIN'ini al
                        first_product = products[0]
                        asin = first_product.get('asin')
                        title = first_product.get('product_title', '')
                        print(f"✅ Kitap bulundu: {title} (ASIN: {asin})")
                        return asin
                    else:
                        print("❌ Kitap bulunamadı")
                        return None
                else:
                    print(f"❌ Arama API hatası: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"❌ Kitap arama hatası: {str(e)}")
            return None
    
    async def _get_product_details(self, asin: str) -> Dict:
        """Amazon'dan ürün detaylarını al"""
        try:
            print(f"🔍 Ürün detayları alınıyor... ASIN: {asin}")
            
            url = f"{self.base_url}/product-details"
            params = {
                'asin': asin,
                'country': 'US'
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Ürün detayları alındı: {response.status_code}")
                    
                    # Satış verilerini çıkar
                    sales_data = self._extract_sales_data_from_product_details(data.get('data', {}))
                    print(f"🔍 Satış verileri çıkarıldı: {sales_data}")
                    
                    # Debug: Tüm API yanıtını göster
                    print(f"🔍 Product Details API yanıtı: {data}")
                    
                    return data.get('data', {})
                else:
                    print(f"❌ Ürün detayları API hatası: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"❌ Ürün detayları alınırken hata: {str(e)}")
            return {}
    
    def _extract_sales_data_from_product_details(self, product_details: Dict) -> Dict:
        """Ürün detaylarından satış verilerini çıkar"""
        try:
            if not product_details:
                return {}
            
            sales_data = {
                'estimated_monthly_sales': 0,
                'daily_average': 0,
                'confidence_score': 0.7,
                'total_ratings': 0,
                'rating_distribution': {},
                'sales_volume': None,
                'seller_count': 0,
                'availability': 'Unknown'
            }
            
            # Sales Volume (satış hacmi) - en önemli veri (farklı alan isimleri dene)
            sales_volume = (
                product_details.get('sales_volume') or 
                product_details.get('sales_rank') or
                product_details.get('rank') or
                product_details.get('best_sellers_rank') or
                product_details.get('amazon_rank')
            )
            print(f"🔍 Sales Volume/Rank: {sales_volume}")
            
            # Tüm ürün detaylarını debug et
            print(f"🔍 Tüm ürün detayları: {list(product_details.keys())}")
            
            if sales_volume:
                sales_data['sales_volume'] = sales_volume
                # Sales volume'dan aylık satış tahmini
                if isinstance(sales_volume, str):
                    # "1000+ sold" formatından sayı çıkar
                    import re
                    numbers = re.findall(r'\d+', sales_volume)
                    if numbers:
                        volume_number = int(numbers[0])
                        if '+' in sales_volume:
                            volume_number = int(volume_number * 1.5)  # + işareti varsa %50 artır
                        sales_data['estimated_monthly_sales'] = volume_number
                        sales_data['daily_average'] = round(volume_number / 30, 2)
                        sales_data['confidence_score'] = 0.9
                        print(f"✅ Sales Volume'dan tahmin: {volume_number} aylık satış")
                elif isinstance(sales_volume, int):
                    sales_data['estimated_monthly_sales'] = sales_volume
                    sales_data['daily_average'] = round(sales_volume / 30, 2)
                    sales_data['confidence_score'] = 0.9
                    print(f"✅ Sales Volume'dan tahmin: {sales_volume} aylık satış")
            
            # Toplam değerlendirme sayısı
            total_ratings = product_details.get('product_num_ratings', 0)
            print(f"🔍 Total Ratings: {total_ratings}")
            if total_ratings:
                sales_data['total_ratings'] = total_ratings
                # Değerlendirme sayısından popülerlik tahmini
                if not sales_data['estimated_monthly_sales']:
                    if total_ratings > 1000:
                        sales_data['estimated_monthly_sales'] = 500
                        sales_data['daily_average'] = 17
                        sales_data['confidence_score'] = 0.8
                        print(f"✅ Ratings'den tahmin: 500 aylık satış (1000+ rating)")
                    elif total_ratings > 500:
                        sales_data['estimated_monthly_sales'] = 300
                        sales_data['daily_average'] = 10
                        sales_data['confidence_score'] = 0.7
                        print(f"✅ Ratings'den tahmin: 300 aylık satış (500+ rating)")
                    elif total_ratings > 100:
                        sales_data['estimated_monthly_sales'] = 150
                        sales_data['daily_average'] = 5
                        sales_data['confidence_score'] = 0.6
                        print(f"✅ Ratings'den tahmin: 150 aylık satış (100+ rating)")
            
            # Rating distribution
            rating_dist = product_details.get('rating_distribution', {})
            if rating_dist:
                sales_data['rating_distribution'] = rating_dist
            
            # Stok durumu
            availability = product_details.get('product_availability')
            if availability:
                sales_data['availability'] = availability
            
            # Best seller durumu
            is_best_seller = product_details.get('is_best_seller', False)
            if is_best_seller and not sales_data['estimated_monthly_sales']:
                sales_data['estimated_monthly_sales'] = 1000
                sales_data['daily_average'] = 33
                sales_data['confidence_score'] = 0.85
            
            # Amazon Choice durumu
            is_amazon_choice = product_details.get('is_amazon_choice', False)
            if is_amazon_choice and not sales_data['estimated_monthly_sales']:
                sales_data['estimated_monthly_sales'] = 800
                sales_data['daily_average'] = 27
                sales_data['confidence_score'] = 0.8
            
            return sales_data
            
        except Exception as e:
            print(f"❌ Satış verileri çıkarılırken hata: {str(e)}")
            return {}
    
    async def _get_product_offers(self, asin: str) -> Dict:
        """Amazon'dan ürün tekliflerini al"""
        try:
            print(f"🔍 Ürün teklifleri alınıyor... ASIN: {asin}")
            
            url = f"{self.base_url}/product-offers"
            params = {
                'asin': asin,
                'country': 'US',
                'limit': 100,
                'page': 1
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Ürün teklifleri alındı: {response.status_code}")
                    
                    # Satıcı bilgilerini çıkar
                    offers_data = self._extract_offers_data(data.get('data', {}))
                    print(f"🔍 Teklif verileri çıkarıldı: {offers_data}")
                    
                    return offers_data
                else:
                    print(f"❌ Ürün teklifleri API hatası: {response.status_code}")
                    return {}
                    
        except Exception as e:
            print(f"❌ Ürün teklifleri alınırken hata: {str(e)}")
            return {}
    
    def _extract_offers_data(self, offers_data: Dict) -> Dict:
        """Teklif verilerinden satış bilgilerini çıkar"""
        try:
            if not offers_data:
                return {}
            
            offers = offers_data.get('offers', [])
            if not offers:
                return {}
            
            # Satıcı sayısı
            seller_count = len(offers)
            
            # Fiyat aralığı
            prices = [offer.get('price', 0) for offer in offers if offer.get('price')]
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            
            # Stok durumu
            in_stock_count = sum(1 for offer in offers if offer.get('availability') == 'In Stock')
            
            return {
                'seller_count': seller_count,
                'min_price': min_price,
                'max_price': max_price,
                'price_range': max_price - min_price if max_price > min_price else 0,
                'in_stock_count': in_stock_count,
                'out_of_stock_count': seller_count - in_stock_count,
                'competition_level': 'High' if seller_count > 10 else 'Medium' if seller_count > 5 else 'Low'
            }
            
        except Exception as e:
            print(f"❌ Teklif verileri çıkarılırken hata: {str(e)}")
            return {}
    
    def _process_comments_data(self, raw_data: Dict, limit: int, product_details: Dict = None) -> Dict:
        """Ham yorum verilerini işle ve formatla"""
        try:
            data = raw_data.get('data', {})
            reviews = data.get('reviews', [])
            
            # Limit uygula
            if limit and len(reviews) > limit:
                reviews = reviews[:limit]
            
            processed_comments = []
            total_rating = 0
            rating_count = 0
            
            for review in reviews:
                try:
                    # Tarih formatını düzelt
                    date_str = review.get('review_date', '')
                    if date_str:
                        # "Reviewed in the United States on September 18, 2024" formatını parse et
                        try:
                            # Tarih kısmını çıkar
                            if "on " in date_str:
                                date_part = date_str.split("on ")[-1]
                                parsed_date = datetime.strptime(date_part, '%B %d, %Y')
                                formatted_date = parsed_date.strftime('%Y-%m-%d')
                            else:
                                formatted_date = datetime.now().strftime('%Y-%m-%d')
                        except:
                            formatted_date = datetime.now().strftime('%Y-%m-%d')
                    else:
                        formatted_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # Yıldız değerini sayıya çevir
                    rating = review.get('review_star_rating', '0')
                    if isinstance(rating, str):
                        try:
                            rating = float(rating.replace(',', '.'))
                        except:
                            rating = 0
                    
                    processed_comment = {
                        'date': formatted_date,
                        'rating': rating,
                        'comment': review.get('review_comment', ''),
                        'user': review.get('review_author', 'Anonim'),
                        'title': review.get('review_title', ''),
                        'year': datetime.strptime(formatted_date, '%Y-%m-%d').year if formatted_date else datetime.now().year,
                        'verified': review.get('is_verified_purchase', False),
                        'helpful_votes': str(review.get('helpful_vote_statement', '')) if review.get('helpful_vote_statement') else '0 kişi faydalı buldu',
                        'review_link': review.get('review_link', '')
                    }
                    
                    processed_comments.append(processed_comment)
                    
                    if rating > 0:
                        total_rating += rating
                        rating_count += 1
                        
                except Exception as e:
                    print(f"⚠️ Yorum işlenirken hata: {str(e)}")
                    continue
            
            # Ortalama yıldız hesapla
            average_rating = total_rating / rating_count if rating_count > 0 else 0
            
            # Yıllara göre ortalama yıldız hesapla
            yearly_ratings = {}
            for comment in processed_comments:
                year = comment['year']
                if year not in yearly_ratings:
                    yearly_ratings[year] = {'total': 0, 'count': 0}
                yearly_ratings[year]['total'] += comment['rating']
                yearly_ratings[year]['count'] += 1
            
            # Yıllık ortalamaları hesapla
            for year in yearly_ratings:
                if yearly_ratings[year]['count'] > 0:
                    yearly_ratings[year]['average'] = round(yearly_ratings[year]['total'] / yearly_ratings[year]['count'], 2)
                else:
                    yearly_ratings[year]['average'] = 0.0
            
            print(f"🔍 Yıllık veriler: {yearly_ratings}")
            
            return {
                'total_comments': len(processed_comments),
                'average_rating': round(average_rating, 2),
                'source': 'amazon_api',
                'timestamp': datetime.now().isoformat(),
                'comments': processed_comments,
                'yearly_ratings': yearly_ratings,
                'product_info': {
                    'asin': data.get('asin', ''),
                    'total_reviews': data.get('total_reviews', 0),
                    'country': data.get('country', 'US'),
                    'domain': data.get('domain', 'www.amazon.com')
                },
                'product_details': product_details
            }
            
        except Exception as e:
            print(f"❌ Veri işleme hatası: {str(e)}")
            return self._get_sample_comments_data()
    
    def _get_sample_comments_data(self) -> Dict:
        """Örnek yorum verileri (fallback için)"""
        print("📝 Örnek yorum verileri kullanılıyor...")
        
        sample_comments = [
            {
                'date': '2024-01-15',
                'rating': 5.0,
                'comment': 'Harika bir kitap! Çok beğendim.',
                'user': 'Ahmet Y.',
                'title': 'Mükemmel',
                'year': 2024,
                'verified': True,
                'helpful_votes': '5 kişi faydalı buldu',
                'review_link': 'https://amazon.com/review1'
            },
            {
                'date': '2024-02-20',
                'rating': 4.0,
                'comment': 'Güzel kitap, tavsiye ederim.',
                'user': 'Mehmet K.',
                'title': 'İyi',
                'year': 2024,
                'verified': True,
                'helpful_votes': '3 kişi faydalı buldu',
                'review_link': 'https://amazon.com/review2'
            },
            {
                'date': '2023-12-10',
                'rating': 5.0,
                'comment': 'Çok kaliteli bir eser.',
                'user': 'Ayşe L.',
                'title': 'Harika',
                'year': 2023,
                'verified': False,
                'helpful_votes': '2 kişi faydalı buldu',
                'review_link': 'https://amazon.com/review3'
            }
        ]
        
        return {
            'total_comments': len(sample_comments),
            'average_rating': 4.67,
            'source': 'sample_data',
            'timestamp': datetime.now().isoformat(),
            'comments': sample_comments,
            'yearly_ratings': {
                2024: {'total': 9.0, 'count': 2, 'average': 4.5},
                2023: {'total': 5.0, 'count': 1, 'average': 5.0}
            },
            'product_info': {
                'asin': 'SAMPLE123',
                'total_reviews': 3,
                'country': 'US',
                'domain': 'www.amazon.com'
            }
        }
    

    
    def extract_asin_from_url(self, url: str) -> Optional[str]:
        """URL'den ASIN çıkar"""
        try:
            if 'amazon.com' in url:
                # Amazon URL'lerinden ASIN çıkarma
                if '/dp/' in url:
                    asin = url.split('/dp/')[1].split('/')[0]
                    return asin
                elif '/gp/product/' in url:
                    asin = url.split('/gp/product/')[1].split('/')[0]
                    return asin
            return None
        except:
            return None 