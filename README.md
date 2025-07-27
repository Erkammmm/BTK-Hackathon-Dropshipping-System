# 🚀 BTK Hackathon - Otomatik Dropshipping Sistemi

## 📖 Proje Amacı
Bu proje, BTK Hackathon yarışması için geliştirilmiş **tam otomatik yerel dropshipping sistemi**dir. Kullanıcıdan alınan kitap ismine göre:

1. **Cimri'den en uygun fiyatı bulur**
2. **Gemini API ile SEO dostu başlık ve açıklama üretir**
3. **Otomatik fiyatlandırma yapar** (%21 komisyon + 70 TL kargo + 100 TL kar)
4. **Excel dosyasına yazar**
5. **Trendyol'a otomatik yükler** (API + Selenium + Sürükle-bırak)

## 🛠️ Teknolojiler

### Backend
- **FastAPI** - Modern web framework
- **Python 3.10+** - Ana programlama dili
- **Uvicorn** - ASGI server

### Web Scraping & Automation
- **httpx** - Asenkron HTTP client
- **BeautifulSoup4** - HTML parsing
- **Selenium** - Web automation
- **PyAutoGUI** - Mouse/keyboard automation

### AI & Content Generation
- **Google Gemini API** - SEO dostu içerik üretimi
- **Natural Language Processing** - Akıllı başlık ve açıklama

### Data Management
- **openpyxl** - Excel dosya işlemleri
- **Pydantic** - Data validation
- **python-dotenv** - Environment variables

### Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container setup

## 🚀 Kurulum

### 1. Repository'yi Klonla
```bash
git clone https://github.com/your-username/btk-hackathon-dropshipping.git
cd btk-hackathon-dropshipping
```

### 2. Environment Variables
`.env` dosyası oluşturun:
```env
GEMINI_API_KEY=your_gemini_api_key_here
TRENDYOL_API_KEY=your_trendyol_api_key_here
TRENDYOL_SUPPLIER_ID=your_supplier_id_here
TRENDYOL_EMAIL=your_trendyol_email@example.com
TRENDYOL_PASSWORD=your_trendyol_password_here
```

### 3. Dependencies Yükle
```bash
pip install -r requirements.txt
```

### 4. Chrome Tarayıcısı
- Google Chrome yüklü olmalı
- Selenium otomatik olarak ChromeDriver'ı indirecek

## 🎯 Kullanım

### Docker ile Çalıştırma
```bash
# Build image
docker build -t btk-dropshipping .

# Run container
docker run -p 8000:8000 btk-dropshipping
```

### Local Çalıştırma
```bash
# FastAPI server başlat
python -m uvicorn app.main:app --reload

# API docs: http://localhost:8000/docs
```

### API Endpoint
```bash
POST /add-book
Content-Type: application/json

{
  "book_name": "satranç"
}
```

## 📊 Sistem Mimarisi

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │───▶│   FastAPI       │───▶│   Cimri Scraper │
│   (Book Name)   │    │   Endpoint      │    │   (Price Fetch) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Excel Writer  │◀───│   Price Calc    │◀───│   Gemini API    │
│   (Product Add) │    │   (Commission)  │    │   (SEO Content) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Trendyol API  │◀───│   Auto Upload   │◀───│   Selenium Bot  │
│   (Direct API)  │    │   (Multi-Method)│    │   (Browser Auto)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Özellikler

### 🤖 Otomatik Fiyatlandırma
- **Base Price**: Cimri'den çekilen fiyat
- **Commission**: %21 komisyon
- **Shipping**: 70 TL kargo
- **Profit**: 100 TL kar
- **Market Price**: Trendyol fiyatından 50-100 TL yüksek

### 📝 Akıllı İçerik Üretimi
- **SEO Optimized Titles**: Gemini API ile üretilen başlıklar
- **Rich Descriptions**: 3-4 paragraf detaylı açıklama
- **Keyword Integration**: "kitap", "okuma", "edebiyat" anahtar kelimeleri

### 🔄 Çoklu Yükleme Yöntemi
1. **Trendyol API** (Direkt)
2. **Selenium Automation** (Browser)
3. **Drag & Drop** (File upload)
4. **Manual Instructions** (Fallback)

### 📊 Excel Entegrasyonu
- **Roman_27_07_2025-21_23.xlsx** formatı
- **30+ field mapping**
- **Automatic barcode generation**
- **Dynamic stock quantities**

## 🎯 API Response Örneği

```json
{
  "book_info": {
    "title": "satranç",
    "price": 35.62,
    "url": "https://www.kitapyurdu.com/kitap/satranç",
    "image_url": "https://img.kitapyurdu.com/v1/getImage/fn:999999/wi:60/wh:true",
    "author": "Bilinmeyen Yazar"
  },
  "base_price": 35.62,
  "market_price": 283.25,
  "trendyol_price": 213.1,
  "gemini_result": {
    "title": "satranç Kitap",
    "description": "SEO dostu açıklama..."
  },
  "trendyol_result": {
    "status": "success",
    "message": "Ürün Excel dosyasına eklendi. Otomatik yükleme başarılı!"
  }
}
```

## 🚀 Deployment

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - TRENDYOL_API_KEY=${TRENDYOL_API_KEY}
      - TRENDYOL_SUPPLIER_ID=${TRENDYOL_SUPPLIER_ID}
```

### Production
```bash
# Build production image
docker build -t btk-dropshipping:prod .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  btk-dropshipping:prod
```

## 📁 Proje Yapısı

```
BTK-HACKTHON-ETİCARET/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI ana uygulama
│   ├── fetch_price.py       # Cimri scraping
│   ├── gemini_agent.py      # AI içerik üretimi
│   ├── trendyol_api.py      # Trendyol entegrasyonu
│   ├── auto_upload.py       # Selenium automation
│   ├── schemas.py           # Pydantic modelleri
│   ├── config.py            # Konfigürasyon
│   └── utils.py             # Yardımcı fonksiyonlar
├── Roman_27_07_2025-21_23.xlsx  # Excel template
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image
├── docker-compose.yml      # Multi-container setup
├── .env                    # Environment variables (gitignore)
├── .gitignore             # Git ignore rules
└── README.md              # Proje dokümantasyonu
```

## 🎯 Yarışma Özellikleri

### 🏆 BTK Hackathon Uyumluluğu
- **Innovation**: AI-powered dropshipping automation
- **Technology**: Modern Python stack (FastAPI, Selenium, Gemini)
- **Scalability**: Docker containerization
- **Documentation**: Comprehensive README and API docs
- **Code Quality**: Clean architecture, error handling, logging

### 🤖 AI Integration
- **Gemini API**: Natural language processing
- **SEO Optimization**: Automated content generation
- **Smart Pricing**: Dynamic commission calculation
- **Agent System**: Natural language commands

### 🔄 Automation Features
- **Web Scraping**: Cimri price discovery
- **Browser Automation**: Selenium integration
- **File Management**: Excel operations
- **API Integration**: Multi-platform support

## 📞 İletişim

- **Developer**: [Your Name]
- **Project**: BTK Hackathon - Otomatik Dropshipping
- **Year**: 2025

## 📄 Lisans

Bu proje BTK Hackathon yarışması için geliştirilmiştir.

---

⭐ **Star this repository if you find it useful!** 