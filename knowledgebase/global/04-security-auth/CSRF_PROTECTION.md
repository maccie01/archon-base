# Research Result: 04_CSRF_PROTECTION


# CSRF Protection

Created: 2025-10-14

Last Updated: 2025-10-14

## What is CSRF?

Cross-Site Request Forgery (CSRF) is an attack that tricks an authenticated user’s browser into sending unintended requests to a web application where the user is logged in. Because the browser automatically includes credentials (cookies, basic auth, etc.), the forged request appears legitimate to the server.

## Real-World Attack Scenario

Consider a banking application (`bank.com`) where users are authenticated via session cookies. An attacker hosts a malicious page (`attacker.com`) with the following HTML:

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">xml</div></div><div><span><code><span class="token token punctuation"><</span><span class="token token">img</span><span class="token token"></span><span class="token token">src</span><span class="token token attr-value punctuation attr-equals">=</span><span class="token token attr-value punctuation">"</span><span class="token token attr-value">https://bank.com/api/transfer?amount=1000&to=attacker</span><span class="token token attr-value punctuation">"</span><span class="token token"></span><span class="token token punctuation">/></span><span>
</span></code></span></div></div></div></pre>

When a logged-in user on `bank.com` visits `attacker.com`, their browser issues a GET request to `bank.com/api/transfer`, including valid session cookies. The bank processes the request, transferring funds to the attacker’s account without the user’s consent.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="No line wrap" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l10 0 M4 18l10 0 M4 12h17l-3 -3m0 6l3 -3"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">text</div></div><div><span><code><span><span>flowchart LR
</span></span><span>    A[User on bank.com] -->|Authenticated| B[Session Cookie]
</span><span>    C[User visits attacker.com] --> D[Malicious Image Tag]
</span><span>    D -->|Browser auto-sends| E[bank.com/api/transfer?amount=1000]
</span><span>    E --> F[Funds transferred]
</span><span></span></code></span></div></div></div></pre>

## How CSRF Attacks Work

1. **Victim Authentication** : User logs into `bank.com`, obtaining session cookies.
2. **Victim Visits Malicious Site** : Attacker lures user to `attacker.com`.
3. **Forged Request** : Malicious page triggers a request to `bank.com` endpoint.
4. **Automatic Credential Inclusion** : Browser attaches session cookies.
5. **Server Processes Request** : Bank thinks it’s a valid user action.

## CSRF vs. XSS

* **CSRF** exploits the browser’s trust in authenticated users by forging requests.
* **XSS** exploits the application’s trust in user-supplied data to execute scripts in the browser.

CSRF requires no script execution on the vulnerable site and leverages automatic credential sending. XSS requires injecting malicious script payloads.

---

## CSRF Protection Strategies

## Synchronizer Token Pattern

A server-generated, cryptographically secure token is embedded in HTML forms. On form submission, the token is validated against the user’s session.

* **When to Use** : Traditional multi-page apps with server-rendered forms.
* **Advantages** : Strong protection; tokens tied to session.
* **Disadvantages** : Requires session state; additional token management server-side.

## Double-Submit Cookie Pattern

Server issues a CSRF token in a cookie and expects the same token in a request parameter or header.

* **When to Use** : Stateless APIs where sessions are not used.
* **Advantages** : Stateless; no server-side token storage.
* **Disadvantages** : Relies on cookie confidentiality; attacker cannot read cookie due to Same-Origin Policy.

## SameSite Cookie Attribute

Modern browsers support `SameSite` attribute on cookies to restrict cross-site sending.

* **When to Use** : Any cookie-based auth.
* **Advantages** : Simple configuration; no code changes in request handling.
* **Disadvantages** : Older browsers may lack support; may break legitimate cross-site flows.

## Custom Request Headers

APIs expect a custom header (e.g., `X-Requested-With`) on all state-changing requests.

