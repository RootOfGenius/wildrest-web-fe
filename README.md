# WildRest.vn · Sắp ra mắt

Repository public: [RootOfGenius/wildrest-web-fe](https://github.com/RootOfGenius/wildrest-web-fe). GitHub Pages phục vụ từ nhánh `main`, thư mục gốc, tên miền `wildrest.vn`.

Website một trang bằng HTML, CSS và JavaScript thuần. Không framework, không npm và không cần build. Mọi ảnh và font được phục vụ tại chỗ; đường dẫn ra ngoài trên trang chỉ dẫn đến Discord.

## Chạy tại máy

Mở `index.html`, hoặc chạy `python -m http.server 8080` tại thư mục này rồi mở `http://localhost:8080`. Dùng máy chủ HTTP để kiểm tra clipboard và đường dẫn tài nguyên. Clipboard tự dùng cách dự phòng nếu trình duyệt không cho truy cập API.

## Sửa nội dung

- Sửa các đoạn giới thiệu, thẻ tính năng, hướng dẫn và hỏi đáp trong `index.html`.
- Đổi màu sắc, kích thước và bố cục trong `style.css`; bảng màu nằm ở `:root`.
- Cấu hình tập trung ở đầu `script.js`: `IP_JAVA`, `IP_BEDROCK`, `CONG_BEDROCK`, `HIEN_IP`, `NGAY_MO`, `DISCORD`.
- `HIEN_IP: false`: ẩn địa chỉ và cổng thực, ẩn nút copy; nút phụ dẫn đến Discord. Đổi thành `true` để công bố IP và bật copy Java, Bedrock, cổng riêng.
- `NGAY_MO: null`: chỉ hiển thị “Sắp ra mắt”. Đặt chuỗi ISO có múi giờ, ví dụ `'2026-12-20T19:00:00+07:00'`, để bật đếm ngược. Hết giờ tự đổi thành “Đã mở cửa! Vào chơi ngay”. Ngày sai định dạng được bỏ qua.
- Khi thay Discord, cũng sửa các đường dẫn dự phòng trong `index.html` để hoạt động khi tắt JavaScript. Khi mở chính thức, cập nhật huy hiệu beta, băng thông báo, FAQ và nội dung SEO nếu cần.
- Năm bản quyền tự cập nhật. Trạng thái online là mục tuỳ chọn và không được tích hợp, tránh gọi API khi chưa công bố IP.

## Thay ảnh

Thay `brand/wildrest-logo.png` và `brand/discord-icon-512.png`. Chạy `python -m pip install Pillow fonttools brotli` rồi `python prepare_assets.py` để tạo lại logo WebP 900/520px, PNG dự phòng, favicon, biểu tượng Apple 180px và ảnh chia sẻ 1200×630. Script chuẩn bị ảnh dùng font Arial trên Windows. Đây chỉ là công cụ biên tập tài nguyên; website không cần chạy Python khi deploy.

Logo dùng `srcset` để chọn ảnh phù hợp màn hình. Không đưa ảnh gốc hơn 2 MB trực tiếp vào HTML. `assets/og.jpg` là ảnh chia sẻ, không tải khi người dùng mở trang. Font có giấy phép OFL lưu kèm trong `assets`.

## Đưa lên GitHub Pages

1. Tạo repository **public**, ví dụ `wildrest-web`, trong tài khoản GitHub của bạn.
2. Đưa các tệp lên nhánh `main`, giữ `index.html`, `CNAME`, `.nojekyll` tại thư mục gốc. Nếu dùng Git: `git init -b main`, `git add .`, `git commit -m "Create WildRest coming soon website"`, thêm remote của repo rồi `git push -u origin main`.
3. **Settings → Pages → Source: Deploy from a branch → main / (root) → Save**.
4. **Custom domain** nhập `wildrest.vn`. File `CNAME` đã chứa đúng tên miền này.
5. Trỏ DNS theo phần dưới. Sau khi kiểm tra DNS thành công, bật **Enforce HTTPS**. Chứng chỉ và DNS có thể cần đến 24 giờ.

Hướng dẫn và IP đã đối chiếu [tài liệu GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## DNS ở ZoneDNS / Nhân Hòa

**Giữ nguyên** CNAME `discord` → `cname.vercel-dns.com` và CNAME `_f5924420…` của Sectigo. Không xoá bản ghi xác minh SSL đã mua.

Sau khi thêm custom domain vào GitHub Pages, thay các bản ghi A / URL Redirect cũ **của riêng `@`** nếu chúng trỏ nơi khác, rồi thêm:

| Loại  | Tên | Giá trị                            |
| ----- | --- | ---------------------------------- |
| A     | @   | 185.199.108.153                    |
| A     | @   | 185.199.109.153                    |
| A     | @   | 185.199.110.153                    |
| A     | @   | 185.199.111.153                    |
| CNAME | www | `rootofgenius.github.io` |

Không thêm tên repo vào giá trị CNAME `www`. IPv6 tuỳ chọn: thêm bốn AAAA tại `@`: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.

`play.wildrest.vn` dành riêng cho máy chủ game, sẽ trỏ A về IP host game (có thể thêm SRV). **Không trỏ `play` vào GitHub Pages.** Người quản lý tên miền thực hiện DNS trong ZoneDNS.

## Kiểm tra

Kiểm tra tại các chiều rộng 360, 390, 768, 1024 và 1440px; thử menu bằng bàn phím, accordion, giảm chuyển động và copy IP khi bật cờ. Thử ngày tương lai / quá khứ. Không có biểu mẫu, đăng nhập hoặc thanh toán.

Đã kiểm tra bằng Chrome headless ở cả năm chiều rộng, không cuộn ngang; menu/Escape, accordion, copy và fallback, ngày tương lai/quá khứ/sai định dạng, giảm chuyển động và trang 404 đều qua. Chạy lại bằng `python -m pip install playwright` rồi `python verify_site.py` trong khi máy chủ cục bộ đang chạy (cần Chrome cài sẵn).

Lighthouse 12.8.2 trên máy chủ cục bộ, giả lập mobile: **Performance 92 / Accessibility 100 / SEO 100**. Tài nguyên ban đầu khoảng **290 KB**. Kết quả thực tế có thể thay đổi theo host và mạng; báo cáo, ảnh kiểm tra nằm trong `.qa/` (không đưa lên Git). Font tiêu đề dùng **VT323** vì đã kiểm tra đủ glyph tiếng Việt; Pixelify Sans thiếu dấu trong bộ font được cung cấp. Font nội dung là Be Vietnam Pro.
