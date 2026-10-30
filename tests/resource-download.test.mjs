import test from 'node:test';
import assert from 'node:assert/strict';
import handler from '../netlify/functions/resource-download.mjs';
const fields = { 'first-name': 'QA', 'last-name': 'Test', email: 'qa@example.com', phone: '+12025550100', city: 'Test', 'state-region': 'Test', country: 'US', resource: 'Interpreting His Word', 'email-consent': 'yes' };
const request = (changes = {}) => new Request('https://example.com/api/resource-download', { method: 'POST', body: new URLSearchParams({...fields, ...changes}) });

test('rejects invalid requests and honeypot submissions without sending email', async () => {
  globalThis.fetch = async () => { throw new Error('Unexpected network call'); };
  assert.equal((await handler(new Request('https://example.com'))).status, 405);
  assert.equal((await handler(request({email:'bad'}))).status, 400);
  assert.equal((await handler(request({'email-consent':''}))).status, 400);
  assert.equal((await handler(request({company:'bot'}))).status, 202);
});
test('delivers real PDF and sends owner notification independently of follow-up failure', async () => {
  process.env.RESEND_API_KEY = 'local-test'; process.env.RESOURCE_FROM_EMAIL = 'test@example.com';
  const messages = [];
  globalThis.fetch = async (url, options) => {
    const body = JSON.parse(options.body); messages.push(body);
    return new Response(JSON.stringify({id:'test'}), {status: body.scheduled_at ? 500 : 200});
  };
  const response = await handler(request());
  assert.equal(response.status, 200);
  assert.equal(response.headers.get('X-Owner-Notification'), 'sent');
  assert.equal(response.headers.get('X-Confirmation-Email'), 'sent');
  assert.match(response.headers.get('Content-Disposition'), /Interpreting His Word.*\.pdf/);
  const bytes = Buffer.from(await response.arrayBuffer());
  assert.equal(bytes.subarray(0,5).toString(), '%PDF-');
  assert.ok(bytes.length > 2000000);
  const owner = messages.find(m => m.subject?.startsWith('Book requested'));
  assert.deepEqual(owner.to, ['lawrence@lawrenceadjah.com']);
  assert.match(owner.text, /qa@example.com/);
});
test('email outage never prevents PDF access', async () => {
  globalThis.fetch = async () => new Response('{}', {status:503});
  const response = await handler(request());
  assert.equal(response.status,200);
  assert.equal(response.headers.get('X-Owner-Notification'),'failed');
  assert.equal(response.headers.get('Content-Type'),'application/pdf');
});
