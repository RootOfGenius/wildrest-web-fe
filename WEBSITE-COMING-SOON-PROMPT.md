# Prompt: Website "Sắp ra mắt" cho server Minecraft WildRest.vn

> Đưa nguyên file này cho agent AI thực hiện. Agent làm đúng phần **Yêu cầu bắt buộc**, các phần **Gợi ý** thì được tự quyết nếu đẹp hơn.

---

## 0. Vai trò và kết quả cần giao

Bạn là front-end developer kiêm designer. Hãy làm **một trang web tĩnh một trang (single page)** giới thiệu server Minecraft **WildRest.vn** ở trạng thái **"Sắp ra mắt"**, deploy lên **GitHub Pages** với tên miền riêng **`wildrest.vn`**.

Giao lại:
1. Một repo GitHub (public) chứa mã nguồn, chạy được ngay trên GitHub Pages, **không cần bước build** (HTML + CSS + JS thuần, không framework, không npm).
2. File `CNAME` chứa đúng một dòng `wildrest.vn`.
3. File `README.md` ghi: cách sửa nội dung (IP, ngày mở, link), cách thay ảnh, và hướng dẫn trỏ DNS (mục 9).
4. Toàn bộ chữ trên trang bằng **tiếng Việt có dấu**.

---

## 1. Về server (nội dung để viết)

- **Tên:** WildRest.vn
- **Slogan:** "Sinh tồn chill · sống chậm, xây nhà, lái xe dạo"
- **Phiên bản:** Minecraft **Java 1.21.11**, **chơi được cả trên điện thoại / PE (Bedrock)**
- **Thể loại:** Sinh tồn (Survival) Việt hoá, có kinh tế, bang hội, boss, trang bị tự chế
- **Trạng thái:** đang **thử nghiệm (beta)**. Báo lỗi được thưởng khi mở chính thức. Khi mở chính thức sẽ **reset world và toàn bộ dữ liệu**.
- **Discord:** `https://discord.wildrest.vn` (đây là link duy nhất ra ngoài; bấm vào là vào server Discord)
- **Địa chỉ vào game:** chưa chốt. Để **hằng số cấu hình** trong JS, mặc định:
  - Java: `play.wildrest.vn` (cổng mặc định, không cần ghi)
  - Bedrock / PE: `play.wildrest.vn`, cổng `19132`
  - Có cờ `HIEN_IP = false`: khi `false` thì ô IP hiện "Sẽ công bố khi mở cửa" thay vì IP.
- **Ngày mở:** chưa chốt. Hằng số `NGAY_MO = null`. Khi `null` thì không hiện đồng hồ đếm ngược, chỉ hiện chữ "Sắp ra mắt". Khi có ngày (ISO, giờ Việt Nam GMT+7) thì hiện đồng hồ đếm ngược ngày / giờ / phút / giây; hết giờ thì đổi thành "Đã mở cửa! Vào chơi ngay".

**Tính năng nổi bật** (mỗi cái 1 thẻ: biểu tượng, tiêu đề, 1–2 câu mô tả; viết giọng thân thiện, ngắn gọn):

| Tiêu đề | Ý chính |
|---|---|
| Sinh tồn Việt hoá | Map sinh tồn vanilla rộng, toàn bộ menu, vật phẩm, nhiệm vụ đều tiếng Việt |
| ☘ Vận May & Năng Lực | Mỗi cấp kỹ năng tăng Vận May: thu hoạch, đào quặng, chặt gỗ rơi thêm đồ. Xem mọi chỉ số bằng `/nangluc` |
| Trang bị tự rèn | Đổi nông sản, đồ rơi của quái, cá thành Tiên → Khối → Nén để rèn bộ giáp và vũ khí nhiều bậc, có kỹ năng riêng |
| Nông cụ & khoáng cụ | Cuốc chuyên từng loại cây, cúp khai khoáng, rìu tiều phu có bộ đếm, càng dùng càng mạnh |
| Boss & Rồng Ender | Boss Sukuna xuất hiện mỗi ngày, gọi lại Rồng Ender để cày bộ giáp Ender huyền thoại |
| Bang hội | Lập bang, lên cấp bang, quỹ chung, kho chung, nhiệm vụ tuần, liên minh. Bang chiến sắp ra mắt |
| Giải trí | Đua ngựa đặt cược, xổ số, Battle Pass theo mùa, xe hơi lái dạo |
| Chơi trên điện thoại | Vào bằng Minecraft PE / Bedrock, có resource pack riêng cho cả hai bản |
| Chống hack | Hệ thống chống gian lận nhiều lớp, đội ngũ quản trị theo dõi |

