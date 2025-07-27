import os
import time
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
from dotenv import load_dotenv
import subprocess
import platform

load_dotenv()

TRENDYOL_EMAIL = os.getenv('TRENDYOL_EMAIL')
TRENDYOL_PASSWORD = os.getenv('TRENDYOL_PASSWORD')

async def simple_auto_upload():
    """Basit otomatik yükleme - Excel'i aç ve Trendyol'a yönlendir"""
    try:
        # Excel dosyasını aç
        excel_path = os.path.abspath("Roman_27_07_2025-21_23.xlsx")
        
        if platform.system() == "Windows":
            os.startfile(excel_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", excel_path])
        else:  # Linux
            subprocess.call(["xdg-open", excel_path])
        
        time.sleep(2)
        
        # Trendyol satıcı paneline git
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Trendyol'a git
        driver.get("https://partner.trendyol.com/product-management")
        
        return {
            'status': 'success',
            'message': '✅ Excel dosyası açıldı ve Trendyol paneline yönlendirildi! Şimdi Excel\'deki son satırı kopyalayıp Trendyol\'a yapıştırabilirsin.'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Basit yükleme hatası: {str(e)}'
        }

async def auto_upload_to_trendyol():
    """Excel dosyasını Trendyol'a otomatik yükle"""
    try:
        # Chrome ayarları
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # WebDriver başlat
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Trendyol satıcı paneline git
        driver.get("https://partner.trendyol.com/account/login")
        
        # Giriş yap
        if TRENDYOL_EMAIL and TRENDYOL_PASSWORD:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(TRENDYOL_EMAIL)
            
            password_input = driver.find_element(By.NAME, "password")
            password_input.send_keys(TRENDYOL_PASSWORD)
            
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Giriş sonrası bekle
            time.sleep(5)
        
        # Ürün yönetimi sayfasına git
        driver.get("https://partner.trendyol.com/product-management")
        time.sleep(3)
        
        # Toplu ürün yükleme bölümüne git
        bulk_upload_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Toplu Ürün Yükleme')]"))
        )
        bulk_upload_link.click()
        time.sleep(3)
        
        # Excel dosyasını yükle
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # Excel dosyasının tam yolunu al
        excel_path = os.path.abspath("Roman_27_07_2025-21_23.xlsx")
        file_input.send_keys(excel_path)
        
        # Yükle butonuna tıkla
        upload_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yükle') or contains(text(), 'Upload')]"))
        )
        upload_button.click()
        
        # Yükleme tamamlanmasını bekle
        time.sleep(10)
        
        # Başarı mesajını kontrol et
        success_message = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'başarı') or contains(text(), 'success')]"))
        )
        
        driver.quit()
        
        return {
            'status': 'success',
            'message': 'Excel dosyası Trendyol\'a otomatik olarak yüklendi!'
        }
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        
        return {
            'status': 'error',
            'message': f'Otomatik yükleme hatası: {str(e)}. Manuel yükleme gerekli.'
        }

async def drag_drop_upload():
    """Sürükle-bırak ile otomatik yükleme"""
    try:
        # Chrome başlat
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Trendyol paneline git
        driver.get("https://partner.trendyol.com/product-management")
        time.sleep(5)
        
        # Excel dosyasını sürükle-bırak
        excel_path = os.path.abspath("Roman_27_07_2025-21_23.xlsx")
        
        # Dosyayı sürükle-bırak alanına bırak
        drop_zone = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'drop-zone') or contains(@class, 'upload-area')]"))
        )
        
        # PyAutoGUI ile dosyayı sürükle
        pyautogui.dragTo(drop_zone.location['x'] + 100, drop_zone.location['y'] + 100, duration=2)
        pyautogui.drop()
        
        time.sleep(5)
        driver.quit()
        
        return {
            'status': 'success',
            'message': 'Dosya sürükle-bırak ile yüklendi!'
        }
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        
        return {
            'status': 'error',
            'message': f'Sürükle-bırak hatası: {str(e)}'
        } 