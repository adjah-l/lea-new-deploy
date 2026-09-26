import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const BOOK_TITLE = "Interpreting His Word";
const BOOK_FILENAME = "Interpreting His Word - Lawrence E. Adjah.pdf";
const BOOK_PATH = resolve(process.cwd(), "assets/resources/interpreting-his-word.pdf");
const RESEND_API = "https://api.resend.com";

const escapeHtml = (value = "") => String(value)
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&#039;");

const normalizeText = (value = "") => String(value).normalize("NFKC").replace(/\s+/g, " ").trim();

const resendRequest = async (path, body, idempotencyKey) => {
  const headers = {
    Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
    "Content-Type": "application/json"
  };
  if (idempotencyKey) headers["Idempotency-Key"] = idempotencyKey;
  const response = await fetch(`${RESEND_API}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body)
  });
  if (!response.ok) throw new Error(`Resend ${path} returned ${response.status}`);
  return response.json();
};

const confirmationEmail = ({ firstName, email, bookBase64 }) => ({
  from: process.env.RESOURCE_FROM_EMAIL,
  to: [email],
  reply_to: "la@lawrenceadjah.com",
  subject: "Your copy of Interpreting His Word",
  text: `Hi ${firstName},\n\nThank you for requesting Interpreting His Word. Your complete digital copy is attached.\n\nThis book is designed to help you read Scripture with a gospel lens and use the TOOLS Bible Study Framework for yourself. Read it with your Bible open, a pen in hand, and—if possible—someone with whom you can grow.\n\nContinue growing:\n- iToro: pray live with people around the world — https://itoro-app.com\n- Family Dinner Foundation: join a family group rooted in mutual care — https://ourfamilydinner.org\n- mbio powered by Family Dinner Foundation: meet people and fellowship in real time — https://mbio.ourfamilydinner.org\n- MaKairos: a Scripture meditation and internalization tool — coming soon at https://makairos.app\n\nI would love to hear what stands out and what questions come up. Simply reply to this email.\n\nWith gratitude,\nLawrence E. Adjah\n\nYou received this because you requested the book and agreed to related updates. Reply “unsubscribe” at any time to stop receiving them.`,
  html: `<div style="font-family:Arial,sans-serif;max-width:620px;margin:0 auto;color:#171412;line-height:1.65"><p>Hi ${escapeHtml(firstName)},</p><p>Thank you for requesting <strong>Interpreting His Word</strong>. Your complete digital copy is attached.</p><p>This book is designed to help you read Scripture with a gospel lens and use the TOOLS Bible Study Framework for yourself. Read it with your Bible open, a pen in hand, and—if possible—someone with whom you can grow.</p><h2 style="font-size:20px;margin-top:30px">Continue growing</h2><p><strong><a href="https://itoro-app.com">iToro</a></strong><br>Pray live with people around the world.</p><p><strong><a href="https://ourfamilydinner.org">Family Dinner Foundation</a></strong><br>Join a family group rooted in mutual care.</p><p><strong><a href="https://mbio.ourfamilydinner.org">mbio powered by Family Dinner Foundation</a></strong><br>Meet people and fellowship in real time.</p><p><strong><a href="https://makairos.app">MaKairos</a></strong><br>A Scripture meditation and internalization tool. Coming soon.</p><p>I would love to hear what stands out and what questions come up. Simply reply to this email.</p><p>With gratitude,<br><strong>Lawrence E. Adjah</strong></p><hr style="border:0;border-top:1px solid #ddd;margin:30px 0"><p style="font-size:12px;color:#777">You received this because you requested the book and agreed to related updates. Reply “unsubscribe” at any time to stop receiving them.</p></div>`,
  attachments: [{ filename: BOOK_FILENAME, content: bookBase64 }],
  tags: [{ name: "resource", value: "interpreting-his-word" }]
});

const followUpEmail = ({ firstName, email }) => ({
  from: process.env.RESOURCE_FROM_EMAIL,
  to: [email],
  reply_to: "la@lawrenceadjah.com",
  subject: "How is Interpreting His Word going?",
  scheduled_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  text: `Hi ${firstName},\n\nI wanted to check in: how is Interpreting His Word going?\n\nWhat are you enjoying? What questions have come up? Is there a passage you are seeing differently after using the gospel lens or the TOOLS framework? I would genuinely love to hear—reply directly to this note.\n\nWe are also developing additional resources for Bible reading, prayer, and fasting. In the meantime:\n- Pray with a global community through iToro: https://itoro-app.com\n- Join a family group rooted in mutual care through Family Dinner Foundation: https://ourfamilydinner.org\n- Meet people and fellowship in real time through mbio powered by Family Dinner Foundation: https://mbio.ourfamilydinner.org\n- Watch for MaKairos, a Scripture meditation and internalization tool: https://makairos.app\n\nGrace and peace,\nLawrence E. Adjah\n\nReply “unsubscribe” if you no longer want these updates.`,
  html: `<div style="font-family:Arial,sans-serif;max-width:620px;margin:0 auto;color:#171412;line-height:1.65"><p>Hi ${escapeHtml(firstName)},</p><p>I wanted to check in: <strong>how is Interpreting His Word going?</strong></p><p>What are you enjoying? What questions have come up? Is there a passage you are seeing differently after using the gospel lens or the TOOLS framework? I would genuinely love to hear—reply directly to this note.</p><p>We are also developing additional resources for Bible reading, prayer, and fasting. In the meantime:</p><ul><li>Pray with a global community through <a href="https://itoro-app.com">iToro</a>.</li><li>Join a family group rooted in mutual care through <a href="https://ourfamilydinner.org">Family Dinner Foundation</a>.</li><li>Meet people and fellowship in real time through <a href="https://mbio.ourfamilydinner.org">mbio powered by Family Dinner Foundation</a>.</li><li>Watch for <a href="https://makairos.app">MaKairos</a>, a Scripture meditation and internalization tool.</li></ul><p>Grace and peace,<br><strong>Lawrence E. Adjah</strong></p><hr style="border:0;border-top:1px solid #ddd;margin:30px 0"><p style="font-size:12px;color:#777">Reply “unsubscribe” if you no longer want these updates.</p></div>`,
  tags: [{ name: "campaign", value: "interpreting-his-word-follow-up" }]
});

