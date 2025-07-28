import os
import google.generativeai as genai
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

class GeminiAgentV2:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
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
            seo_prompt = self.create_seo_prompt(best_offer)
            seo_result = await self.call_gemini_api(seo_prompt)
            
            # Satış önerisi üret
            sales_prompt = self.create_sales_prompt(best_offer)
            sales_result = await self.call_gemini_api(sales_prompt)
            
            # Özet oluştur
            summary_prompt = self.create_summary_prompt(best_offer)
            summary_result = await self.call_gemini_api(summary_prompt)
            
            # Satış analizi ve kar hesaplama
            profit_analysis_prompt = self.create_profit_analysis_prompt(search_results, best_offer)
            profit_analysis_result = await self.call_gemini_api(profit_analysis_prompt)
            
            return {
                'analysis': analysis_result,
                'seo_content': seo_result,
                'sales_recommendation': sales_result,
                'best_offer_summary': summary_result,
                'profit_analysis': profit_analysis_result
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
    
    def create_seo_prompt(self, best_offer: Dict) -> str:
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
    
    def create_sales_prompt(self, best_offer: Dict) -> str:
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
    
    def create_summary_prompt(self, best_offer: Dict) -> str:
        """Özet için prompt oluştur"""
        
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
        
        return prompt
    
    def create_profit_analysis_prompt(self, search_results: Dict, best_offer: Dict) -> str:
        """Kar analizi için prompt oluştur"""
        
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
        
        # En ucuz ve en pahalı fiyatları bul
        prices = [r['price'] for r in all_results if r['price'] > 0]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # Kar hesaplama
        best_price = best_offer.get('price', 0)
        commission_rate = 0.21  # %21 komisyon
        shipping_cost = 70  # 70 TL kargo
        profit_margin = 100  # 100 TL kar
        
        # Toplam maliyet
        total_cost = best_price + shipping_cost
        commission_amount = (best_price + profit_margin) * commission_rate
        suggested_selling_price = total_cost + commission_amount + profit_margin
        
        # Kar marjı hesaplama
        profit_percentage = (profit_margin / suggested_selling_price) * 100 if suggested_selling_price > 0 else 0
        
        # Rekabet analizi
        max_competitor_price = max(prices) if prices else 0
        can_compete = suggested_selling_price < max_competitor_price
        
        # Farklı kar marjları ile test
        profit_margins = [50, 75, 100, 125, 150]
        competitive_prices = []
        
        for margin in profit_margins:
            test_commission = (best_price + margin) * commission_rate
            test_selling_price = total_cost + test_commission + margin
            if test_selling_price < max_competitor_price:
                competitive_prices.append({
                    'margin': margin,
                    'selling_price': test_selling_price,
                    'profit': test_selling_price - total_cost
                })
        
        prompt = f"""
Sen bir e-ticaret satış analisti ve kar hesaplama uzmanısın. Aşağıdaki kitap için detaylı satış analizi yap:

KİTAP: {best_offer.get('title', '')}
EN UCUZ FİYAT: {best_offer.get('platform', '')} - {best_price} TL
EN PAHALI FİYAT: {max_price} TL
ORTALAMA FİYAT: {avg_price:.2f} TL

TÜM FİYATLAR:
"""
        
        for i, result in enumerate(all_results, 1):
            prompt += f"{i}. {result['title']} - {result['platform']} - {result['price']} TL\n"
        
        prompt += f"""

KAR HESAPLAMA:
- Alış Fiyatı: {best_price} TL
- Kargo Maliyeti: {shipping_cost} TL
- Toplam Maliyet: {total_cost} TL
- Komisyon Oranı: %{commission_rate * 100}
- Kar Marjı: {profit_margin} TL
- Önerilen Satış Fiyatı: {suggested_selling_price:.2f} TL
- Kar Yüzdesi: %{profit_percentage:.1f}

REKABET ANALİZİ:
- En Pahalı Rakip: {max_price} TL
- Bizim Satış Fiyatımız: {suggested_selling_price:.2f} TL
- Rekabet Edebilir mi: {'EVET' if can_compete else 'HAYIR'}

KAR MARJI SEÇENEKLERİ:
"""
        
        for price_info in competitive_prices:
            prompt += f"- {price_info['margin']} TL kar ile: {price_info['selling_price']:.2f} TL (Net kar: {price_info['profit']:.2f} TL)\n"
        
        prompt += f"""

ANALİZ YAP:
1. Bu kitap satış için uygun mu?
2. Hangi kar marjı ile rekabet edebiliriz?
3. En uygun satış fiyatı nedir?
4. Risk değerlendirmesi nasıl?

DETAYLI RAPOR VER:
- Satış Uygunluğu: [Uygun/Orta/Uygun Değil]
- Kar Analizi: [Yüksek/Orta/Düşük]
- Rekabet Durumu: [Açıklama]
- Önerilen Fiyat: [Fiyat] TL
- Satış Stratejisi: [Açıklama]
- Risk Değerlendirmesi: [Açıklama]

Türkçe olarak detaylı analiz yaz.
"""
        
        return prompt
    
    async def call_gemini_api(self, prompt: str) -> str:
        """Gemini API'yi çağır"""
        try:
            print(f"🔍 Gemini API çağrılıyor...")
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text
            else:
                print(f"❌ Gemini API boş sonuç")
                return "API boş sonuç döndü"
                    
        except Exception as e:
            print(f"❌ Gemini API çağrı hatası: {str(e)}")
            return f"API çağrısı başarısız: {str(e)}"
    
    def get_fallback_content(self, best_offer: Dict) -> Dict:
        """Fallback içerik"""
        # Kar hesaplama
        best_price = best_offer.get('price', 0)
        commission_rate = 0.21
        shipping_cost = 70
        profit_margin = 100
        total_cost = best_price + shipping_cost
        commission_amount = (best_price + profit_margin) * commission_rate
        suggested_selling_price = total_cost + commission_amount + profit_margin
        
        return {
            'analysis': f"{best_offer.get('title', '')} kitabı analiz edildi. Fiyat aralığı {best_offer.get('price', 0)} TL civarında ve {best_offer.get('platform', '')} platformunda en uygun fiyatla bulunabilir.",
            'seo_content': f"SEO içeriği: {best_offer.get('title', '')} - {best_offer.get('price', 0)} TL fiyatla {best_offer.get('platform', '')} platformunda satışta. Kitap severler için ideal fiyat ve kalite.",
            'sales_recommendation': f"Satış önerisi: {best_offer.get('platform', '')} platformunda {best_offer.get('price', 0)} TL fiyatla satabilirsiniz. Hedef kitle kitap severler ve öğrenciler.",
            'best_offer_summary': f"{best_offer.get('title', '')} kitabı {best_offer.get('platform', '')} platformunda {best_offer.get('price', 0)} TL fiyatla bulunabilir. Bu fiyatla satış yapabilirsiniz.",
            'profit_analysis': f"Kar Analizi: {best_offer.get('title', '')} kitabı {best_price} TL'ye alınıp {suggested_selling_price:.2f} TL'ye satılabilir. %21 komisyon, 70 TL kargo ve 100 TL kar ile toplam {suggested_selling_price - total_cost:.2f} TL net kar elde edilir."
        } 