import re
import datetime

def generate_barkod(book_name: str) -> str:
    # Türkçe karakterleri sadeleştir
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'
    }
    for src, target in replacements.items():
        book_name = book_name.replace(src, target)
    # Sadece harf ve rakamları al, boşlukları kaldır
    short = ''.join([w[:3] for w in book_name.split() if w.isalnum()])
    short = re.sub(r'[^a-zA-Z0-9]', '', short)
    year = datetime.datetime.now().year
    return f"mf{short.lower()}{year}"

def get_trendyol_upload_instructions():
    """Trendyol'a Excel yükleme talimatları"""
    return """
    📋 TRENDYOL EXCEL YÜKLEME TALİMATLARI:
    
    1. Trendyol Satıcı Paneli'ne giriş yapın
    2. "Ürün Yönetimi" > "Toplu Ürün Yükleme" bölümüne gidin
    3. "Excel ile Ürün Yükle" seçeneğini tıklayın
    4. "Roman_27_07_2025-21_23.xlsx" dosyasını seçin
    5. "Yükle" butonuna tıklayın
    6. Yükleme durumunu takip edin
    
    ⚠️ ÖNEMLİ NOTLAR:
    - Excel dosyası açık olmamalı
    - Tüm zorunlu alanlar doldurulmuş olmalı
    - Barkod benzersiz olmalı
    - Fiyatlar doğru formatta olmalı
    
    🔗 ALTERNATİF YÖNTEM:
    - Excel dosyasını Trendyol paneline sürükleyip bırakın
    - Otomatik yükleme başlayacaktır
    """

def get_manual_upload_steps():
    """Manuel yükleme adımları"""
    return """
    🚀 MANUEL YÜKLEME ADIMLARI:
    
    1. Excel dosyasını açın
    2. Son eklenen satırı kontrol edin
    3. Trendyol'da "Ürün Ekle" sayfasına gidin
    4. Bilgileri tek tek girin:
       - Barkod: {barkod}
       - Ürün Adı: {title}
       - Açıklama: {description}
       - Fiyat: {price} TL
       - Stok: {stock}
       - Kategori: 1750 (Roman)
       - Marka: GENEL
    
    ⏱️ TAHMİNİ SÜRE: 2-3 dakika
    """ 