const CAU_HINH = {
  IP_JAVA: "play.wildrest.vn",
  IP_BEDROCK: "play.wildrest.vn",
  CONG_BEDROCK: 19132,
  HIEN_IP: false,
  NGAY_MO: null, // Ví dụ: '2026-12-20T19:00:00+07:00'
  DISCORD: "https://discord.wildrest.vn",
  DISCORD_GUILD_ID: "1568170875491192842",
  MANG_XA_HOI: { tiktok: "", facebook: "", youtube: "" },
};

const ANH_MAY_CHU = [
  {
    src: "assets/gallery/anh-01.webp",
    width: 1918,
    height: 973,
    alt: "Tháp đá nhìn từ con phố gỗ treo đèn lồng",
    chuThich: "Dạo phố dưới chân tháp đá",
  },
  {
    src: "assets/gallery/anh-02.webp",
    width: 1792,
    height: 883,
    alt: "Người chơi đứng cạnh dãy siêu xe ngoài quảng trường",
    chuThich: "Hẹn bạn bè lái xe quanh sảnh",
  },
  {
    src: "assets/gallery/anh-03.webp",
    width: 1667,
    height: 889,
    alt: "Người chơi mặc giáp có cánh đứng cạnh rồng băng trên đồng cỏ",
    chuThich: "Bộ Cơ Giáp Pha Lê và rồng băng",
  },
  {
    src: "assets/gallery/anh-04.webp",
    width: 1799,
    height: 971,
    alt: "Dãy trưng bày trang bị cạnh boong tàu gỗ",
    chuThich: "Ghé khu trưng bày trang bị",
  },
  {
    src: "assets/gallery/anh-05.webp",
    width: 1859,
    height: 970,
    alt: "Người chơi đeo cánh lấp lánh bay trên tán rừng",
    chuThich: "Một đôi cánh giữa trời WildRest",
  },
  {
    src: "assets/gallery/anh-06.webp",
    width: 1918,
    height: 979,
    alt: "Người chơi đứng cạnh xe trắng đỗ bên hiên nhà",
    chuThich: "Dừng xe trước hiên nhà",
  },
];

const CAP_NHAT = [
  {
    ngay: "2026-11-09",
    tieuDe: "Dungeon & bộ Cơ Giáp Pha Lê",
    noiDung: [
      "Đánh trùm cuối Dungeon để săn Lõi Pha Lê.",
      "Bộ Cơ Giáp Pha Lê có cánh sau lưng. Kiếm phóng bánh xe xoay và gọi rồng băng.",
      "Thêm dụng cụ bậc Pha Lê.",
    ],
  },
  {
    ngay: "2026-11-09",
    tieuDe: "Nông trại theo mùa & nội thất",
    noiDung: [
      "Trồng 10 loại cây theo mùa và giao đơn hàng cho Thương Lái.",
      "Hơn 140 món nội thất để trang trí, có ghế và sofa ngồi được.",
    ],
  },
  {
    ngay: "2026-11-09",
    tieuDe: "Câu cá & cân bằng",
    noiDung: [
      "Ghé Lão Ngư để khám phá cần câu 4 bậc.",
      "Kiếm mọi bậc mạnh hơn. Dungeon xuất hiện nhiều quái hơn.",
    ],
  },
];

// Chỉ tải nền đêm khi người xem sắp cuộn tới phần tính năng.
const features = document.getElementById("tinh-nang");
if ("IntersectionObserver" in window) {
  const backgroundObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        features.classList.add("background-ready");
        backgroundObserver.disconnect();
      }
    },
    { rootMargin: "200px" },
  );
  backgroundObserver.observe(features);
} else {
  features.classList.add("background-ready");
}

document.querySelectorAll("[data-discord]").forEach((link) => {
  link.href = CAU_HINH.DISCORD;
});
document.getElementById("year").textContent = new Date().getFullYear();

const timeline = document.querySelector("#update-list");
if (CAP_NHAT.length) {
  const template = timeline.firstElementChild;
  timeline.replaceChildren(
    ...CAP_NHAT.map(({ ngay, tieuDe, noiDung }) => {
      const article = template.cloneNode(true);
      const date = article.querySelector("time");
      date.dateTime = ngay;
      date.textContent = `${ngay.slice(8, 10)}/${ngay.slice(5, 7)}`;
      article.querySelector("h3").textContent = tieuDe;
      article.querySelector("ul").replaceChildren(
        ...noiDung.map((line) => {
          const item = document.createElement("li");
          item.textContent = line;
          return item;
        }),
      );
      return article;
    }),
  );
}