**Không** nhắc tới tên plugin (AuraSkills, MMOItems, Grim...), không nhắc tiền thật, nạp thẻ, giá cả, rank donate. Trang chỉ giới thiệu lối chơi.

---

## 2. Cấu trúc trang (từ trên xuống)

1. **Thanh trên cùng (sticky):** logo nhỏ + chữ "WildRest.vn" bên trái; bên phải các mục cuộn tới "Tính năng", "Cách vào", "Hỏi đáp", nút **"Discord"** nổi bật. Trên mobile gom thành nút menu (hamburger) mở ra danh sách.
2. **Hero (màn hình đầu, cao ≥ 100vh trên desktop):**
   - Ảnh logo `assets/logo.webp` ở giữa, có hiệu ứng **bay lên xuống nhẹ** (floating, 6 giây/vòng).
   - Dòng chữ nhỏ trên logo: nhãn "BETA · ĐANG THỬ NGHIỆM" dạng huy hiệu nhấp nháy nhẹ.
   - Tiêu đề lớn: **"Sắp ra mắt"** (font pixel, mục 3).
   - Slogan bên dưới.
   - Đồng hồ đếm ngược (nếu có `NGAY_MO`).
   - 2 nút: **"Tham gia Discord"** (nút chính, màu cam gỗ) và **"Copy IP"** (nút phụ). Bấm Copy IP thì copy vào clipboard và hiện thông báo nhỏ "Đã copy!" kiểu toast của Minecraft (khung đen viền vàng, trượt từ góc phải trên xuống, tự tắt sau 2,5 giây). Nếu `HIEN_IP = false` thì nút này đổi thành "Nhận thông báo khi mở cửa" dẫn tới Discord.
   - Nền: bầu trời hoàng hôn gradient + vài đám mây khối pixel trôi ngang chậm (CSS, lặp vô hạn), dưới đáy là dải cỏ/đất kiểu khối Minecraft (dùng CSS hoặc SVG vẽ ô vuông, không cần ảnh).
3. **Dải thông báo beta:** băng ngang nền vàng nhạt viền đậm: "Máy chủ đang thử nghiệm: tìm ra lỗi và báo trên Discord để nhận **thưởng** khi mở chính thức. Lúc mở chính thức sẽ **reset** world và dữ liệu."
4. **Tính năng:** lưới thẻ (mục 1). Desktop 3 cột, tablet 2 cột, mobile 1 cột. Mỗi thẻ nhìn như **ô trong túi đồ Minecraft** (nền xám đá, viền sáng trên-trái, viền tối dưới-phải, góc vuông), hover thì nâng lên 4px và viền phát sáng màu nhấn của thẻ. Biểu tượng trên mỗi thẻ: emoji hoặc SVG pixel tự vẽ (không dùng ảnh có bản quyền Mojang).
5. **Cách vào server:** 2 cột (mobile xếp dọc): **Java** và **Bedrock/PE**, mỗi cột ghi các bước 1-2-3, ô IP (và cổng cho Bedrock) có nút copy riêng. Ghi chú: "Vào lần đầu sẽ được hỏi tải resource pack, hãy chọn Đồng ý".
6. **Trạng thái server (tuỳ chọn, gợi ý):** thẻ nhỏ hiện Online/Offline và số người đang chơi, lấy từ `https://api.mcsrvstat.us/3/<địa chỉ Java>` mỗi 60 giây. Nếu lỗi mạng hoặc `HIEN_IP = false` thì ẩn thẻ này, không báo lỗi.
7. **Hỏi đáp (FAQ):** dạng accordion (bấm mở/đóng), 5–6 câu:
   - Server có miễn phí không? → Có, vào chơi miễn phí.
   - Chơi bằng điện thoại được không? → Được, dùng Minecraft PE/Bedrock.
   - Phiên bản nào? → Java 1.21.11; Bedrock bản mới nhất.
   - Bao giờ mở chính thức? → Theo dõi Discord để biết ngày mở.
   - Dữ liệu bản thử nghiệm có giữ không? → Không, sẽ reset khi mở chính thức; người báo lỗi được thưởng.
   - Báo lỗi ở đâu? → Kênh báo lỗi trên Discord.
