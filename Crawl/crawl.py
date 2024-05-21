import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
import threading

topics = ['thoi-su','the-gioi','kinh-te','doi-song','suc-khoe','gioi-tre','giao-duc','van-hoa','giai-tri','the-thao','cong-nghe-game','xe','du-lich']
cac_danh_muc = ['Thời sự',
                'Thế giới',
                'Kinh tế',
                'Đời sống',
                'Sức khỏe',
                'Giới trẻ',
                'Giáo dục',
                'Văn hóa',
                'Giải trí',
                'Thể thao',
                'Công nghệ - Game',
                'Xe',
                'Du lịch',]
base_url = 'https://thanhnien.vn'

article_links = []
data = []
lock = threading.Lock()

def get_link(url):
    print("Link",len(article_links))
    #Kiểm tra nếu lỗi thì bỏ qua
    try:
        response = rq.get(f"{base_url}{url}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,"html.parser")
            #Tìm all các ô có đường dẫn
            content = soup.find_all('a',class_='box-category-link-title')
            # Lấy link bài viết ở trang 
            for article in content:
                with lock:
                    #Kiểm tra href này có trong article_links chưa nếu chưa thì thêm vào
                    if article['href'] not in article_links:
                        article_links.append(article['href'])
        else:
            print("Không thể truy cập trang web.")
    except:
        return
#Lặp qua các topic lấy các href      
for topic in topics:
    get_link("/"+topic)
#Dùng đa luồng lặp lấy các href từ article_links
threads = []
# max_threads = 10000   
for link in article_links:
    #Nếu số lượng link lớn hơn 30000 dừng
    if len(article_links) > 30000:
        break
    thread = threading.Thread(target=get_link, args=(link,))
    thread.start()
    threads.append(thread)

def get_content(url):
    print("Data",len(data))
    try:
        html_sub = rq.get(base_url+url)
        # Use BeautifulSoup to parse the HTML
        soup_sub = BeautifulSoup(html_sub.content, 'html.parser')
        if soup_sub.find('div',class_ = 'detail-cate'):
        #Lấy danh mục
            danh_muc = soup_sub.find('div',class_ = 'detail-cate').find('a').text.strip()
            if danh_muc not in cac_danh_muc:
                return
            #Lấy nội dung của bài viết
            paragraphs = soup_sub.find('div', class_ = 'detail-cmain').find_all('p')
            noi_dung = ' '.join(p.text for p in paragraphs)
            #Lưu danh mục và nội dung dưới dạng từ điển
            with lock:
                data.append({'Danh mục':danh_muc,'Nội dung':noi_dung})
        else:
            return
    except:
        return
#Dùng đa luồng lấy danh mục và nội dung từ các link đã crawl
threads = []
for link in article_links:
    thread = threading.Thread(target=get_content, args=(link,))
    thread.start()
    threads.append(thread)
print("Đang lưu vào data.csv")
# Lưu data thành file csv
df = pd.DataFrame(data)
df.to_csv('Data.csv', index=False)