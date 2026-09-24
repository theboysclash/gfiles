/**
 * Capture screenshot thumbnails for the bundled games.
 *
 * These thumbnails are used as the card artwork on the /games page. They are
 * committed to the repo (gfiles/thumbnails/), so you only need to run this when
 * adding new games or refreshing previews.
 *
 * Requirements:
 *   - The site must be running locally (npm start) on BASE (default :8080).
 *   - A Chrome/Chromium binary (set CHROME_PATH if it isn't auto-detected).
 *   - puppeteer-core (installed as a devDependency).
 *
 * Usage:
 *   npm start                     # in one terminal
 *   npm run thumbnails            # in another
 *   npm run thumbnails -- 2048,chess --force
 */
import puppeteer from "puppeteer-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const BASE = process.env.BASE || "http://localhost:8080";
const CHROME =
  process.env.CHROME_PATH ||
  "/usr/local/bin/google-chrome" ||
  "/usr/bin/google-chrome";
const HTML5_DIR = path.join(ROOT, "gfiles/html5");
const OUT_HTML5 = path.join(ROOT, "gfiles/thumbnails/html5");
const OUT_ROOT = path.join(ROOT, "gfiles/thumbnails");
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const args = process.argv.slice(2);
const force = args.includes("--force");
const only = args.find((a) => !a.startsWith("--"))?.split(",") || null;

fs.mkdirSync(OUT_HTML5, { recursive: true });

const launchOpts = {
  headless: "new",
  executablePath: CHROME,
  args: ["--no-sandbox", "--disable-dev-shm-usage", "--hide-scrollbars"],
  defaultViewport: { width: 800, height: 600 },
};

let browser = await puppeteer.launch(launchOpts);
let sinceRestart = 0;

async function ensureBrowser() {
  if (!browser || !browser.connected || sinceRestart >= 6) {
    try {
      if (browser) await browser.close();
    } catch {}
    browser = await puppeteer.launch(launchOpts);
    sinceRestart = 0;
  }
}

async function shoot(url, outFile) {
  await ensureBrowser();
  sinceRestart++;
  const page = await browser.newPage();
  await page.setViewport({ width: 800, height: 600 });
  try {
    await page.goto(url, { waitUntil: "networkidle2", timeout: 20000 });
  } catch {}
  await sleep(4000);
  await page.screenshot({
    path: outFile,
    type: "jpeg",
    quality: 72,
    clip: { x: 0, y: 0, width: 800, height: 600 },
  });
  await page.close();
  return fs.statSync(outFile).size;
}

async function withRetries(label, url, outFile) {
  if (!force && fs.existsSync(outFile)) {
    console.log(`${label}: skip (exists)`);
    return;
  }
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const size = await shoot(url, outFile);
      console.log(`${label}: ${(size / 1024).toFixed(0)}KB`);
      return;
    } catch (e) {
      console.log(`${label}: attempt ${attempt} failed (${e.message.split("\n")[0]})`);
      try {
        if (browser) await browser.close();
      } catch {}
      browser = null;
      await sleep(500);
    }
  }
  console.log(`${label}: FAILED`);
}

// webretro
if (!only || only.includes("webretro") || only.includes("rarch")) {
  await withRetries("webretro", `${BASE}/gfiles/rarch/`, path.join(OUT_ROOT, "rarch.jpg"));
}

// HTML5 games
let games = fs
  .readdirSync(HTML5_DIR, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name)
  .sort();
if (only) games = games.filter((g) => only.includes(g));

for (const game of games) {
  await withRetries(
    game,
    `${BASE}/gfiles/html5/${game}/`,
    path.join(OUT_HTML5, `${game}.jpg`)
  );
}

try {
  await browser.close();
} catch {}
console.log("Done.");
