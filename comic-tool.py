import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse

# Hàm để tải ảnh và lưu với tên đúng định dạng
def download_images(url):
    # Thiết lập trình duyệt Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Chạy trình duyệt ở chế độ ẩn
    options.add_argument('--disable-gpu')  # Tắt GPU khi không cần thiết
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Mở trang
    driver.get(url)
    time.sleep(5)  # Đợi một lúc để trang tải xong

    # Lấy tên truyện và số chương từ URL
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    comic_name = path_parts[2]  # Tên truyện
    chapter_number = path_parts[-1]  # Số chương

    # Tạo thư mục để lưu hình ảnh nếu chưa có
    folder_name = f"{comic_name}-{chapter_number}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Lấy tất cả các URL hình ảnh
    images = driver.find_elements(By.CSS_SELECTOR, 'img.lozad')  # Lấy tất cả các hình ảnh với class 'lozad'

    # Tải tất cả các hình ảnh
    for idx, img in enumerate(images):
        img_url = img.get_attribute('data-src')  # Lấy URL ảnh từ thuộc tính 'data-src'

        if img_url:
            # Tạo tên ảnh theo định dạng: comic_name-chapter_number-image_index.jpg
            img_name = f"{comic_name}-{chapter_number}-{idx + 1}.jpg"
            img_path = os.path.join(folder_name, img_name)

            # Gửi yêu cầu tải ảnh với headers giả lập trình duyệt
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": url,  # Đảm bảo referer từ trang web chính
            }

            # Tải ảnh và lưu vào thư mục
            try:
                response = requests.get(img_url, headers=headers)
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                with open(img_path, 'wb') as f:
                    f.write(response.content)
                print(f"Đã tải {img_name} thành công!")
            except requests.exceptions.RequestException as e:
                print(f"Lỗi khi tải ảnh {img_name}: {e}")

    # Đóng trình duyệt Selenium
    driver.quit()

# URL truyện bạn muốn tải ảnh
url = "https://nettruyenviet.com/truyen-tranh/doremon/chuong-5"
download_images(url)
