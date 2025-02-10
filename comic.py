import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

def download_images(url, multiple_images=True):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    comic_name = path_parts[2] if len(path_parts) > 2 else "comic"
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    options.add_argument('--disable-gpu')  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5) 

    if not os.path.exists(comic_name):
        os.makedirs(comic_name)

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    chapter_number = path_parts[-1] if len(path_parts) > 1 else "unknown"

    if multiple_images:
        chapter_folder = os.path.join(comic_name, f"{comic_name}-{chapter_number}")
        if not os.path.exists(chapter_folder):
            os.makedirs(chapter_folder)
    else:
        chapter_folder = comic_name

    try:
        if multiple_images:
            images = driver.find_elements(By.CSS_SELECTOR, 'img.lozad')
            for idx, img in enumerate(images):
                img_url = img.get_attribute('data-src')
                if img_url:
                    img_name = f"{comic_name}-{chapter_number}-{idx + 1}.jpg"
                    img_path = os.path.join(chapter_folder, img_name)
                    download_and_save_image(img_url, img_path, url)
        else:
            img_element = driver.find_element(By.CSS_SELECTOR, 'div.col-xs-4.col-image img.image-thumb')
            img_url = img_element.get_attribute('data-src')
            if img_url:
                img_name = f"{comic_name}-cover.jpg"
                img_path = os.path.join(chapter_folder, img_name)
                download_and_save_image(img_url, img_path, url)
    except Exception as e:
        print(f"Lỗi khi tải ảnh từ {url}: {e}")

    driver.quit()

def download_and_save_image(img_url, img_path, referer_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": referer_url,
    }
    try:
        response = requests.get(img_url, headers=headers)
        response.raise_for_status() 
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"Đã tải {img_path} thành công!")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải ảnh {img_url}: {e}")

url = "https://nettruyenvie.com/truyen-tranh/tham-tu-kindaichi"

download_images(url, multiple_images=False)
for i in range(0, 11):  # 1 -> 10
    base_url = url + f"/chuong-{i}" 
    download_images(base_url)
