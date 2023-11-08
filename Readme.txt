Chương trình trên thực hiện xử lý ảnh 2D từ ảnh đầu vào thu được thông qua Camera. Đầu ra chương trình là tọa độ 4 góc của mẫu phôi. Chương trình được viết bằng ngôn ngữ Python với thư viện xử lý ảnh OpenCV.
Các bước thực thi như sau:
1. Lấy ảnh
2. Lọc màu đỏ xác định phạm vi phôi
3. khoanh vùng phạm vi phôi
4. Phân ngưỡng bức ảnh tách phôi ra khỏi nền
5. Thực hiện tiền xử lý ảnh loại bỏ các nhiễu còn lại
6. Thực hiện xác định các đường line biên dạng phôi
7. Xác định gốc phôi là giao của các đường line
8. Lưu giá trị tọa độ pixel của từng gốc phôi
9. Thực hiện các tác vụ còn lại (Chuyển tọa độ, Mở giao diện,...)

Các vấn đề tồn tại của chương trình
1. Chương trình viết còn thô sơ chưa khoa học
2. Chương trình thực hiện chỉ dùng cho phôi phẳng và có 4 góc vuông
3. Ngoài ra còn một số hạn chế về ý tưởng các bước thực thi cho ra kết quả không như mong đợi
