import os
from dotenv import load_dotenv
import openpyxl
from app.utils import generate_barkod
import datetime
import random
import httpx
import json
import base64
from app.auto_upload import auto_upload_to_trendyol, drag_drop_upload, simple_auto_upload

load_dotenv()

TRENDYOL_API_KEY = os.getenv('TRENDYOL_API_KEY')
TRENDYOL_SUPPLIER_ID = os.getenv('TRENDYOL_SUPPLIER_ID')

EXCEL_PATH = "Roman_27_07_2025-21_23.xlsx"

async def find_trendyol_existing_product(book_name: str):
    """Trendyol'da mevcut ürün linki bul"""
    try:
        search_url = f"https://www.trendyol.com/sr?q={book_name.replace(' ', '+')}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(search_url, timeout=10)
            if resp.status_code == 200:
                # Basit bir link bulma (gerçek scraping için daha gelişmiş gerekir)
                return f"https://www.trendyol.com/sr?q={book_name.replace(' ', '+')}"
        return None
    except:
        return None

async def upload_to_trendyol_api(product_info: dict):
    """Trendyol API'ye ürün yükle (gelişmiş versiyon)"""
    if not TRENDYOL_API_KEY or not TRENDYOL_SUPPLIER_ID:
        # API anahtarları yoksa basit otomatik yüklemeyi dene
        simple_result = await simple_auto_upload()
        return simple_result
    
    try:
        # Farklı API endpoint'lerini dene
        api_urls = [
            f"https://api.trendyol.com/sapigw/suppliers/{TRENDYOL_SUPPLIER_ID}/products",
            f"https://api.trendyol.com/sapigw/suppliers/{TRENDYOL_SUPPLIER_ID}/product",
            f"https://api.trendyol.com/sapigw/suppliers/{TRENDYOL_SUPPLIER_ID}/products/create"
        ]
        
        # Ürün verisi hazırla
        product_data = {
            "barcode": generate_barkod(product_info['title']),
            "title": product_info['title'],
            "productMainId": generate_barkod(product_info['title']),
            "brandId": 1,
            "categoryId": 1750,
            "quantity": random.choice([10, 50, 100]),
            "stockCode": "",
            "dimensionalWeight": 1,
            "description": product_info['description'],
            "listPrice": product_info['price'],
            "salePrice": product_info['price'],
            "vatRate": 0,
            "cargoCompanyId": 1,
            "images": [
                {
                    "url": product_info.get('image_url', '')
                }
            ],
            "attributes": [
                {
                    "attributeId": 1,
                    "attributeValueId": 1
                }
            ]
        }
        
        # Farklı authentication yöntemlerini dene
        auth_methods = [
            {"Authorization": f"Bearer {TRENDYOL_API_KEY}"},
            {"Authorization": f"Basic {base64.b64encode(f'{TRENDYOL_SUPPLIER_ID}:{TRENDYOL_API_KEY}'.encode()).decode()}"},
            {"X-API-Key": TRENDYOL_API_KEY},
            {"Authorization": f"Basic {base64.b64encode(f'{TRENDYOL_SUPPLIER_ID}:{TRENDYOL_API_KEY}'.encode()).decode()}", "X-Supplier-Id": TRENDYOL_SUPPLIER_ID}
        ]
        
        headers_base = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8"
        }
        
        async with httpx.AsyncClient() as client:
            for api_url in api_urls:
                for auth_header in auth_methods:
                    try:
                        headers = {**headers_base, **auth_header}
                        resp = await client.post(api_url, headers=headers, json=product_data, timeout=30)
                        
                        if resp.status_code == 200:
                            return {
                                'status': 'success',
                                'message': f'Ürün Trendyol API\'ye başarıyla yüklendi. Endpoint: {api_url}'
                            }
                        elif resp.status_code == 201:
                            return {
                                'status': 'success',
                                'message': f'Ürün Trendyol API\'ye başarıyla oluşturuldu. Endpoint: {api_url}'
                            }
                        elif resp.status_code == 403:
                            continue
                        else:
                            return {
                                'status': 'warning',
                                'message': f'Trendyol API hatası: {resp.status_code} - {resp.text[:200]}'
                            }
                    except Exception as e:
                        continue
            
            # Hiçbir API yöntemi çalışmadıysa, basit otomatik yüklemeyi dene
            simple_result = await simple_auto_upload()
            if simple_result['status'] == 'success':
                return simple_result
            
            # Basit yükleme de başarısızsa, tam otomatik dene
            auto_result = await auto_upload_to_trendyol()
            if auto_result['status'] == 'success':
                return auto_result
            
            # Tam otomatik de başarısızsa, sürükle-bırak dene
            drag_result = await drag_drop_upload()
            if drag_result['status'] == 'success':
                return drag_result
            
            # Hiçbiri çalışmadıysa, manuel yükleme talimatları ver
            trendyol_link = await find_trendyol_existing_product(product_info['title'])
            
            return {
                'status': 'info',
                'message': f'Excel dosyası hazır! Trendyol paneline git ve Excel\'deki son satırı kopyala. Link: {trendyol_link if trendyol_link else "https://partner.trendyol.com/product-management"}'
            }
                
    except Exception as e:
        # Hata durumunda da basit otomatik yüklemeyi dene
        simple_result = await simple_auto_upload()
        return simple_result

