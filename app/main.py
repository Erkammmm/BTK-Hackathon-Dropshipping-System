from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import uvicorn
from app.schemas import BookRequest
from app.gemini_agent_v2 import GeminiAgentV2
from app.serp_agent import SerpAgent
from app.excel_generator import ExcelGenerator

app = FastAPI(title="Kitap Fiyat Karşılaştırma API", version="1.0.0")

# Agent instances
serp_agent = SerpAgent()
gemini_agent = GeminiAgentV2()
excel_generator = ExcelGenerator()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Ana sayfa - Kitap arama ve fiyat karşılaştırma"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kitap Fiyat Karşılaştırma</title>
        <meta charset="utf-8">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-top: 20px; }
            h1 { color: #333; text-align: center; margin-bottom: 30px; font-size: 2.5em; }
            .subtitle { text-align: center; color: #666; margin-bottom: 40px; font-size: 1.2em; }
            .search-form { text-align: center; margin: 40px 0; }
            input[type="text"] { width: 60%; padding: 15px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; margin-right: 10px; }
            button { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; }
            button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 40px 0; }
            .feature { background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea; }
            .feature h3 { color: #333; margin-bottom: 10px; }
            .feature p { color: #666; line-height: 1.6; }
            .api-info { background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; }
            .api-info h3 { color: #1976d2; margin-bottom: 15px; }
            .api-info ul { list-style: none; padding: 0; }
            .api-info li { padding: 5px 0; color: #333; }
            .api-info li:before { content: "🔍 "; }
            .result { margin-top: 20px; padding: 15px; border-radius: 8px; background: #f8f9fa; display: none; }
            .result.show { display: block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Kitap Fiyat Karşılaştırma</h1>
            <p class="subtitle">
                Tüm web sitelerinde arama yaparak en uygun fiyatlı kitabı bulun!
            </p>
            
            <div class="search-form">
                <input type="text" id="bookName" placeholder="Kitap adını yazın (örn: Beyaz Geceler)" />
                <button onclick="searchBook()">🔍 Kitap Ara</button>
            </div>
            
            <div id="result" class="result">
                <h3>📚 Arama Sonuçları</h3>
                <div id="resultContent"></div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🔍 Google Shopping Arama</h3>
                    <p>SerpAPI ile Google Shopping'de arama yaparak tüm e-ticaret sitelerinden en uygun fiyatlı kitabı bulur.</p>
                </div>
                <div class="feature">
                    <h3>🧠 SEO Açıklama</h3>
                    <p>Gemini AI ile bulunan kitap için SEO uyumlu başlık ve açıklama üretir.</p>
                </div>
                <div class="feature">
                    <h3>💰 En İyi Fiyat</h3>
                    <p>Tüm platformlardan en düşük fiyatlı seçeneği otomatik olarak seçer ve gösterir.</p>
                </div>
            </div>
            
            <div class="api-info">
                <h3>📡 API Endpoints</h3>
                <ul>
                    <li><strong>POST /search-book</strong> - Kitap ara ve en iyi fiyatı bul</li>
                    <li><strong>GET /docs</strong> - API dokümantasyonu</li>
                </ul>
            </div>
        </div>
        
        <script>
            async function searchBook() {
                const bookName = document.getElementById('bookName').value;
                if (!bookName) {
                    alert('Lütfen kitap adını girin!');
                    return;
                }
                
                const resultDiv = document.getElementById('result');
                const resultContent = document.getElementById('resultContent');
                
                resultContent.innerHTML = '<p>🔍 Arama yapılıyor...</p>';
                resultDiv.classList.add('show');
                
                try {
                    const response = await fetch('/search-book', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ book_name: bookName })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        const bestOffer = result.best_offer;
                        const geminiAnalysis = result.gemini_analysis;
                        
                        let html = `
                            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>🏆 En İyi Teklif</h4>
                                <p><strong>Kitap:</strong> ${bestOffer.title}</p>
                                <p><strong>Platform:</strong> ${bestOffer.platform}</p>
                                <p><strong>Fiyat:</strong> ${bestOffer.price} TL</p>
                                <p><strong>Link:</strong> <a href="${bestOffer.url}" target="_blank">${bestOffer.url || 'Link bulunamadı'}</a></p>
                            </div>
                            
                            <div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>🧠 Gelişmiş Analiz</h4>
                                <p><strong>Kitap Analizi:</strong></p>
                                <p style="white-space: pre-line;">${geminiAnalysis.analysis}</p>
                            </div>
                            
                            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>📝 SEO İçeriği</h4>
                                <p style="white-space: pre-line;">${geminiAnalysis.seo_content}</p>
                            </div>
                            
                            <div style="background: #f3e5f5; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>💰 Satış Önerileri</h4>
                                <p style="white-space: pre-line;">${geminiAnalysis.sales_recommendation}</p>
                            </div>
                            
                            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>📊 Özet</h4>
                                <p style="white-space: pre-line;">${geminiAnalysis.best_offer_summary}</p>
                            </div>
                            
                            <div style="background: #fff8e1; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>💰 Kar Analizi</h4>
                                <p style="white-space: pre-line;">${geminiAnalysis.profit_analysis}</p>
                            </div>
                            
                            <div style="background: #e1f5fe; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                <h4>📊 Excel Raporu</h4>
                                <p><strong>Dosya:</strong> ${result.excel_report}</p>
                                <p><em>Excel raporu reports/ klasörüne kaydedildi. Detaylı analiz için bu dosyayı açabilirsiniz.</em></p>
                            </div>
                            
                            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                                <h4>📊 Tüm Sonuçlar</h4>
                        `;
                        
                        for (const [platform, offer] of Object.entries(result.search_results)) {
                            if (platform !== 'best_offer' && offer) {
                                html += `
                                    <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                                        <p><strong>${offer.platform}:</strong> ${offer.price} TL - <a href="${offer.url}" target="_blank">Görüntüle</a></p>
                                    </div>
                                `;
                            }
                        }
                        
                        html += '</div>';
                        resultContent.innerHTML = html;
                    } else {
                        resultContent.innerHTML = '<p style="color: red;">❌ Kitap bulunamadı!</p>';
                    }
                } catch (error) {
                    resultContent.innerHTML = '<p style="color: red;">❌ Hata: ' + error.message + '</p>';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/search-book")
async def search_book(request: BookRequest):
    """Kitap ara ve en iyi fiyatı bul"""
    try:
        print(f"🔍 Kitap aranıyor: {request.book_name}")
        
        # SerpAPI ile Google Shopping'de arama yap
        print("🔍 Google Shopping'de arama yapılıyor...")
        search_results = await serp_agent.search_book(request.book_name)
        
        best_offer = search_results['best_offer']
        
        if not best_offer:
            raise HTTPException(status_code=404, detail="Kitap bulunamadı")
        
        print(f"✅ En iyi teklif bulundu: {best_offer['title']} - {best_offer['price']} TL")
        
        # Gelişmiş Gemini analizi ve içerik üretimi
        print("🧠 Gelişmiş analiz ve içerik üretimi yapılıyor...")
        gemini_analysis = await gemini_agent.analyze_book_and_generate_content(
            search_results['search_results'], 
            best_offer
        )
        
        # Excel raporu oluştur
        print("📊 Excel raporu oluşturuluyor...")
        excel_file_path = excel_generator.create_book_analysis_report(
            search_results['search_results'],
            best_offer,
            gemini_analysis
        )
        
        return {
            "success": True,
            "search_results": search_results,
            "best_offer": best_offer,
            "gemini_analysis": gemini_analysis,
            "excel_report": excel_file_path,
            "message": f"✅ {best_offer['title']} için detaylı analiz ve Excel raporu tamamlandı!"
        }
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Kitap arama hatası: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 