* **When to Use** : AJAX-based apps.
* **Advantages** : Simple; no token generation.
* **Disadvantages** : Some cross-origin contexts may strip custom headers; not foolproof.

## Origin/Referer Header Validation

Server checks the `Origin` or `Referer` header on state-changing requests.

* **When to Use** : Secure contexts where these headers are reliably sent.
* **Advantages** : No tokens; lightweight.
* **Disadvantages** : Some browsers or proxies may omit or modify headers.

## Comparison Table

| Strategy                     | Requires State | Stateless | Complexity | Coverage         |
| ---------------------------- | -------------- | --------- | ---------- | ---------------- |
| Synchronizer Token Pattern   | Yes            | No        | Medium     | Forms and APIs   |
| Double-Submit Cookie Pattern | No             | Yes       | Low        | APIs only        |
| SameSite Cookie Attribute    | No             | Yes       | Low        | Cookies globally |
| Custom Request Headers       | No             | Yes       | Low        | AJAX APIs        |
| Origin/Referer Validation    | No             | Yes       | Low        | Browsers only    |

---

## SameSite Cookie Attribute

Browser support for `SameSite` is now widespread.

## SameSite=Strict

Cookie is never sent on cross-site requests.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span>app</span><span class="token token punctuation">.</span><span class="token token">use</span><span class="token token punctuation">(</span><span class="token token">session</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span>
</span><span>  secret</span><span class="token token operator">:</span><span> process</span><span class="token token punctuation">.</span><span>env</span><span class="token token punctuation">.</span><span class="token token constant">SESSION_SECRET</span><span class="token token operator">!</span><span class="token token punctuation">,</span><span>
</span><span>  cookie</span><span class="token token operator">:</span><span></span><span class="token token punctuation">{</span><span>
</span><span>    httpOnly</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    secure</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    sameSite</span><span class="token token operator">:</span><span></span><span class="token token">'strict'</span><span class="token token punctuation">,</span><span>
</span><span>    maxAge</span><span class="token token operator">:</span><span></span><span class="token token">86400000</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

 **Impact** : Prevents all cross-site cookies. Might break legitimate third-party integrations.

## SameSite=Lax

Cookie is sent on top-level GET navigations (safe by default).

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span>app</span><span class="token token punctuation">.</span><span class="token token">use</span><span class="token token punctuation">(</span><span class="token token">session</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span>
</span><span>  secret</span><span class="token token operator">:</span><span> process</span><span class="token token punctuation">.</span><span>env</span><span class="token token punctuation">.</span><span class="token token constant">SESSION_SECRET</span><span class="token token operator">!</span><span class="token token punctuation">,</span><span>
</span><span>  cookie</span><span class="token token operator">:</span><span></span><span class="token token punctuation">{</span><span>
</span><span>    httpOnly</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    secure</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    sameSite</span><span class="token token operator">:</span><span></span><span class="token token">'lax'</span><span class="token token punctuation">,</span><span>
</span><span>    maxAge</span><span class="token token operator">:</span><span></span><span class="token token">86400000</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

 **Impact** : Good default; allows basic navigation (e.g., links) but blocks less safe contexts.

## SameSite=None

Cookie is sent in all contexts, but must specify `secure`.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span>app</span><span class="token token punctuation">.</span><span class="token token">use</span><span class="token token punctuation">(</span><span class="token token">session</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span>
</span><span>  secret</span><span class="token token operator">:</span><span> process</span><span class="token token punctuation">.</span><span>env</span><span class="token token punctuation">.</span><span class="token token constant">SESSION_SECRET</span><span class="token token operator">!</span><span class="token token punctuation">,</span><span>
</span><span>  cookie</span><span class="token token operator">:</span><span></span><span class="token token punctuation">{</span><span>
</span><span>    httpOnly</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    secure</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span>
</span><span>    sameSite</span><span class="token token operator">:</span><span></span><span class="token token">'none'</span><span class="token token punctuation">,</span><span>
</span><span>    maxAge</span><span class="token token operator">:</span><span></span><span class="token token">86400000</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

 **Implications** : Enables third-party usage; must be sent over HTTPS; susceptible to CSRF unless additional measures applied.

---

## Token-Based Protection

## CSRF Token Generation

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span class="token token">import</span><span> crypto </span><span class="token token">from</span><span></span><span class="token token">'crypto'</span><span class="token token punctuation">;</span><span>
</span>
<span></span><span class="token token">function</span><span></span><span class="token token">generateCsrfToken</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token operator">:</span><span></span><span class="token token">string</span><span></span><span class="token token punctuation">{</span><span>
</span><span></span><span class="token token">return</span><span> crypto</span><span class="token token punctuation">.</span><span class="token token">randomBytes</span><span class="token token punctuation">(</span><span class="token token">32</span><span class="token token punctuation">)</span><span class="token token punctuation">.</span><span class="token token">toString</span><span class="token token punctuation">(</span><span class="token token">'hex'</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span></code></span></div></div></div></pre>

Tokens should be:

* Unique per session or request.
* Stored server-side (session) or encoded in signed JWT.
* Rotated periodically.

## Token Validation

On state-changing requests (POST, PUT, DELETE), extract token from header or body and compare to stored session token.

## Token Expiration and Rotation

* Invalidate token on logout.
* Rotate on each sensitive operation if required.
* Use short lifetimes to limit exposure.

## Storage Locations

* **Hidden Form Field** : `<input type="hidden" name="_csrf" value="{{token}}" />`
* **Request Header** : `X-CSRF-Token: <token>`

---

## Express.js Implementation

## Using csurf Middleware (Traditional Forms)

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span class="token token">import</span><span> express </span><span class="token token">from</span><span></span><span class="token token">'express'</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">import</span><span> session </span><span class="token token">from</span><span></span><span class="token token">'express-session'</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">import</span><span> csrf </span><span class="token token">from</span><span></span><span class="token token">'csurf'</span><span class="token token punctuation">;</span><span>
</span>
<span></span><span class="token token">const</span><span> app </span><span class="token token operator">=</span><span></span><span class="token token">express</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span>
<span>app</span><span class="token token punctuation">.</span><span class="token token">use</span><span class="token token punctuation">(</span><span class="token token">session</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span>
</span><span>  secret</span><span class="token token operator">:</span><span> process</span><span class="token token punctuation">.</span><span>env</span><span class="token token punctuation">.</span><span class="token token constant">SESSION_SECRET</span><span class="token token operator">!</span><span class="token token punctuation">,</span><span>
</span><span>  cookie</span><span class="token token operator">:</span><span></span><span class="token token punctuation">{</span><span> httpOnly</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span> secure</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span class="token token punctuation">,</span><span> sameSite</span><span class="token token operator">:</span><span></span><span class="token token">'lax'</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span>
<span></span><span class="token token">const</span><span> csrfProtection </span><span class="token token operator">=</span><span></span><span class="token token">csrf</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span> cookie</span><span class="token token operator">:</span><span></span><span class="token token boolean">true</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span>
<span>app</span><span class="token token punctuation">.</span><span class="token token">get</span><span class="token token punctuation">(</span><span class="token token">'/form'</span><span class="token token punctuation">,</span><span> csrfProtection</span><span class="token token punctuation">,</span><span></span><span class="token token punctuation">(</span><span>req</span><span class="token token punctuation">,</span><span> res</span><span class="token token punctuation">)</span><span></span><span class="token token operator">=></span><span></span><span class="token token punctuation">{</span><span>
</span><span>  res</span><span class="token token punctuation">.</span><span class="token token">render</span><span class="token token punctuation">(</span><span class="token token">'form'</span><span class="token token punctuation">,</span><span></span><span class="token token punctuation">{</span><span> csrfToken</span><span class="token token operator">:</span><span> req</span><span class="token token punctuation">.</span><span class="token token">csrfToken</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span>
<span>app</span><span class="token token punctuation">.</span><span class="token token">post</span><span class="token token punctuation">(</span><span class="token token">'/process'</span><span class="token token punctuation">,</span><span> csrfProtection</span><span class="token token punctuation">,</span><span></span><span class="token token punctuation">(</span><span>req</span><span class="token token punctuation">,</span><span> res</span><span class="token token punctuation">)</span><span></span><span class="token token operator">=></span><span></span><span class="token token punctuation">{</span><span>
</span><span>  res</span><span class="token token punctuation">.</span><span class="token token">send</span><span class="token token punctuation">(</span><span class="token token">'Data processed'</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

## Custom CSRF Middleware

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span class="token token">import</span><span></span><span class="token token punctuation">{</span><span> Request</span><span class="token token punctuation">,</span><span> Response</span><span class="token token punctuation">,</span><span> NextFunction </span><span class="token token punctuation">}</span><span></span><span class="token token">from</span><span></span><span class="token token">'express'</span><span class="token token punctuation">;</span><span>
</span>
<span></span><span class="token token">function</span><span></span><span class="token token">csrfProtection</span><span class="token token punctuation">(</span><span>req</span><span class="token token operator">:</span><span> Request</span><span class="token token punctuation">,</span><span> res</span><span class="token token operator">:</span><span> Response</span><span class="token token punctuation">,</span><span> next</span><span class="token token operator">:</span><span> NextFunction</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">{</span><span>
</span><span></span><span class="token token">const</span><span> safeMethods </span><span class="token token operator">=</span><span></span><span class="token token punctuation">[</span><span class="token token">'GET'</span><span class="token token punctuation">,</span><span></span><span class="token token">'HEAD'</span><span class="token token punctuation">,</span><span></span><span class="token token">'OPTIONS'</span><span class="token token punctuation">]</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">if</span><span></span><span class="token token punctuation">(</span><span>safeMethods</span><span class="token token punctuation">.</span><span class="token token">includes</span><span class="token token punctuation">(</span><span>req</span><span class="token token punctuation">.</span><span>method</span><span class="token token punctuation">)</span><span class="token token punctuation">)</span><span></span><span class="token token">return</span><span></span><span class="token token">next</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span>
<span></span><span class="token token">const</span><span> token </span><span class="token token operator">=</span><span> req</span><span class="token token punctuation">.</span><span>headers</span><span class="token token punctuation">[</span><span class="token token">'x-csrf-token'</span><span class="token token punctuation">]</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">const</span><span> sessionToken </span><span class="token token operator">=</span><span> req</span><span class="token token punctuation">.</span><span>session</span><span class="token token punctuation">.</span><span>csrfToken</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">if</span><span></span><span class="token token punctuation">(</span><span class="token token operator">!</span><span>token </span><span class="token token operator">||</span><span> token </span><span class="token token operator">!==</span><span> sessionToken</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">{</span><span>
</span><span></span><span class="token token">return</span><span> res</span><span class="token token punctuation">.</span><span class="token token">status</span><span class="token token punctuation">(</span><span class="token token">403</span><span class="token token punctuation">)</span><span class="token token punctuation">.</span><span class="token token">json</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span> error</span><span class="token token operator">:</span><span></span><span class="token token">'Invalid CSRF token'</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token">next</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span>
<span></span><span class="token token">// Token issuance middleware (attach at login)</span><span>
</span><span></span><span class="token token">function</span><span></span><span class="token token">issueCsrfToken</span><span class="token token punctuation">(</span><span>req</span><span class="token token operator">:</span><span> Request</span><span class="token token punctuation">,</span><span> res</span><span class="token token operator">:</span><span> Response</span><span class="token token punctuation">,</span><span> next</span><span class="token token operator">:</span><span> NextFunction</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">{</span><span>
</span><span>  req</span><span class="token token punctuation">.</span><span>session</span><span class="token token punctuation">.</span><span>csrfToken </span><span class="token token operator">=</span><span></span><span class="token token">generateCsrfToken</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token">next</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span></code></span></div></div></div></pre>

## SameSite Cookie Configuration

Refer to examples in the SameSite section above for `strict`, `lax`, and `none`.

---

## CSRF Protection for SPAs

## JWT/Bearer Token Approach

Bearer tokens in `Authorization` headers are not automatically sent by browsers, making CSRF attacks ineffective.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span class="token token">// Frontend</span><span>
</span><span></span><span class="token token">const</span><span> token </span><span class="token token operator">=</span><span> localStorage</span><span class="token token punctuation">.</span><span class="token token">getItem</span><span class="token token punctuation">(</span><span class="token token">'token'</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span>axios</span><span class="token token punctuation">.</span><span>defaults</span><span class="token token punctuation">.</span><span>headers</span><span class="token token punctuation">.</span><span>common</span><span class="token token punctuation">[</span><span class="token token">'Authorization'</span><span class="token token punctuation">]</span><span></span><span class="token token operator">=</span><span></span><span class="token token template-string template-punctuation">`</span><span class="token token template-string">Bearer </span><span class="token token template-string interpolation interpolation-punctuation punctuation">${</span><span class="token token template-string interpolation">token</span><span class="token token template-string interpolation interpolation-punctuation punctuation">}</span><span class="token token template-string template-punctuation">`</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

## Custom Header Validation

Require `X-Requested-With` or other custom header on all state-changing AJAX calls.

<pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">typescript</div></div><div><span><code><span class="token token">// Backend</span><span>
</span><span></span><span class="token token">function</span><span></span><span class="token token">validateCustomHeader</span><span class="token token punctuation">(</span><span>req</span><span class="token token operator">:</span><span> Request</span><span class="token token punctuation">,</span><span> res</span><span class="token token operator">:</span><span> Response</span><span class="token token punctuation">,</span><span> next</span><span class="token token operator">:</span><span> NextFunction</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">{</span><span>
</span><span></span><span class="token token">if</span><span></span><span class="token token punctuation">(</span><span>req</span><span class="token token punctuation">.</span><span>headers</span><span class="token token punctuation">[</span><span class="token token">'x-requested-with'</span><span class="token token punctuation">]</span><span></span><span class="token token operator">!==</span><span></span><span class="token token">'XMLHttpRequest'</span><span class="token token punctuation">)</span><span></span><span class="token token punctuation">{</span><span>
</span><span></span><span class="token token">return</span><span> res</span><span class="token token punctuation">.</span><span class="token token">status</span><span class="token token punctuation">(</span><span class="token token">403</span><span class="token token punctuation">)</span><span class="token token punctuation">.</span><span class="token token">json</span><span class="token token punctuation">(</span><span class="token token punctuation">{</span><span> error</span><span class="token token operator">:</span><span></span><span class="token token">'Forbidden'</span><span></span><span class="token token punctuation">}</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span><span></span><span class="token token">next</span><span class="token token punctuation">(</span><span class="token token punctuation">)</span><span class="token token punctuation">;</span><span>
</span><span></span><span class="token token punctuation">}</span><span>
</span>
<span></span><span class="token token">// Frontend</span><span>
</span><span>axios</span><span class="token token punctuation">.</span><span>defaults</span><span class="token token punctuation">.</span><span>headers</span><span class="token token punctuation">.</span><span>common</span><span class="token token punctuation">[</span><span class="token token">'X-Requested-With'</span><span class="token token punctuation">]</span><span></span><span class="token token operator">=</span><span></span><span class="token token">'XMLHttpRequest'</span><span class="token token punctuation">;</span><span>
</span></code></span></div></div></div></pre>

## When SPAs Still Need CSRF Protection

* Apps using cookies for auth rather than Bearer tokens.
* Hybrid apps mixing cookie and token auth.
* Third-party scripts requiring cookies.

---

## Security Best Practices

1. Enforce **SameSite** cookies and  **HttpOnly** .
2. Use **CSRF tokens** for all state-changing operations.
3. Validate **Origin** and **Referer** headers.
4. Require **custom headers** on AJAX calls.
5. Rotate and expire tokens regularly.
6. Disallow **GET** for state-changing endpoints.
7. Test endpoints with **missing** or **tampered** tokens.

## Common Pitfalls

## ❌ GET Requests Modifying State

Using GET for transfers can be exploited via image tags or links. Always use POST/PUT/DELETE.

## ❌ Missing CSRF on API Endpoints

Ensure all endpoints altering data enforce protection patterns.

## ❌ Incorrect SameSite Configuration

Using `SameSite=None` without `secure` flag or on HTTP breaks protection.

## ❌ Weak Token Generation

Use cryptographically secure RNG (e.g., `crypto.randomBytes`), not predictable values.

## ❌ Not Validating on State-Changing Operations

Apply middleware consistently across routes.

---

## Testing CSRF Protection

## Manual Testing

1. Attempt a state-changing request without token/header via curl:
   <pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">bash</div></div><div><span><code><span class="token token">curl</span><span> -XPOST https://app.com/api/transfer
   </span></code></span></div></div></div></pre>
2. Expect `403 Forbidden`.
3. Replay with valid token:
   <pre class="not-prose w-full rounded font-mono text-sm font-extralight"><div class="codeWrapper text-light selection:text-super selection:bg-super/10 my-md relative flex flex-col rounded font-mono text-sm font-normal bg-subtler"><div class="translate-y-xs -translate-x-xs bottom-xl mb-xl flex h-0 items-start justify-end md:sticky md:top-[100px]"><div class="overflow-hidden rounded-full border-subtlest ring-subtlest divide-subtlest bg-base"><div class="border-subtlest ring-subtlest divide-subtlest bg-subtler"><button data-testid="toggle-wrap-code-button" aria-label="Wrap lines" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6l16 0 M4 18l5 0 M4 12h13a3 3 0 0 1 0 6h-4l2 -2m0 4l-2 -2"></path></svg></div></div></button><button data-testid="copy-code-button" aria-label="Copy code" type="button" class="focus-visible:bg-subtle hover:bg-subtle text-quiet  hover:text-foreground dark:hover:bg-subtle font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out select-none items-center relative group/button font-semimedium justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square" data-state="closed"><div class="flex items-center min-w-0 gap-two justify-center"><div class="flex shrink-0 items-center justify-center size-4"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" color="currentColor" class="tabler-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1"></path></svg></div></div></button></div></div></div><div class="-mt-xl"><div><div data-testid="code-language-indicator" class="text-quiet bg-subtle py-xs px-sm inline-block rounded-br rounded-tl-[3px] font-thin">bash</div></div><div><span><code><span class="token token">curl</span><span> -XPOST https://app.com/api/transfer </span><span class="token token punctuation">\</span><span>
   </span><span>  -H </span><span class="token token">"X-CSRF-Token: <token>"</span><span></span><span class="token token punctuation">\</span><span>
   </span><span>  -d </span><span class="token token">"amount=100"</span><span>
   </span></code></span></div></div></div></pre>

## Automated Testing

Use integration tests or Postman collections that:

* Omit CSRF tokens to verify rejection.
* Send valid tokens to verify acceptance.
* Change `Origin` or `Referer` headers to invalid domains.

## Browser Developer Tools

* Inspect `Set-Cookie` headers for `SameSite`.
* Monitor requests to verify tokens in headers or form fields.

---

## References

* OWASP CSRF Prevention Cheat Sheet
* MDN Web Docs – SameSite Cookies
* expressjs/csurf npm package
* RFC 6265 – HTTP State Management Mechanism
* OWASP Top Ten – Broken Access Control

---

This document covers both traditional and modern SPA CSRF protection patterns, complete with code examples, configuration guidelines, and testing methodologies.