const gallery = document.querySelector("#gallery-grid");
const lightbox = document.querySelector("#gallery-lightbox");
const lightboxImage = lightbox.querySelector("img");
const lightboxCaption = lightbox.querySelector("figcaption");
let currentPhoto = 0;
let galleryTrigger;
let swipeStart;

function showPhoto(index) {
  currentPhoto = (index + ANH_MAY_CHU.length) % ANH_MAY_CHU.length;
  const photo = ANH_MAY_CHU[currentPhoto];
  lightboxImage.alt = photo.alt;
  lightboxImage.width = photo.width;
  lightboxImage.height = photo.height;
  lightboxImage.src = photo.src;
  lightboxCaption.textContent = `${photo.chuThich} · ${currentPhoto + 1}/${ANH_MAY_CHU.length}`;
}

document.querySelector("#anh").hidden = !ANH_MAY_CHU.length;
document.querySelector('#menu a[href="#anh"]').hidden = !ANH_MAY_CHU.length;
const photoTemplate = document.querySelector("#gallery-item");
ANH_MAY_CHU.forEach(({ src, alt, chuThich, width, height }, index) => {
  const item = photoTemplate.content.cloneNode(true);
  const button = item.querySelector("button");
  const img = item.querySelector("img");
  img.alt = alt;
  img.width = width;
  img.height = height;
  img.sizes =
    "(max-width: 639px) calc(100vw - 40px), (max-width: 1000px) calc((100vw - 68px) / 2), 374px";
  if (width > 640) {
    img.srcset = `${src.replace(/\.webp$/i, "-640.webp")} 640w, ${src} ${width}w`;
  }
  img.src = src;
  button.setAttribute("aria-label", `Mở ảnh: ${alt}`);
  item.querySelector("figcaption").textContent = chuThich;
  button.addEventListener("click", () => {
    galleryTrigger = button;
    showPhoto(index);
    lightbox.showModal();
  });
  gallery.append(item);
});

lightbox
  .querySelector("[data-close]")
  .addEventListener("click", () => lightbox.close());
lightbox
  .querySelector("[data-prev]")
  .addEventListener("click", () => showPhoto(currentPhoto - 1));
lightbox
  .querySelector("[data-next]")
  .addEventListener("click", () => showPhoto(currentPhoto + 1));
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) lightbox.close();
});
lightbox.addEventListener("close", () => {
  swipeStart = null;
  lightboxImage.removeAttribute("src");
  galleryTrigger.focus({ preventScroll: true });
});
lightbox.addEventListener("keydown", (event) => {
  if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
  event.preventDefault();
  showPhoto(currentPhoto + (event.key === "ArrowLeft" ? -1 : 1));
});
lightboxImage.addEventListener("pointerdown", (event) => {
  if (event.pointerType !== "touch" || !event.isPrimary) return;
  swipeStart = { x: event.clientX, y: event.clientY };
  lightboxImage.setPointerCapture(event.pointerId);
});
lightboxImage.addEventListener("pointerup", (event) => {
  if (!swipeStart || !event.isPrimary) return;
  const dx = event.clientX - swipeStart.x;
  const dy = event.clientY - swipeStart.y;
  swipeStart = null;
  if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy))
    showPhoto(currentPhoto + (dx < 0 ? 1 : -1));
});
lightboxImage.addEventListener("pointercancel", () => {
  swipeStart = null;
});

const ownerAvatar = document.querySelector(".owner-avatar");
function hideOwnerAvatar() {
  ownerAvatar.hidden = true;
}
ownerAvatar.addEventListener("error", hideOwnerAvatar);
if (ownerAvatar.complete && ownerAvatar.naturalWidth === 0) hideOwnerAvatar();

