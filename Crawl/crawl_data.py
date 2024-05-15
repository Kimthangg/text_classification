from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Danh sách các danh mục
topics = ['the-gioi','kinh-te','doi-song','suc-khoe','gioi-tre','giao-duc','van-hoa','giai-tri','xe','du-lich','the-thao','cong-nghe-game']

cac_danh_muc = ['Thế giới',
                    'Kinh tế',
                    'Đời sống',
                    'Sức khỏe',
                    'Giới trẻ',
                    'Giáo dục',
                    'Văn hóa',
                    'Giải trí',
                    'Xe',
                    'Du lịch',
                    'Thể thao',
                    'Công nghệ - Game']

base_url = 'https://thanhnien.vn'

# Khởi tạo các list
article_links = []
data = []

# Duyệt qua từng topic
for topic in topics:
    # Đường dẫn đến các topic
    url = f"{base_url}/{topic}.htm"
    #Get đường dẫn
    driver.get(url)
    #Đợi 3s cho trang load
    sleep(3)
    #Lấy html của trang web 
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #Tìm all các ô có đường dẫn
    content = soup.find_all('h3',class_='box-title-text')
    print(topic)
    # Lấy link bài viết ở trang topic đầu
    for article in content:
        article_links.append(article.find('a')['href'])
        
for i in article_links:
    driver.get(base_url+i)
    # Get the page source HTML
    html_sub = driver.page_source
    # Use BeautifulSoup to parse the HTML
    soup_sub = BeautifulSoup(html_sub, 'html.parser')
    if soup_sub.find('div',class_ = 'detail-cate'):
    #Lấy danh mục
        danh_muc = soup_sub.find('div',class_ = 'detail-cate').find('a').text.strip()
        if danh_muc not in cac_danh_muc:
            continue
        #Lấy nội dung của bài viết
        paragraphs = soup_sub.find('div', class_ = 'detail-cmain').find_all('p')
        noi_dung = ' '.join(p.text for p in paragraphs)
        #Lưu danh mục và nội dung dưới dạng từ điển
        data.append({'Danh mục':danh_muc,'Nội dung':noi_dung})
        print({'Danh mục':danh_muc,'Nội dung':noi_dung})
    else:
        continue

# Đóng trình duyệt
driver.quit()
#Lưu data thành file csv
df = pd.DataFrame(data)
df.to_csv('Data.csv', index=False)
