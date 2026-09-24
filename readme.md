# Proxy & Games

A custom web proxy powered by [Ultraviolet](https://github.com/titaniumnetwork-dev/Ultraviolet)
(the modern wisp / bare-mux / epoxy stack) bundled together with a large
collection of HTML5, Flash (via [ruffle](https://ruffle.rs/)) and retro games
(via [webretro](https://github.com/BinBashBanana/webretro)).

## Running

Requires Node.js 20+.

```sh
npm install
npm start
```

Then open <http://localhost:8080>:

- `/` — the Ultraviolet web proxy.
- `/games` — the bundled games list (served from `list.html`).

Set the `PORT` environment variable to change the listen port (defaults to `8080`).

## How it works

`server.js` is an Express + wisp server that:

- serves the proxy frontend from `public/`;
- serves the Ultraviolet, epoxy-transport and bare-mux vendor scripts at
  `/uv/`, `/epoxy/` and `/baremux/`;
- terminates the wisp WebSocket used by the proxy transport at `/wisp/`;
- serves the games from `gfiles/` (with `list.html` at `/games`).

The proxy frontend and its vendor assets are served with cross-origin isolation
headers (required by Ultraviolet's transport). The static games are served
without those headers.

## Games list

The games list (`list.html`) is generated from the contents of `gfiles/` by the
included Python script:

```sh
python3 compiler.py   # or: npm run compile
```

swfs are [here](https://github.com/BinBashBanana/gstore).

---

This was forked from [LQ16's repository](https://github.com/LQ16/gfiles), which is long deleted.
