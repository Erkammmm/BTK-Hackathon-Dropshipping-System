# 📚 BTK Kitap Fiyat Karşılaştırma ve Analiz Sistemi v5.0

## 🎯 Proje Hakkında

Bu proje, kitap arama ve analiz sistemi olup, **Gerçek Veriler**, **Machine Learning** ve **Gelişmiş Excel Raporlama** özellikleri ile donatılmıştır. Sistem, Google Shopping'den fiyat karşılaştırması yapar, Amazon'dan gerçek satış verilerini çeker, Gemini AI ile detaylı analiz üretir ve gelişmiş Excel raporları oluşturur.

## ✨ Versiyon 5.0 Yeni Özellikler

### 🚀 MAJOR OPTIMIZASYONLAR
- **✅ Amazon API Entegrasyonu** - Gerçek satış verileri ve yorumlar
- **✅ Real Machine Learning** - Gerçek veriler
- **✅ Dinamik Trend Analizi** - ML ile 6 aylık satış tahmini
- **✅ Sentiment Analizi** - Amazon yorumlarından duygu analizi
- **✅ Otomatik Ürün Açıklaması** - Gemini AI ile kullanıcı bazlı açıklama
- **✅ Zaman Serisi Analizi** - Yıllık yorum trend analizi
- **🆕 Dropshipping Analizi** - Yerel dropshipping potansiyeli analizi

