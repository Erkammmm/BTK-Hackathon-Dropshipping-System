# 🔍 Akıllı Kitap Fiyat Karşılaştırma ve Satış Analizi API

Bu proje, kitap adını girdiğinizde Google Shopping üzerinden tüm e-ticaret sitelerinde arama yaparak en uygun fiyatlı kitabı bulan, Gemini AI ile detaylı analiz yapan ve Excel raporu oluşturan gelişmiş bir FastAPI uygulamasıdır.

## 🎯 Özellikler

### 🔍 Akıllı Arama
- **🌐 Google Shopping Entegrasyonu**: SerpAPI ile gerçek zamanlı fiyat arama
- **💰 En İyi Fiyat Bulma**: Tüm platformlardan en düşük fiyatlı seçeneği otomatik seçme
- **📊 Fiyat Karşılaştırma**: Detaylı platform bazlı fiyat analizi
- **🔗 URL Yönetimi**: Eksik URL'leri otomatik oluşturma

### 🧠 Gelişmiş AI Analizi
- **📝 Kitap Analizi**: Popülerlik, talep durumu, hedef kitle analizi
- **🔍 SEO İçeriği**: Başlık, meta açıklama, ürün açıklaması üretimi
- **💰 Satış Önerileri**: Platform önerileri ve satış stratejileri
- **📈 Kar Analizi**: Otomatik kar hesaplama ve rekabet analizi

### 📊 Excel Raporlama
- **📋 Özet Sayfası**: Kitap bilgileri ve satış uygunluğu
- **📈 Fiyat Karşılaştırma**: Tüm platformların fiyat tablosu
- **💰 Kar Analizi**: Detaylı maliyet ve kar hesaplamaları
- **📝 Detaylı Analiz**: Gemini AI analizlerinin tam metni

### 🎯 Satış Optimizasyonu
- **💡 Rekabet Analizi**: En pahalı rakip fiyatı ile karşılaştırma
- **📊 Kar Marjı Testi**: 50-150 TL arası farklı kar marjları
- **⚡ Satış Uygunluğu**: Otomatik satış önerisi
- **🎯 Optimal Fiyat**: Rekabetçi fiyat önerisi

## 🛠️ Kullanılan Teknolojiler

### Backend Framework
- **FastAPI**: Modern, hızlı web framework
- **Python 3.10+**: Güncel Python sürümü
- **Uvicorn**: ASGI server

### AI ve Machine Learning
- **Google Gemini AI**: Doğal dil işleme ve içerik üretimi
- **Google Generative AI**: Python kütüphanesi

### Web Scraping ve API
- **SerpAPI**: Google Shopping arama API'si
- **httpx**: Asenkron HTTP client
- **BeautifulSoup4**: HTML parsing (geçmiş versiyonlarda)

### Veri İşleme ve Raporlama
- **Pandas**: Veri analizi ve manipülasyon
- **OpenPyXL**: Excel dosya oluşturma ve düzenleme
- **Pydantic**: Veri validasyonu ve serialization

### Frontend
- **HTML5**: Modern web standartları
- **CSS3**: Responsive tasarım
- **JavaScript**: Dinamik kullanıcı etkileşimi

### Environment ve Konfigürasyon
- **python-dotenv**: Environment variables yönetimi
- **Docker**: Containerization (opsiyonel)

## 📦 Kurulum

### 1. Projeyi Klonlayın
```bash
git clone <repository-url>
cd BTK-HACKTHON-ETİCARET
```

### 2. Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Environment Variables Ayarlayın
`env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp env.example .env
```

`.env` dosyasını düzenleyin:
```env
# Gemini AI API Key (Google AI Studio'dan alın)
GEMINI_API_KEY=your_gemini_api_key_here

# SerpAPI Key (https://serpapi.com/ adresinden alın)
SERP_API_KEY=your_serp_api_key_here
```

### 4. Uygulamayı Çalıştırın
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 API Endpoints

### Ana Sayfa
- `GET /` - Web arayüzü

### Kitap Arama ve Analiz
- `POST /search-book` - Kitap ara, analiz et ve Excel raporu oluştur

### API Dokümantasyonu
- `GET /docs` - Swagger UI dokümantasyonu
- `GET /redoc` - ReDoc dokümantasyonu

## 📖 Kullanım

### Web Arayüzü
1. Tarayıcınızda `http://localhost:8000` adresine gidin
2. Kitap adını girin (örn: "Beyaz Geceler")
3. "🔍 Kitap Ara" butonuna tıklayın
4. Detaylı analizi ve Excel raporunu görün

