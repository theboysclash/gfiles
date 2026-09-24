import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { hostname } from "node:os";
import { createServer } from "node:http";
import express from "express";
import wisp from "wisp-server-node";

import { uvPath } from "@titaniumnetwork-dev/ultraviolet";
import { epoxyPath } from "@mercuryworkshop/epoxy-transport";
import { baremuxPath } from "@mercuryworkshop/bare-mux/node";

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();

/**
 * Cross-origin isolation is required by Ultraviolet's transport layer
 * (epoxy/bare-mux use SharedArrayBuffer). It is applied to the proxy frontend
 * and its vendor assets only. The static games are served without it so that
 * any game loading cross-origin assets is not affected.
 */
function crossOriginIsolation(_req, res, next) {
  res.setHeader("Cross-Origin-Opener-Policy", "same-origin");
  res.setHeader("Cross-Origin-Embedder-Policy", "require-corp");
  next();
}

// --- Games (bundled from gfiles) ---
app.use("/gfiles", express.static(join(__dirname, "gfiles")));
app.use("/css", express.static(join(__dirname, "css")));
app.get(["/games", "/games.html", "/list.html"], (_req, res) => {
  res.sendFile(join(__dirname, "list.html"));
});

// --- Ultraviolet proxy frontend + vendor scripts (cross-origin isolated) ---
app.use(crossOriginIsolation);
// Our public frontend is prioritized so our uv.config.js overrides the vendor one.
app.use(express.static(join(__dirname, "public")));
app.use("/uv/", express.static(uvPath));
app.use("/epoxy/", express.static(epoxyPath));
app.use("/baremux/", express.static(baremuxPath));

// Everything else -> 404 page
app.use((_req, res) => {
  res.status(404);
  res.sendFile(join(__dirname, "public", "404.html"));
});

const server = createServer();

server.on("request", (req, res) => {
  app(req, res);
});

server.on("upgrade", (req, socket, head) => {
  if (req.url.endsWith("/wisp/")) {
    wisp.routeRequest(req, socket, head);
    return;
  }
  socket.end();
});

let port = parseInt(process.env.PORT || "");
if (isNaN(port)) port = 8080;

server.on("listening", () => {
  const address = server.address();
  console.log("Listening on:");
  console.log(`\thttp://localhost:${address.port}`);
  console.log(`\thttp://${hostname()}:${address.port}`);
  console.log(
    `\thttp://${
      address.family === "IPv6" ? `[${address.address}]` : address.address
    }:${address.port}`
  );
});

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

function shutdown() {
  console.log("Signal received: closing HTTP server");
  server.close();
  process.exit(0);
}

server.listen({ port });
