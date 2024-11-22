import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Thư mục gốc và tên truyện
base_folder = "manga_chapters"  # Thư mục gốc
manga_name = "tham-tu-conan"
manga_folder = os.path.join(base_folder, manga_name)  # Đường dẫn đến thư mục truyện

# URL gốc cho các chương truyện
base_url = "https://nettruyenviet.com/truyen-tranh/tham-tu-conan/chuong-"
chapters = [7]  # Danh sách số chương

# Tạo thư mục gốc và thư mục truyện
os.makedirs(manga_folder, exist_ok=True)

for chapter in chapters:
    chapter_folder_name = f"{manga_name}-chapter-{chapter}"
    chapter_folder = os.path.join(manga_folder, chapter_folder_name)
    os.makedirs(chapter_folder, exist_ok=True)

    chapter_url = f"{base_url}{chapter}"
    print(f"Downloading chapter {chapter}...")

    # Gửi yêu cầu đến trang chương truyện
    response = requests.get(chapter_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Chọn các thẻ ảnh trong chương
    images = soup.select('img[data-src]')  # Thay đổi selector nếu cần

    for index, img in enumerate(images):
        img_url = urljoin(chapter_url, img['data-src'])
        img_data = requests.get(img_url).content

        file_name = f"{manga_name}-{chapter}-{index+1}.jpg"
        file_path = os.path.join(chapter_folder, file_name)
        with open(file_path, 'wb') as file:
            file.write(img_data)
            print(f"Downloaded: {file_name}")

print("All chapters downloaded successfully!")