### API Kullanımı
```bash
# Kitap ara ve analiz et
curl -X POST "http://localhost:8000/search-book" \
     -H "Content-Type: application/json" \
     -d '{"book_name": "Beyaz Geceler"}'
```

## 🔧 API Key Alma

### Gemini AI API Key
1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan API key'i `.env` dosyasına ekleyin

### SerpAPI Key
1. [SerpAPI](https://serpapi.com/) adresine gidin
2. Ücretsiz hesap oluşturun
3. API key'inizi alın
4. `.env` dosyasına ekleyin

## 📁 Proje Yapısı

```
BTK-HACKTHON-ETİCARET/
├── app/
│   ├── main.py                 # FastAPI ana uygulama
│   ├── serp_agent.py           # SerpAPI entegrasyonu
│   ├── gemini_agent_v2.py      # Gelişmiş Gemini AI entegrasyonu
│   ├── excel_generator.py      # Excel rapor oluşturucu
│   └── schemas.py              # Pydantic modelleri
├── reports/                    # Excel raporları (otomatik oluşturulur)
├── requirements.txt            # Python bağımlılıkları
├── env.example                 # Örnek environment variables
├── Dockerfile                  # Docker konfigürasyonu
├── docker-compose.yml          # Docker Compose
└── README.md                   # Bu dosya
```

## 🚀 Örnek Çıktı

### API Response
```json
{
  "success": true,
  "search_results": {
    "serpapi": [
      {
        "title": "Beyaz Geceler",
        "price": 33.0,
        "url": "https://www.kitapyurdu.com/kitap/beyaz-geceler",
        "platform": "Kitapyurdu",
        "original_price": "₺33,00"
      }
    ]
  },
  "best_offer": {
    "title": "Beyaz Geceler",
    "price": 33.0,
    "platform": "Kitapyurdu"
  },
  "gemini_analysis": {
    "analysis": "Kitap analizi...",
    "seo_content": "SEO içeriği...",
    "sales_recommendation": "Satış önerileri...",
    "profit_analysis": "Kar analizi..."
  },
  "excel_report": "reports/kitap_analizi_Beyaz_Geceler_20241201_143022.xlsx"
}
```

### Excel Raporu İçeriği
- **Özet Sayfası**: Kitap bilgileri ve satış uygunluğu
- **Fiyat Karşılaştırma**: Tüm platformların fiyat tablosu
- **Kar Analizi**: Maliyet hesaplama ve kar marjı analizi
- **Detaylı Analiz**: Gemini AI analizlerinin tam metni

## 💰 Kar Hesaplama Formülü

```
Alış Fiyatı: [En ucuz platform fiyatı]
Kargo Maliyeti: 70 TL (sabit)
Komisyon: %21 (Trendyol/Shopify)
Kar Marjı: 100 TL (varsayılan)

Toplam Maliyet = Alış Fiyatı + Kargo
Komisyon Tutarı = (Alış Fiyatı + Kar Marjı) × %21
Önerilen Satış Fiyatı = Toplam Maliyet + Komisyon Tutarı + Kar Marjı
Net Kar = Önerilen Satış Fiyatı - Toplam Maliyet
```

## 🎯 Özellik Detayları

### Akıllı Rekabet Analizi
- En pahalı rakip fiyatı ile karşılaştırma
- Farklı kar marjları ile test (50, 75, 100, 125, 150 TL)
- Rekabet edebilir mi? analizi
- Optimal fiyat önerisi

### Gelişmiş Fiyat Çıkarma
- Farklı fiyat formatlarını destekler (1.850,00, 1,850.00, 1850)
- Binlik ayırıcı otomatik algılama
- TL işareti ve para birimi tanıma
- Hata durumunda fallback mekanizması

### Profesyonel Excel Raporu
- 4 sayfa detaylı analiz
- Renkli başlıklar ve tablolar
- Otomatik sütun genişlikleri
- Timestamp ile dosya adlandırma

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje BTK Hackathon kapsamında geliştirilmiştir.

## 📞 İletişim

Proje hakkında sorularınız için issue açabilirsiniz.

## 🔄 Güncelleme Geçmişi

### v2.0.0 (Güncel)
- ✅ SerpAPI entegrasyonu
- ✅ Gelişmiş Gemini AI analizi
- ✅ Excel rapor oluşturma
- ✅ Akıllı kar hesaplama
- ✅ Rekabet analizi
- ✅ Profesyonel web arayüzü

### v1.0.0 (Önceki)
- ✅ Temel web scraping
- ✅ Basit Gemini AI entegrasyonu
- ✅ Temel fiyat karşılaştırma
