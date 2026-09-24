"use strict";
/**
 * @type {HTMLFormElement}
 */
const form = document.getElementById("uv-form");
/**
 * @type {HTMLInputElement}
 */
const address = document.getElementById("uv-address");
/**
 * @type {HTMLSelectElement}
 */
const searchEngine = document.getElementById("uv-search-engine");
/**
 * @type {HTMLParagraphElement}
 */
const error = document.getElementById("uv-error");
/**
 * @type {HTMLPreElement}
 */
const errorCode = document.getElementById("uv-error-code");

const overlay = document.getElementById("uv-overlay");
const frame = document.getElementById("uv-frame");
const loading = document.getElementById("uv-loading");
const exitBtn = document.getElementById("uv-exit");
const quickLinks = document.getElementById("quick-links");

const connection = new BareMux.BareMuxConnection("/baremux/worker.js");

function closeFrame() {
  overlay.classList.remove("show");
  frame.src = "about:blank";
  document.body.classList.remove("proxy-open");
}

if (exitBtn) exitBtn.addEventListener("click", closeFrame);

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && overlay.classList.contains("show")) closeFrame();
});

frame.addEventListener("load", () => {
  if (frame.src && frame.src !== "about:blank" && loading)
    loading.textContent = "";
});

if (quickLinks) {
  quickLinks.addEventListener("click", (e) => {
    const btn = e.target.closest(".chip");
    if (!btn) return;
    address.value = btn.dataset.url;
    form.requestSubmit();
  });
}

async function launch(rawInput) {
  error.textContent = "";
  errorCode.textContent = "";

  try {
    await registerSW();
  } catch (err) {
    error.textContent = "Failed to register service worker.";
    errorCode.textContent = err.toString();
    throw err;
  }

  const url = search(rawInput, searchEngine.value);

  overlay.classList.add("show");
  document.body.classList.add("proxy-open");
  if (loading) loading.textContent = "Connecting…";

  const wispUrl =
    (location.protocol === "https:" ? "wss" : "ws") +
    "://" +
    location.host +
    "/wisp/";
  if ((await connection.getTransport()) !== "/epoxy/index.mjs") {
    await connection.setTransport("/epoxy/index.mjs", [{ wisp: wispUrl }]);
  }
  frame.src = __uv$config.prefix + __uv$config.encodeUrl(url);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const value = address.value.trim();
  if (!value) return;
  await launch(value);
});
