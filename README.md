# 1.	Nghiên cứu và thu thập dữ liệu
-	Lấy danh sách link:
o	Để thực hiện bài toán phân loại văn bản này , cần thu thập một tập dữ liệu phong phú và đa dạng. Nguồn dữ liệu có thể từ các trang web, báo điện tử , diễn đàn, hoặc các kho dữ liệu mở. Ở đây chúng em thu thập dữ liệu từ trang web : Tin tức 24h mới nhất, tin nhanh, tin nóng hàng ngày | Báo Thanh Niên (thanhnien.vn).
o	Bước đầu ta sử dụng thư viện requests để lấy được nội dung của các trang chủ của các danh mục và sử dụng thư viện BeautifulSoup để xử lý
o	Sau đó tìm các hrel từ thẻ <a> có class = “box-category-link-title” và lưu lại. Sau đó truy cập vào các link và lặp lại các bước đến khi đủ số lượng link nhất định (Trong bài là 30000 link)
o	Do số lượng lớn nên ta sử dụng đa luồng để tối ưu về thời gian chạy
-	Lấy danh mục và nội dung:
o	Ta truy cập từng link đã lấy ở trên, sau đó ta lấy danh mục từ thẻ div có class = “detail-cate” và lấy nội dung từ thẻ div có class  = “detail-cmain”. Lặp lại các bước đến khi hết số lượng link
o	Do số lượng lớn nên ta cũng sử dụng đa luồng để tối ưu về thời gian chạy
# 2.	Xử lý dữ liệu
Dữ liệu thu thập cần phải qua nhiều bước xử lý để chuẩn bị cho việc xây dựng mô hình phân loại:
-	Chuyển đổi văn bản về dạng thống nhất : Chuyển về chữ thường.
-	Loại bỏ dấu câu , ký tự đặc biệt, xoá các dòng trống : Giúp đơn giản hóa văn bản
-	Tokenize : Tách văn bản thành từ hoặc cụm từ 
-	Chia dữ liệu thành 2 phần train và test với tỉ lệ 70/30
-	Biểu diễn văn bản: Sử dụng kĩ thuật TF-IDF để chuyển văn bản sang vector.
-	Dùng LabelEncoder chuyển các nhãn danh mục sang dạng số
# 3.	Xây dựng mô hình và đánh giá độ chính xác
-	Sử dụng các mô hình học máy và học sâu để phân loại văn bản. Các mô hình phổ biến bao gồm:
 Naive bayes
 Support Vector Machines (SVM)
 Mô hình hồi quy tuyến tính 
-	Để đánh giá hiệu quả của các mô hình, chúng tôi sử dụng các chỉ số như độ chính xác (accuracy) , độ chính xác(precision), độ nhạy (recall) , và điểm F1 (F1- score). 
-	Sau khi kiểm tra và đánh giá thì chúng tôi chọn mô hình Naive bayes cho bài toán

# 4.	Triển khai mô hình lên web
-	Chúng tôi sử dụng thư viện streamlit để triển khai mô hình lên trang web
-	Người dùng nhập đoạn văn bản cần phân loại vào mà bấm submit
-	Sau  đó đoạn văn bản sẽ được tiền xử lý và vector như xử lý dữ liệu train mô hình
-	Tiếp theo gọi mô hình đã train để dự đoán nhãn cho văn bản và hiển thị nhãn dự đoán cho người dùng
Link demo: https://phanloaivanban.streamlit.app/
