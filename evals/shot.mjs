// usage: node shot.mjs <mock.html> <out.png> [width height]
// Exact-viewport screenshot through the DevTools protocol (headless Brave), reduced motion, fonts settled.
import { spawn } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { tmpdir } from "node:os";

const [mock, out, w = "1280", h = "800"] = process.argv.slice(2);
const B = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser";
const port = 9300 + Math.floor(Math.random() * 500);
const prof = mkdtempSync(resolve(tmpdir(), "shot-"));
const br = spawn(B, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${port}`,
  `--user-data-dir=${prof}`, "--no-first-run", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send("Emulation.setDeviceMetricsOverride", { width: +w, height: +h, deviceScaleFactor: 1, mobile: false });
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await send("Page.enable");
await send("Page.navigate", { url: pathToFileURL(resolve(mock)).href });
await sleep(2500);
await send("Runtime.evaluate", { expression: "document.fonts.ready.then(()=>1)", awaitPromise: true });
await sleep(500);
const shot = await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: +w, height: +h, scale: 1 } });
writeFileSync(out, Buffer.from(shot.result.data, "base64"));
ws.close(); br.kill();
