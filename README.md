# 📚 BTK Kitap Fiyat Karşılaştırma ve Analiz Sistemi v3.0

## 🎯 Proje Hakkında

Bu proje, kitap arama ve analiz sistemi olup, **Machine Learning** ve **Gelişmiş Excel Raporlama** özellikleri ile donatılmıştır. Sistem, Google Shopping'den fiyat karşılaştırması yapar, Gemini AI ile detaylı analiz üretir ve gelişmiş Excel raporları oluşturur.

## ✨ Versiyon 3.0 Yeni Özellikler

### 🤖 Machine Learning Özellikleri
- **Random Forest Regressor** ile satış tahmini
- **Popülerlik skoru** hesaplama (kitap adından)
- **Kategori bazlı analiz** (Roman, Eğitim, Çocuk vs.)
- **Güven skoru** hesaplama
- **Aylık satış tahmini** ve gelir hesaplama

### 📊 Gelişmiş Excel Raporlama
- **5 farklı sayfa**: Özet, Fiyat Grafikleri, Kâr Analizi, Satış Tahmini, Detaylı Analiz
- **Tablo formatında detaylı analiz**: 3 sütunlu profesyonel görünüm
- **Renkli tasarım**: Mavi, sarı, yeşil, turuncu renkler
- **Metin kaydırma**: Uzun yazılar otomatik alt satıra geçiyor
- **Grafikler**: Bar chart, line chart, pie chart

### 🔧 API Entegrasyonları
- **Google Shopping** (SerpAPI) - Fiyat karşılaştırması
- **Google Gemini AI** - Detaylı analiz ve SEO içeriği
- **Google Trends** - Popülerlik analizi
- **Türk E-ticaret API** - Hazır (gelecekte kullanılacak)

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
- ML satış tahminleri
- Popülerlik skoru
- Güven skoru
- Aylık gelir tahmini

### 📈 Fiyat Grafikleri
- Platform fiyat karşılaştırması
- Bar chart grafikleri
- En uygun fiyat vurgusu

### 💰 Kâr Analizi
- Kâr marjı hesaplamaları
- Trendyol komisyon analizi
- Kargo maliyeti hesaplama
- Net kâr tahmini

### 🎯 Satış Tahmini
- ML model sonuçları
- Kategori bazlı analiz
- Trend analizi
- Günlük ortalama satış

### 📝 Detaylı Analiz
- **Tablo formatında** Gemini AI analizleri
- SEO içeriği
- Satış önerileri
- Kâr analizi detayları

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
- **Google Gemini AI** - Content generation
- **SerpAPI** - Google Shopping data
- **Google Trends** - Popularity analysis

### Web Scraping
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Browser automation

## 📁 Proje Yapısı

```
BTK-HACKTHON-ETİCARET/
├── app/
│   ├── main.py                 # FastAPI uygulaması
│   ├── serp_agent.py          # Google Shopping API
│   ├── gemini_agent.py        # Gemini AI entegrasyonu
│   ├── google_trends_scraper.py # Google Trends analizi
│   ├── turkish_ecommerce_api.py # Türk E-ticaret API
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
2. Türk E-ticaret API'sine abone olun
3. API key alın

## 📈 ML Model Detayları

### Satış Tahmini Algoritması
```python
# Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Özellikler
features = ['price', 'popularity_score', 'category']

# Tahmin
predicted_sales = model.predict([[price, popularity, category]])
```

### Popülerlik Skoru Hesaplama
- Kitap adından anahtar kelime analizi
- Yazar popülerliği
- Kategori etkisi
- Başlık uzunluğu

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

## 📊 Performans

### API Response Times
- **Google Shopping**: ~2-3 saniye
- **Gemini AI**: ~5-8 saniye
- **Excel Generation**: ~3-5 saniye
- **ML Prediction**: ~1-2 saniye

### Memory Usage
- **Base**: ~150MB
- **With Chrome (Selenium)**: ~300MB
- **With ML Models**: ~200MB

## 🔮 Gelecek Planları (v4.0)

### 🎯 Öncelikli Özellikler
- [ ] **RapidAPI entegrasyonu** (gerçek satış verileri)
- [ ] **Trendyol satış verileri** (web scraping)
- [ ] **Daha gelişmiş ML modelleri** (LSTM, XGBoost)
- [ ] **Real-time veri güncelleme**
- [ ] **Dashboard arayüzü**

### 🚀 Gelişmiş Özellikler
- [ ] **Çoklu dil desteği**
- [ ] **Mobil uygulama**
- [ ] **Email raporları**
- [ ] **Webhook entegrasyonları**
- [ ] **Cache sistemi**

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

- **Proje Sahibi**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [@your-username]

## 🙏 Teşekkürler

- **BTK** - Hackathon organizasyonu
- **Google** - Gemini AI ve SerpAPI
- **Open Source Community** - Kullanılan kütüphaneler

---

**Versiyon**: 3.0.0  
**Son Güncelleme**: 2024  
**Python Versiyonu**: 3.10+  
**Docker**: Destekleniyor
