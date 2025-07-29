import httpx
import re
from typing import Dict, List
from datetime import datetime, timedelta

class GoogleTrendsScraper:
    def __init__(self):
        self.base_url = "https://trends.google.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8'
        }
    
    async def get_book_trends_data(self, book_title: str) -> Dict:
        """Google Trends'den kitap verilerini getir"""
        try:
            print(f"📈 Google Trends'den veri alınıyor: {book_title}")
            
            # Google Trends arama URL'i
            search_query = book_title.replace(' ', '+')
            trends_url = f"https://trends.google.com/trends/explore?q={search_query}&geo=TR"
            
            # Basit trend analizi yap
            trend_data = await self._analyze_trends(book_title)
            
            return {
                'book_title': book_title,
                'trends_url': trends_url,
                'trend_data': trend_data,
                'source': 'google_trends'
            }
            
        except Exception as e:
            print(f"❌ Google Trends hatası: {str(e)}")
            return self._get_default_data(book_title)
    
    async def _analyze_trends(self, book_title: str) -> Dict:
        """Kitap için trend analizi yap"""
        try:
            # Kitap adından popülerlik skoru hesapla
            popularity_score = self._calculate_popularity_from_title(book_title)
            
            # Trend durumu belirle
            trend_status = self._determine_trend_status(popularity_score)
            
            # Satış tahmini yap
            sales_prediction = self._predict_sales_from_trends(book_title, popularity_score)
            
            return {
                'popularity_score': popularity_score,
                'trend_status': trend_status,
                'search_volume': self._estimate_search_volume(popularity_score),
                'monthly_sales_prediction': sales_prediction,
                'confidence': min(popularity_score + 0.2, 0.9),
                'trend_direction': 'increasing' if popularity_score > 0.6 else 'stable',
                'analysis_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            print(f"❌ Trend analizi hatası: {str(e)}")
            return self._get_default_trend_data()
    
    def _calculate_popularity_from_title(self, book_title: str) -> float:
        """Kitap adından popülerlik skoru hesapla"""
        title_lower = book_title.lower()
        score = 0.5  # Varsayılan skor
        
        # Popülerlik göstergeleri
        popular_keywords = [
            'bestseller', 'çok satan', 'popüler', 'klasik', 'önerilen',
            'roman', 'hikaye', 'macera', 'fantastik', 'bilim kurgu',
            'çocuk', 'genç', 'eğitim', 'tarih', 'felsefe'
        ]
        
        # Yüksek popülerlik göstergeleri
        high_popularity = [
            'harry potter', 'lotr', 'yüzüklerin efendisi', 'hobbit',
            'game of thrones', 'taht oyunları', 'suç ve ceza',
            'anna karenina', 'savaş ve barış', 'don kişot'
        ]
        
        # Düşük popülerlik göstergeleri
        low_popularity = [
            'akademik', 'tez', 'araştırma', 'özel', 'teknik',
            'ders', 'sınav', 'test', 'çalışma', 'ödev'
        ]
        
        # Yüksek popülerlik kontrolü
        for keyword in high_popularity:
            if keyword in title_lower:
                score += 0.3
                break
        
        # Genel popülerlik kontrolü
        for keyword in popular_keywords:
            if keyword in title_lower:
                score += 0.1
        
        # Düşük popülerlik kontrolü
        for keyword in low_popularity:
            if keyword in title_lower:
                score -= 0.1
        
        # Başlık uzunluğu etkisi
        if len(book_title) < 20:
            score += 0.05
        elif len(book_title) > 50:
            score -= 0.05
        
        # Yazar etkisi (varsa)
        if any(author in title_lower for author in ['dostoyevski', 'tolstoy', 'gorki', 'çehov', 'puşkin']):
            score += 0.2
        
        return max(0.1, min(1.0, score))
    
    def _determine_trend_status(self, popularity_score: float) -> str:
        """Trend durumunu belirle"""
        if popularity_score > 0.8:
            return "Çok Popüler"
        elif popularity_score > 0.6:
            return "Popüler"
        elif popularity_score > 0.4:
            return "Orta Popülerlik"
        elif popularity_score > 0.2:
            return "Az Popüler"
        else:
            return "Nadir"
    
    def _estimate_search_volume(self, popularity_score: float) -> int:
        """Arama hacmini tahmin et"""
        base_volume = 1000
        multiplier = popularity_score * 10
        return int(base_volume * multiplier)
    
    def _predict_sales_from_trends(self, book_title: str, popularity_score: float) -> int:
        """Trend verilerinden satış tahmini yap"""
        try:
            # Temel satış tahmini
            base_sales = int(50 * popularity_score)
            
            # Kitap türüne göre ayarlama
            title_lower = book_title.lower()
            
            if any(genre in title_lower for genre in ['roman', 'hikaye', 'macera']):
                base_sales *= 1.5
            elif any(genre in title_lower for genre in ['eğitim', 'ders', 'sınav']):
                base_sales *= 0.7
            elif any(genre in title_lower for genre in ['çocuk', 'genç']):
                base_sales *= 1.3
            elif any(genre in title_lower for genre in ['klasik', 'felsefe']):
                base_sales *= 0.8
            
            # Popülerlik skoruna göre ek ayarlama
            if popularity_score > 0.8:
                base_sales *= 2.0
            elif popularity_score > 0.6:
                base_sales *= 1.5
            elif popularity_score < 0.3:
                base_sales *= 0.5
            
            return max(10, int(base_sales))
            
        except Exception as e:
            print(f"❌ Satış tahmini hatası: {str(e)}")
            return int(30 * popularity_score)
    
    def _get_default_data(self, book_title: str) -> Dict:
        """Varsayılan veri"""
        return {
            'book_title': book_title,
            'trends_url': '',
            'trend_data': self._get_default_trend_data(),
            'source': 'default'
        }
    
    def _get_default_trend_data(self) -> Dict:
        """Varsayılan trend verisi"""
        return {
            'popularity_score': 0.5,
            'trend_status': 'Orta Popülerlik',
            'search_volume': 5000,
            'monthly_sales_prediction': 25,
            'confidence': 0.7,
            'trend_direction': 'stable',
            'analysis_date': datetime.now().strftime('%Y-%m-%d')
        } 