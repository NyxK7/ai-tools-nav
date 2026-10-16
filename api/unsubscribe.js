// Vercel Serverless Function: newsletter unsubscribe -> delete Resend contact.
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
  if (body.website) return res.status(200).json({ ok: true, msg: "已退订" });
  const ip = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim() || "unknown";
  if (limited(ip)) return res.status(429).json({ ok: false, msg: "请求过于频繁，请稍后再试" });
  const email = String(body.email || "").trim().toLowerCase();
  if (email.length > 254 || !EMAIL_RE.test(email))
    return res.status(400).json({ ok: false, msg: "邮箱格式不正确" });
  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(500).json({ ok: false, msg: "服务未配置" });
  try {
    const r = await fetch(`https://api.resend.com/contacts/${encodeURIComponent(email)}`, {
      method: "DELETE", headers: { Authorization: `Bearer ${key}` },
    });
    if (!r.ok && r.status !== 404) { console.error("delete", r.status); throw 0; }
    // Same reply whether or not the address existed (no enumeration).
    return res.status(200).json({ ok: true, msg: "已退订，您的邮箱已从订阅列表删除" });
  } catch {
    return res.status(502).json({ ok: false, msg: "退订失败，请稍后再试" });
  }
};
