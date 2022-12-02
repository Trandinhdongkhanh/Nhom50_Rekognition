# Nhom50_Rekognition
Trần Đình Đông Khánh - 20110503 (Nhóm trưởng)\
Đào Ngọc Thạch - 20110564\
Trần Trung Phát - 20110536

## Hướng dẫn cài đặt và chạy Project

B0: Tải và cài đặt các thư viện cần thiết

B1: Đăng nhập vào giao diện AWS Console trên Learner Lab và chọn dịch vụ S3

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/1.png?raw=true)

B2: Tạo Bucket và upload các Object (file ảnh) lên Bucket đó
### Lưu ý: Đặt tên file theo tên người nổi tiếng để dễ dàng quản lý, AWS chỉ hỗ trợ các dạng file ảnh sau: .png, .jpg, .jpeg

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/2.png?raw=true)

B3: Lấy key từ AWS Details và copy chúng vào file credentials.py

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/3.png?raw=true)

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/4.png?raw=true)

B4: Chạy đoạn code này 1 lần, sau đó comment nó lại

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/5.png?raw=true)

B5: Chọn dịch vụ DynamoDB trên AWS Console và tạo Table

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/6.png?raw=true)

B6: Copy ID người nổi tiếng và Paste vào mục face_id (khóa chính) của Table

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/7.png?raw=true)

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/8.png?raw=true)

B7: Uncomment đoạn code khởi tạo giao diện và hoàn thành


![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/10.png?raw=true)

![alt text](https://github.com/Trandinhdongkhanh/Nhom50_Rekognition/blob/main/Tutorial_Images/9.png?raw=true)

## Lưu ý: Thay các giá trị như Bucket, Table, Partition Key,... bằng cấu hình AWS trên tài khoản của bạn
