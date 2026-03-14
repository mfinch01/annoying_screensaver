const timeEl = document.getElementById("time");
const dateEl = document.getElementById("date");
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");
const video = document.getElementById("bg-video");

function updateClock() {
  const now = new Date();

  const time = now.toLocaleTimeString("ru-RU", {
    hour: "2-digit",
    minute: "2-digit"
  });

  const date = now.toLocaleDateString("ru-RU", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric"
  });

  timeEl.textContent = time;
  dateEl.textContent = date.charAt(0).toUpperCase() + date.slice(1);
}

updateClock();
setInterval(updateClock, 1000);

const chars = "01アイウエオカキクケコサシスセソABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&*+-=<>/\\";
let columns = [];
let fontSize = 16;
let drops = [];

function setupMatrix() {
  const rect = canvas.getBoundingClientRect();
  const colCount = Math.floor(rect.width / fontSize);

  columns = Array.from({ length: colCount }, (_, i) => i * fontSize);
  drops = Array.from({ length: colCount }, () => Math.random() * -100);
}

function resizeCanvas() {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();

  canvas.width = Math.floor(rect.width * dpr);
  canvas.height = Math.floor(rect.height * dpr);

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  setupMatrix();
}

function drawMatrix() {
  const rect = canvas.getBoundingClientRect();

  ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
  ctx.fillRect(0, 0, rect.width, rect.height);

  ctx.font = `${fontSize}px "JetBrains Mono", "Ubuntu Mono", monospace`;
  ctx.textBaseline = "top";

  for (let i = 0; i < columns.length; i++) {
    const x = columns[i];
    const y = drops[i] * fontSize;
    const tailLength = 18 + Math.floor(Math.random() * 10);

    for (let j = 0; j < tailLength; j++) {
      const ch = chars[Math.floor(Math.random() * chars.length)];
      const yy = y - j * fontSize;

      if (yy < -fontSize || yy > rect.height + fontSize) continue;

      if (j === 0) {
        ctx.fillStyle = "rgba(234, 255, 239, 0.95)";
      } else {
        const alpha = Math.max(0.06, 0.8 - j * 0.045);
        ctx.fillStyle = `rgba(99,255,143,${alpha})`;
      }

      ctx.fillText(ch, x, yy);
    }

    drops[i] += 0.55 + Math.random() * 0.65;

    if (y - tailLength * fontSize > rect.height + 40) {
      drops[i] = Math.random() * -25 - 5;
    }
  }

  requestAnimationFrame(drawMatrix);
}

window.addEventListener("resize", resizeCanvas);
resizeCanvas();
requestAnimationFrame(drawMatrix);

video.play().catch(() => {});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    window.close();
  }
});