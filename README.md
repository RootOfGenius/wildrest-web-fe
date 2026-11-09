# WildRest.vn

Trang giới thiệu server Minecraft sinh tồn WildRest.vn, dùng HTML, CSS và JavaScript thuần. Chạy trực tiếp trên GitHub Pages, không cần build.

- Chạy thử: `python -m http.server 8080` rồi mở `http://localhost:8080`.
- Nội dung nằm trong `index.html`, giao diện trong `style.css`.
- IP, ngày mở cửa, Discord và các liên kết mạng xã hội được cấu hình ở đầu `script.js`.
- Ảnh tối ưu và font được lưu trong `assets/`.
- Để hiện số người trực tuyến Discord, bật **Server Settings → Widget → Enable Server Widget**. Nếu widget không khả dụng, thống kê tự ẩn.

## Thêm ảnh và tin cập nhật

- Đặt ảnh WebP đã gắn watermark trong `assets/gallery/`, ví dụ `anh-07.webp`. Chạy `python -m pip install Pillow` rồi `python prepare_assets.py --gallery` để tạo bản `anh-07-640.webp`.
- Thêm ảnh vào `ANH_MAY_CHU` ở đầu `script.js`, gồm `src`, kích thước gốc `width` / `height`, mô tả `alt` và `chuThich`. Nếu đổi ảnh đầu tiên, cập nhật `VideoGame.image` trong JSON-LD.
- Thêm tin mới nhất vào đầu `CAP_NHAT` với `ngay` dạng `YYYY-MM-DD`, `tieuDe` và mảng `noiDung`. Đồng bộ danh sách tĩnh `#update-list` trong `index.html` để tin hiện cả khi tắt JavaScript.