async def add_product_to_trendyol(product_info: dict):
    try:
        # Excel dosyasını aç
        wb = openpyxl.load_workbook(EXCEL_PATH)
        ws = wb.active
        # Barkod oluştur
        barkod = generate_barkod(product_info['title'])
        # Mevcut yıl
        current_year = datetime.datetime.now().year
        # Stok adedi (10 veya 100)
        stock_quantity = random.choice([10, 50, 100])
        # Sevkiyat süresi (sadece sayı)
        shipping_days = random.choice([2, 3, 4])
        
        # Kolon sırasına göre yeni satır oluştur
        new_row = [
            barkod,  # Barkod
            "",     # Model Kodu
            "GENEL", # Marka
            1750,    # Kategori
            "TRY",  # Para Birimi
            product_info['title'], # Ürün Adı
            product_info['description'], # Ürün Açıklaması (Gemini'den gelen açıklama)
            product_info.get('market_price', product_info['price']), # Piyasa Satış Fiyatı (Trendyol'dan yüksek)
            product_info['price'], # Trendyol Satış Fiyatı (hesaplanan fiyat)
            stock_quantity,     # Stok Adedi (10, 50, 100)
            "",     # Stok Kodu
            0,       # KDV Oranı
            1,       # Desi
            product_info.get('image_url', ''), # Görsel 1
            "", "", "", "", "", "", "", # Görsel 2-8
            shipping_days,     # Sevkiyat Süresi (sadece sayı: 2, 3, 4)
            "",     # Sevkiyat Tipi (boş bırakıldı)
            "Tekil",     # Setli/Tekil
            current_year,     # Basım Yılı
            product_info.get('author', ''), # Yazar (gerçek yazar adı)
            "",     # Temsilci/İfa
            "TR",   # Menşei
            "13.5x21",     # Boyut
            "200",     # Sayfa Sayısı
            "Roman",     # Roman Türü
            "GENEL YAYIN",     # Üretici Bilgi
            "Karton Kapak",     # Cilt Bilgisi
            "Genel",     # Yaş Grubu
        ]
        ws.append(new_row)
        wb.save(EXCEL_PATH)
        
        # Trendyol API'ye de yükle (artık tam otomatik)
        api_result = await upload_to_trendyol_api(product_info)
        
        return {
            'status': 'success',
            'message': f'Ürün Excel dosyasına eklendi. Barkod: {barkod}, Stok: {stock_quantity}, Sevkiyat: {shipping_days} gün. {api_result["message"]}'
        }
    except PermissionError:
        return {
            'status': 'warning',
            'message': f'Excel dosyası açık olduğu için yazılamadı. Barkod: {generate_barkod(product_info["title"])} - Lütfen Excel dosyasını kapatıp tekrar deneyin.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Excel dosyasına yazma hatası: {str(e)}'
        } 