8. **Kêu gọi cuối trang:** khối lớn "Cùng chờ ngày mở cửa nhé!" + nút Discord.
9. **Footer:** © năm hiện tại WildRest.vn · "Không liên kết với Mojang/Microsoft" · link Discord.

---

## 3. Phong cách thiết kế

**Cảm giác:** ấm áp, vui, "chill", nhiều màu nhưng dễ đọc. Lấy cảm hứng trực tiếp từ logo: đảo cỏ lơ lửng, lửa trại, đèn lồng, bầu trời hoàng hôn, chữ gỗ cam.

**Bảng màu** (khai báo bằng CSS variables trong `:root`):

| Biến | Mã | Dùng cho |
|---|---|---|
| `--troi-tren` | `#8ec5ff` | gradient trời (trên) |
| `--troi-duoi` | `#ffd2a6` | gradient trời (dưới, hoàng hôn) |
| `--go` | `#f08a24` | màu chính, nút chính, tiêu đề |
| `--go-dam` | `#8a4a1c` | viền chữ, bóng chữ |
| `--co` | `#5fbf3a` | màu phụ, điểm nhấn xanh |
| `--co-dam` | `#2f6e1f` | viền khối cỏ |
| `--dat` | `#7a5232` | dải đất |
| `--den-long` | `#ffd34d` | phát sáng, huy hiệu |
| `--nuoc` | `#3fa9f5` | nhấn phụ |
| `--da` | `#2b2d36` | nền thẻ, nền khối tối |
| `--chu` | `#fff8ee` | chữ trên nền tối |
| `--chu-toi` | `#2a1a0e` | chữ trên nền sáng |

Mỗi thẻ tính năng có 1 màu nhấn riêng xoay vòng: cỏ, nước, đèn lồng, gỗ, tím `#b06cff`, hồng `#ff6fa8`.

**Font** (Google Fonts):
- Tiêu đề và nhãn ngắn: **"Pixelify Sans"** hoặc **"Silkscreen"** (pixel, có hỗ trợ tiếng Việt). Phải kiểm tra dấu tiếng Việt hiển thị đúng (ví dụ "Sắp ra mắt", "Bang hội"); font nào lỗi dấu thì đổi font khác, **không** để dấu bị rơi.
- Nội dung: **"Be Vietnam Pro"** (rất dễ đọc với tiếng Việt), cỡ chữ thân tối thiểu 16px.

**Chi tiết kiểu Minecraft:**
- Nút bấm: khối vuông góc, viền 3px, bóng đổ cứng dưới-phải (không blur); bấm vào thì lún xuống 2px.
- Chữ tiêu đề lớn có viền tối và bóng cứng giống chữ trong logo.
- Đường phân cách giữa các phần là dải khối cỏ/đất vẽ bằng CSS.
- Con trỏ bình thường (không đổi cursor lạ).

**Hiệu ứng (nhẹ, không làm chậm):**
- Mây trôi, logo bay nhẹ, vài **hạt sáng** (đom đóm/tàn lửa) bay lên chậm ở hero (≤ 25 hạt, CSS hoặc canvas nhẹ).
- Các phần xuất hiện mờ dần khi cuộn tới (IntersectionObserver).
- Tôn trọng `prefers-reduced-motion`: tắt mọi chuyển động khi người dùng bật giảm chuyển động.

---

## 4. Yêu cầu bắt buộc

- **Responsive:** đẹp và không cuộn ngang ở 360px, 390px, 768px, 1024px, 1440px. Mobile-first. Lề hai bên tối thiểu 16px trên mobile. Nút bấm cao tối thiểu 44px.
- **Hiệu năng:** tổng dung lượng tải lần đầu < 1,5 MB. Ảnh logo nén sang **WebP** (rộng 900px cho desktop, 520px cho mobile bằng `srcset`), kèm bản PNG dự phòng. Không dùng thư viện JS nặng; nếu cần thì chỉ một file JS tự viết.
- **Dễ đọc:** tương phản chữ/nền đạt WCAG AA. Chữ không đặt trực tiếp lên ảnh nhiều chi tiết (phải có lớp nền mờ phía sau).
- **SEO và chia sẻ:**
  - `<html lang="vi">`, `<title>WildRest.vn · Server Minecraft sinh tồn Việt · Sắp ra mắt</title>`.
  - `meta description` tiếng Việt.
  - Open Graph và Twitter card dùng ảnh `assets/og.jpg` (1200×630, tạo từ logo + chữ "Sắp ra mắt").
  - `favicon.ico`, `apple-touch-icon.png` (180×180) tạo từ logo.