const enrollReader = async ({ firstName, lastName, email, phone, city, stateRegion, country, bookBase64 }) => {
  if (!process.env.RESEND_API_KEY || !process.env.RESOURCE_FROM_EMAIL) return false;
  const keyBase = createHash("sha256").update(email.toLowerCase()).digest("hex").slice(0, 24);

  try {
    await resendRequest("/contacts", {
      email,
      first_name: firstName,
      last_name: lastName,
      unsubscribed: false
    });
  } catch (error) {
    console.warn("Could not create or update Resend contact", error);
  }

  if (process.env.RESEND_SEGMENT_ID) {
    try {
      await resendRequest(`/segments/${process.env.RESEND_SEGMENT_ID}/contacts`, { email });
    } catch (error) {
      console.warn("Could not add reader to Resend segment", error);
    }
  }

  if (process.env.RESOURCE_CAMPAIGN_WEBHOOK_URL) {
    try {
      await fetch(process.env.RESOURCE_CAMPAIGN_WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          full_name: `${firstName} ${lastName}`,
          email,
          phone,
          city,
          state_region: stateRegion,
          country,
          country_code: country,
          resource: BOOK_TITLE,
          source: "lawrenceadjah.com/books",
          campaign: "interpreting-his-word-readers"
        })
      });
    } catch (error) {
      console.warn("Could not notify campaign webhook", error);
    }
  }

  await resendRequest("/emails", confirmationEmail({ firstName, email, bookBase64 }), `ihw-confirmation-${keyBase}`);
  await resendRequest("/emails", followUpEmail({ firstName, email }), `ihw-follow-up-${keyBase}`);
  return true;
};

export default async (request) => {
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405, headers: { Allow: "POST" } });
  }

  const rawBody = await request.text();
  if (rawBody.length > 10000) return new Response("Request too large", { status: 413 });
  const form = new URLSearchParams(rawBody);
  const firstName = normalizeText(form.get("first-name"));
  const lastName = normalizeText(form.get("last-name"));
  const email = (form.get("email") || "").trim().toLowerCase();
  const rawPhone = (form.get("phone") || "").trim();
  const phone = (form.get("phone-e164") || "").trim();
  const city = normalizeText(form.get("city"));
  const stateRegion = normalizeText(form.get("state-region"));
  const country = (form.get("country") || "").trim().toUpperCase();
  const resource = (form.get("resource") || "").trim();
  const consent = form.get("email-consent") === "yes";
  const honeypot = (form.get("company") || "").trim();

  if (honeypot) return new Response("Accepted", { status: 202 });
  const validText = (value, max) => value.length > 0 && value.length <= max;
  const normalizedPhone = phone || (rawPhone.startsWith("+") ? `+${rawPhone.replace(/\D/g, "")}` : "");
  if (!validText(firstName, 80) || !validText(lastName, 80) || !/^\S+@\S+\.\S+$/.test(email) || !/^\+[1-9]\d{6,14}$/.test(normalizedPhone) || !validText(city, 100) || !validText(stateRegion, 100) || !/^[A-Z]{2}$/.test(country) || resource !== BOOK_TITLE || !consent) {
    return new Response("First name, last name, valid email, international phone number, city, state or region, country, and consent are required.", { status: 400 });
  }

  try {
    const book = await readFile(BOOK_PATH);
    const bookBase64 = book.toString("base64");
    let confirmationSent = false;
    try {
      confirmationSent = await enrollReader({ firstName, lastName, email, phone: normalizedPhone, city, stateRegion, country, bookBase64 });
    } catch (error) {
      console.error("Reader email enrollment failed", error);
    }

    return new Response(book, {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": `attachment; filename="${BOOK_FILENAME}"`,
        "Cache-Control": "private, no-store, max-age=0",
        "X-Content-Type-Options": "nosniff",
        "X-Confirmation-Email": confirmationSent ? "sent" : "not-configured"
      }
    });
  } catch (error) {
    console.error("Book delivery failed", error);
    return new Response("The book is temporarily unavailable.", { status: 503 });
  }
};

export const config = { path: "/api/resource-download" };
