// Vercel Serverless Function: newsletter signup -> Resend contact in segment.
// Sends NO email. Secrets come only from env (RESEND_API_KEY, RESEND_SEGMENT_ID).
const ORIGINS = new Set([
  "https://nyxk7.github.io",
  "https://ai-tools-nav-seven-pearl.vercel.app",
]);
const EMAIL_RE = /^[^\s@<>()",;:]{1,64}@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$/;
const hits = new Map(); // best-effort per-instance rate limit
const WINDOW = 10 * 60 * 1000, MAX = 5;

function limited(ip) {
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter((t) => now - t < WINDOW);
  arr.push(now);
  hits.set(ip, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > MAX;
}

module.exports = async (req, res) => {
  const origin = req.headers.origin || "";
  if (ORIGINS.has(origin) || /^https:\/\/ai-tools-[a-z0-9-]+-dk-b199\.vercel\.app$/.test(origin)) {
    res.setHeader("Access-Control-Allow-Origin", origin);
    res.setHeader("Vary", "Origin");
    res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    res.setHeader("Access-Control-Max-Age", "86400");
  }
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "POST") return res.status(405).json({ ok: false, msg: "仅支持 POST" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};
  // Honeypot: bots fill hidden "website" field; pretend success.
  if (body.website) return res.status(200).json({ ok: true, msg: "订阅成功" });

  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ ok: false, msg: "请求过于频繁，请稍后再试" });

  const email = String(body.email || "").trim().toLowerCase();
  if (email.length > 254 || !EMAIL_RE.test(email))
    return res.status(400).json({ ok: false, msg: "邮箱格式不正确" });

  const key = process.env.RESEND_API_KEY, seg = process.env.RESEND_SEGMENT_ID;
  if (!key || !seg) return res.status(500).json({ ok: false, msg: "服务未配置" });
  const H = { Authorization: `Bearer ${key}`, "Content-Type": "application/json" };
  try {
    const c = await fetch("https://api.resend.com/contacts", {
      method: "POST", headers: H, body: JSON.stringify({ email, unsubscribed: false }),
    });
    if (!c.ok && c.status !== 409) {
      const t = await c.text();
      if (!/already exists/i.test(t)) { console.error("create", c.status, t.slice(0, 200)); throw 0; }
    }
    const s = await fetch(`https://api.resend.com/contacts/${encodeURIComponent(email)}/segments/${seg}`, {
      method: "POST", headers: H,
    });
    if (!s.ok) { console.error("segment", s.status, (await s.text()).slice(0, 200)); throw 0; }
    return res.status(200).json({ ok: true, msg: "订阅成功，感谢关注！" });
  } catch {
    return res.status(502).json({ ok: false, msg: "订阅失败，请稍后再试" });
  }
};