- **Truy cập:** mọi ảnh có `alt`. Accordion và menu dùng được bằng bàn phím. Có `:focus-visible` rõ ràng.
- **Không** dùng ảnh, texture, logo chính thức của Mojang/Minecraft. Chỉ dùng logo của WildRest (tệp đính kèm) và hình tự vẽ bằng CSS/SVG.
- **Không** có form thu thập email, đăng nhập hay thanh toán.
- Cấu hình tập trung ở đầu file `script.js`:
  ```js
  const CAU_HINH = {
    IP_JAVA: 'play.wildrest.vn',
    IP_BEDROCK: 'play.wildrest.vn',
    CONG_BEDROCK: 19132,
    HIEN_IP: false,
    NGAY_MO: null, // ví dụ '2026-12-20T19:00:00+07:00'
    DISCORD: 'https://discord.wildrest.vn',
  };
  ```

## 5. Cấu trúc thư mục

```
/
├─ index.html
├─ style.css
├─ script.js
├─ CNAME              (một dòng: wildrest.vn)
├─ 404.html           (trang lạc đường kiểu Minecraft "Bạn đã chết! ... Hồi sinh" → nút về trang chủ)
├─ README.md
└─ assets/
   ├─ logo.webp, logo-520.webp, logo.png
   ├─ og.jpg
   ├─ favicon.ico, apple-touch-icon.png
```

## 6. Tài nguyên đính kèm

- `wildrest-logo.png` (1254×1254, ~2 MB): logo chính, cảnh đảo cỏ lơ lửng lúc hoàng hôn, chữ "WILDREST .VN" gỗ cam. **Phải nén** trước khi dùng.
- `discord-icon-512.png`: biểu tượng server Discord (có thể dùng làm favicon nếu đẹp hơn).

(Người dùng sẽ gửi kèm 2 tệp này; nằm ở `_kir-tools/brand/` trong thư mục server.)

## 7. Kiểm tra trước khi giao

- Mở thử ở Chrome desktop và giả lập iPhone SE / Galaxy S (DevTools), không vỡ bố cục, không cuộn ngang.
- Dấu tiếng Việt hiển thị đúng ở mọi font.
- Nút Copy IP chạy trên mobile (dùng `navigator.clipboard`, có dự phòng `document.execCommand('copy')`).
- Lighthouse mobile: Performance ≥ 90, Accessibility ≥ 95, SEO ≥ 95.
- Không lỗi trong Console.

## 8. Deploy lên GitHub Pages

1. Tạo repo, ví dụ `wildrest-web`, đẩy mã lên nhánh `main`.
2. Repo → **Settings → Pages**: Source = "Deploy from a branch", Branch = `main` / `(root)`.
3. Mục **Custom domain** điền `wildrest.vn`, lưu. Đợi kiểm tra DNS xong thì tick **Enforce HTTPS**.

## 9. Trỏ DNS (người dùng tự làm ở ZoneDNS / Nhân Hòa; ghi rõ trong README)

Tên miền đang quản lý ở ZoneDNS. **Giữ nguyên** các bản ghi đang có:
- CNAME `discord` → `cname.vercel-dns.com` (trang chuyển hướng Discord, đừng xoá);
- CNAME `_f5924420…` của Sectigo (xác minh SSL đã mua, đừng xoá).

Thêm cho trang chủ:

| Loại | Tên | Giá trị |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `<tên-tài-khoản-github>.github.io` |

(Tuỳ chọn IPv6: AAAA `@` → `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.)

Nếu `@` đang có bản ghi A hoặc URL Redirect khác thì xoá trước. Sau khi DNS cập nhật (vài phút tới vài giờ), GitHub tự cấp HTTPS.

> **Lưu ý cho sau này:** khi server lên host riêng, `play.wildrest.vn` sẽ là bản ghi A (và có thể SRV) trỏ về IP máy chủ game, **không** trỏ vào GitHub Pages. Không đặt `play` thành CNAME tới GitHub.