const menuButton = document.querySelector(".menu-toggle");
const menu = document.getElementById("menu");
function closeMenu() {
  menuButton.setAttribute("aria-expanded", "false");
  menu.classList.remove("open");
}
menuButton.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  menu.classList.toggle("open", open);
});
menu
  .querySelectorAll("a")
  .forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menu.classList.contains("open")) {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener("click", (event) => {
  if (!event.target.closest(".header")) closeMenu();
});

let toastTimer;
function notify(message, detail) {
  const toast = document.getElementById("toast");
  toast.querySelector("strong").textContent = message;
  toast.querySelector("small").textContent = detail;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2500);
}
async function copyText(value) {
  let copied = false;
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(String(value));
      copied = true;
    } catch {
      /* Thử cách dự phòng bên dưới. */
    }
  }
  if (!copied) {
    const previousFocus = document.activeElement;
    const field = document.createElement("textarea");
    field.value = String(value);
    field.setAttribute("readonly", "");
    field.style.cssText =
      "position:fixed;left:0;top:0;opacity:0;font-size:16px";
    document.body.append(field);
    field.focus();
    field.select();
    field.setSelectionRange(0, field.value.length);
    try {
      copied = document.execCommand("copy");
    } catch {
      copied = false;
    }
    field.remove();
    previousFocus?.focus({ preventScroll: true });
  }
  notify(
    copied ? "Đã copy!" : "Chưa sao chép được",
    copied
      ? "Sẵn sàng cho chuyến phiêu lưu."
      : `Bạn có thể chép thủ công: ${value}`,
  );
}
if (CAU_HINH.HIEN_IP) {
  document.querySelector('[data-ip="java"]').textContent = CAU_HINH.IP_JAVA;
  document.querySelector('[data-ip="bedrock"]').textContent =
    CAU_HINH.IP_BEDROCK;
  document.getElementById("bedrock-port").textContent = CAU_HINH.CONG_BEDROCK;
  const values = {
    java: CAU_HINH.IP_JAVA,
    bedrock: CAU_HINH.IP_BEDROCK,
    port: CAU_HINH.CONG_BEDROCK,
  };
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.hidden = false;
    button.addEventListener("click", () =>
      copyText(values[button.dataset.copy]),
    );
  });
  const heroIP = document.getElementById("hero-ip");
  heroIP.textContent = "Copy IP";
  heroIP.href = "#cach-vao";
  heroIP.addEventListener("click", (event) => {
    event.preventDefault();
    copyText(CAU_HINH.IP_JAVA);
  });
}

if (CAU_HINH.NGAY_MO) {
  const target = new Date(CAU_HINH.NGAY_MO).getTime();
  if (Number.isFinite(target)) {
    const countdown = document.getElementById("countdown");
    const units = ["ngày", "giờ", "phút", "giây"];
    countdown.innerHTML = units
      .map(
        (unit) =>
          `<div class="time-block"><strong>00</strong><span>${unit}</span></div>`,
      )
      .join("");
    const digits = countdown.querySelectorAll("strong");
    function tick() {
      const remaining = Math.max(0, Math.floor((target - Date.now()) / 1000));
      if (!remaining) {
        document.getElementById("launch-status").textContent =
          "Đã mở cửa! Vào chơi ngay";
        countdown.hidden = true;
        return false;
      }
      countdown.hidden = false;
      [
        Math.floor(remaining / 86400),
        Math.floor(remaining / 3600) % 24,
        Math.floor(remaining / 60) % 60,
        remaining % 60,
      ].forEach((value, index) => {
        digits[index].textContent = String(value).padStart(2, "0");
      });
      return true;
    }
    if (tick()) {
      const timer = setInterval(() => {
        if (!tick()) clearInterval(timer);
      }, 1000);
    }
  }
}

// Số người trực tuyến do Discord cung cấp; không ước lượng hoặc hiển thị khi lỗi.
async function updateDiscordPresence() {
  if (!/^\d+$/.test(CAU_HINH.DISCORD_GUILD_ID)) return;
  try {
    const response = await fetch(
      `https://discord.com/api/guilds/${CAU_HINH.DISCORD_GUILD_ID}/widget.json`,
      { signal: AbortSignal.timeout(6000) },
    );
    if (!response.ok) return;
    const data = await response.json();
    if (!Number.isInteger(data.presence_count) || data.presence_count < 0)
      return;
    const presence = document.getElementById("discord-presence");
    presence.textContent = `${data.presence_count.toLocaleString("vi-VN")} người đang trực tuyến trên Discord`;
    presence.hidden = false;
  } catch {
    /* Widget chưa bật hoặc lỗi mạng: giữ dòng thống kê ẩn. */
  }
}
updateDiscordPresence();

document.querySelectorAll("[data-social]").forEach((link) => {
  const value = CAU_HINH.MANG_XA_HOI[link.dataset.social];
  if (!value) return;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:") return;
    link.href = url.href;
    link.target = "_blank";
    link.rel = "noopener";
    link.hidden = false;
  } catch {
    /* Bỏ qua liên kết chưa hợp lệ. */
  }
});

const motion = window.matchMedia("(prefers-reduced-motion: reduce)");
if (!motion.matches && "IntersectionObserver" in window) {
  document.documentElement.classList.add("js-motion");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.08 },
  );
  document
    .querySelectorAll(".reveal")
    .forEach((element) => observer.observe(element));
  const sparks = document.querySelector(".sparks");
  for (let i = 0; i < 16; i++) {
    const spark = document.createElement("i");
    spark.style.left = `${15 + ((i * 37) % 70)}%`;
    spark.style.animationDelay = `${i * -0.7}s`;
    spark.style.animationDuration = `${6 + (i % 5)}s`;
    sparks.append(spark);
  }
}