### 🤖 Machine Learning Özellikleri
- **Amazon Real Data** ile satış tahmini (Gerçek veriler)
- **Sales Volume** analizi (Amazon Product Details API)
- **Rating Distribution** analizi (Amazon yorumları)
- **Dinamik Güven Skoru** (Amazon verilerine dayalı)
- **ML Trend Analizi** (6 aylık dinamik tahmin)
- **Popülerlik skoru** hesaplama (Amazon ratings'den)
- **Kategori bazlı analiz** (Roman, Eğitim, Çocuk vs.)

### 📊 Gelişmiş Excel Raporlama
- **7 farklı sayfa**: Özet, Fiyat Grafikleri, Kâr Analizi, Satış Tahmini, Detaylı Analiz, Amazon Yorum Analizi, **Sonuç**
- **Amazon Satış Verileri**: Gerçek satış tahminleri ve rekabet analizi
- **Sentiment Analizi**: Yorumlardan duygu analizi (%75 pozitif gibi)
- **Zaman Serisi Analizi**: Yıllık yorum trend analizi
- **Otomatik Ürün Açıklaması**: Kullanıcı yorumlarından üretilen açıklama
- **Dropshipping Analizi**: Yerel dropshipping potansiyeli ve kar analizi
- **Tablo formatında detaylı analiz**: 3 sütunlu profesyonel görünüm
- **Renkli tasarım**: Mavi, sarı, yeşil, turuncu, mor renkler
- **Metin kaydırma**: Uzun yazılar otomatik alt satıra geçiyor
- **Grafikler**: Bar chart, line chart, pie chart

### 🔧 API Entegrasyonları
- **Google Shopping** (SerpAPI) - Fiyat karşılaştırması
- **Amazon Real-Time Data API** (RapidAPI) - Gerçek satış verileri, ürün bilgileri, yorumlar ve satıcı bilgileri
- **Google Gemini AI** - Detaylı analiz, sentiment analizi, otomatik açıklama ve dropshipping analizi
- **Google Trends** - Popülerlik analizi

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.10+
- Docker (opsiyonel)
- API Anahtarları

### Kurulum

1. **Repository'yi klonlayın**
```bash
git clone https://github.com/your-username/BTK-HACKTHON-ETİCARET.git
cd BTK-HACKTHON-ETİCARET
```

2. **Environment dosyasını oluşturun**
```bash
cp env.example .env
```

3. **API anahtarlarını ekleyin**
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERP_API_KEY=your_serp_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
```

4. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

5. **Uygulamayı başlatın**
```bash
python -m uvicorn app.main:app --reload
```

### Docker ile Kurulum

```bash
# Docker Compose ile başlat
docker-compose up --build

# Veya sadece Docker ile
docker build -t btk-kitap-analizi .
docker run -p 8000:8000 --env-file .env btk-kitap-analizi
```

## 📖 Kullanım

### Web Arayüzü
- **Ana Sayfa**: `http://localhost:8000`
- **API Dokümantasyonu**: `http://localhost:8000/docs`

### API Endpoints

#### 🔍 Temel Analiz
```http
POST /search-book
Content-Type: application/json

{
  "book_name": "Beyaz Geceler"
}
```

#### 🚀 Gelişmiş Analiz (ML + Grafikler)
```http
POST /search-book-advanced
Content-Type: application/json

{
  "book_name": "Beyaz Geceler"
}
```

### Örnek Kullanım

```python
import requests

# Gelişmiş analiz
response = requests.post(
    "http://localhost:8000/search-book-advanced",
    json={"book_name": "Beyaz Geceler"}
)

result = response.json()
print(f"Excel Raporu: {result['excel_report']}")
print(f"ML Tahmini: {result['sales_prediction']}")
```

## 📊 Excel Rapor Yapısı

### 📋 Özet Sayfası
- Kitap bilgileri
- **Amazon Real Data** ML satış tahminleri
- **Amazon Ratings** popülerlik skoru
- **Amazon Sales Volume** güven skoru
- **Gerçek satış verileri** aylık gelir tahmini
- **Amazon Satış Verileri** bölümü (Toplam değerlendirme, stok durumu, satıcı sayısı)

### 📈 Fiyat Grafikleri
- Platform fiyat karşılaştırması
- Bar chart grafikleri
- En uygun fiyat vurgusu

### 💰 Kâr Analizi
- Kâr marjı hesaplamaları
- %14 komisyon analizi
- Net kâr tahmini

### 🎯 Satış Tahmini
- **Amazon Real Data** ML model sonuçları
- **Dinamik Trend Analizi** (ML ile 6 aylık tahmin)
- **Mevsimsellik Faktörü** (yaz aylarında artış)
- **Popülerlik Bazlı Ayarlama** (±10% dinamik)
- **Güven Skoru Bazlı Trend** (yüksek güven = yavaş düşüş)
- Günlük ortalama satış

### 📝 Detaylı Analiz
- **Tablo formatında** Gemini AI analizleri
- SEO içeriği
- Satış önerileri
- Kâr analizi detayları

### 🆕 Amazon Yorum Analizi
- **Sentiment Analizi**: Yorumlardan duygu analizi (%75 pozitif gibi)
- **Zaman Serisi Analizi**: Yıllık yorum trend analizi (2021: 4.8, 2023: 3.9)
- **Otomatik Ürün Açıklaması**: Kullanıcı yorumlarından üretilen açıklama
- **Detaylı Yorum Tablosu**: 100+ Amazon yorumu (tarih, kullanıcı, yıldız, başlık, yorum)
- **Yıldız Bazlı Renk Kodlaması**: Yeşil (4+), Sarı (3+), Kırmızı (<3)

### 🆕 Sonuç Sayfası (Dropshipping Analizi)
- **Fiyat Analizi**: En ucuz ve en pahalı fiyat karşılaştırması
- **Dropshipping Hesaplaması**: %14 komisyon + 100 TL kar marjı ile önerilen satış fiyatı
- **Kar Analizi**: Gemini AI ile detaylı kar potansiyeli analizi
- **Trendyol Satış Önerisi**: Fiyat uygunluğuna göre satış önerisi veya risk uyarısı
- **Detaylı Fiyat Tablosu**: Platform bazlı dropshipping potansiyeli
- **Gemini AI Analizi**: Yerel dropshipping stratejisi ve öneriler

## Tüm analizde Gemine API kullanılmıştır.

## 🛠️ Kullanılan Teknolojiler

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **httpx** - Async HTTP client

### Machine Learning
- **Scikit-learn** - ML algorithms
- **Random Forest** - Sales prediction
- **NumPy** - Numerical operations
- **Pandas** - Data manipulation

### Excel & Grafikler
- **OpenPyXL** - Excel file generation
- **Matplotlib** - Plotting library
- **Seaborn** - Statistical visualization

### AI & APIs
- **Google Gemini AI** - Content generation, sentiment analysis, automatic description, dropshipping analysis
- **Amazon Real-Time Data API** - Product details, reviews, offers
- **SerpAPI** - Google Shopping data
- **Google Trends** - Popularity analysis


## 📁 Proje Yapısı

```
BTK-HACKTHON-ETİCARET/
├── app/
│   ├── main.py                 # FastAPI uygulaması
│   ├── serp_agent.py          # Google Shopping API
│   ├── gemini_agent_v2.py     # Gemini AI entegrasyonu (v2)
│   ├── amazon_comments_api.py # Amazon API entegrasyonu
│   ├── google_trends_scraper.py # Google Trends analizi
│   ├── advanced_excel_generator.py # Excel rapor oluşturucu
│   ├── schemas.py             # Pydantic modelleri
│   └── config.py              # Konfigürasyon
├── reports/                   # Excel raporları
├── requirements.txt           # Python bağımlılıkları
├── Dockerfile                 # Docker konfigürasyonu
├── docker-compose.yml         # Docker Compose
├── env.example               # Environment örneği
└── README.md                 # Bu dosya
```

## 🔧 Konfigürasyon

### Environment Variables
```env
# Gerekli API Anahtarları
GEMINI_API_KEY=your_gemini_api_key_here
SERP_API_KEY=your_serp_api_key_here
RAPIDAPI_KEY=your_rapidapi_key_here
```

### API Anahtarı Alma

#### 🔑 Gemini AI
1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. API key oluşturun
3. `.env` dosyasına ekleyin

#### 🔑 SerpAPI
1. [SerpAPI](https://serpapi.com/) adresine gidin
2. Ücretsiz hesap oluşturun
3. API key alın

#### 🔑 RapidAPI
1. [RapidAPI](https://rapidapi.com/) adresine gidin
2. Amazon Data API'sine abone olun
3. API key alın

## 📈 ML Model Detayları

### Amazon Real Data Satış Tahmini
```python
# Amazon Product Details API'den gelen veriler
sales_volume = product_details.get('sales_volume')  # "1000+ sold"
total_ratings = product_details.get('product_num_ratings')  # 751
is_best_seller = product_details.get('is_best_seller')  # True/False

# Dinamik tahmin algoritması
if sales_volume:
    estimated_sales = extract_number_from_sales_volume(sales_volume)
elif total_ratings > 1000:
    estimated_sales = 500
elif total_ratings > 500:
    estimated_sales = 300
elif is_best_seller:
    estimated_sales = 1000
```

### Dinamik Trend Analizi
```python
# ML ile 6 aylık trend hesaplama
confidence = sales_prediction.get('confidence', 0.7)
popularity = sales_prediction.get('popularity_score', 0.5)

# Güven skoruna göre trend faktörleri
if confidence > 0.8:
    factors = [1.0, 0.95, 0.90, 0.85, 0.80, 0.75]  # Yavaş düşüş
elif confidence > 0.6:
    factors = [1.0, 0.90, 0.80, 0.70, 0.60, 0.50]  # Orta düşüş
else:
    factors = [1.0, 0.85, 0.70, 0.55, 0.40, 0.25]  # Hızlı düşüş

# Mevsimsellik + Popülerlik ayarlaması
seasonal_factors = [1.0, 1.1, 1.2, 1.0, 0.9, 0.8]  # Yaz artışı
```

### Popülerlik Skoru Hesaplama (Amazon'dan)
- **Total Ratings**: 751 rating = yüksek popülerlik
- **Rating Distribution**: 5 yıldız oranı
- **Best Seller**: Amazon best seller durumu
- **Amazon Choice**: Amazon choice durumu

## 🚀 Deployment

### Docker ile Production
```bash
# Production build
docker build -t btk-kitap-analizi:latest .

# Production run
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name btk-kitap-analizi \
  btk-kitap-analizi:latest
```

### Docker Compose ile Production
```bash
# Production mode
docker-compose -f docker-compose.yml up -d
```

## 💡 Yerel Dropshipping Kavramı

Bu proje, **yerel dropshipping** stratejisini analiz eder. Yerel dropshipping, geleneksel dropshipping'in yerel bir versiyonudur:

### 🔄 Nasıl Çalışır?
1. **Satış Öncesi**: Ürünü stokta tutmazsınız
2. **Satış Sonrası**: Müşteri sipariş verdiğinde, en ucuz platformdan ürünü alırsınız
3. **Kar Marjı**: Alış fiyatı + komisyon + kar marjı = satış fiyatınız
4. **Rekabet**: Satış fiyatınız rakiplerden düşük olmalı

### 📊 Analiz Kriterleri
- **En Ucuz Fiyat**: Hangi platformdan alınacağı
- **Komisyon Oranı**: %14 (Trendyol komisyonu)
- **Kar Marjı**: 100 TL sabit kar(veya kendinize göre ayarlayabilirsiniz)
- **Rekabet Analizi**: Diğer platformlardaki fiyatlarla karşılaştırma

### ✅ Avantajları
- **Düşük Risk**: Stok maliyeti yok
- **Yüksek Esneklik**: Fiyat değişimlerine hızlı adaptasyon
- **Kolay Başlangıç**: Düşük sermaye gereksinimi

## 📞 İletişim

- **Proje Sahibi**: Erkam ÇETKİN
- **Email**: cetkinerkam17@gmail.com

---

**Versiyon**: 5.0.0  
**Son Güncelleme**: 2025  
**Python Versiyonu**: 3.10+  
**Docker**: Destekleniyor  
**Amazon API**: Entegre edildi  
**Real ML Data**: Aktif  
**Dropshipping Analizi**: Yeni Özellik
