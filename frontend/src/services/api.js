/*
  src/services/api.ts

  Small helper that centralizes API calls to the backend. Keeping network
  requests in one place makes the app easier to maintain and to test.

  Behavior:
  - Reads `VITE_BACKEND_URL` from `import.meta.env` when present. This lets
    the same code run in both development (with Vite) and production builds.
  - Falls back to a relative `/api/interview/chat` path when `VITE_BACKEND_URL`
    is empty (this is the standard for same-origin production deployments).

  For beginners: call `chat(profile, targetRole, history)` from components
  to send data to the backend. The function returns the parsed JSON response
  or throws an Error when the request fails.
*/
export async function chat(profile, target_role, history) {
    const form = new FormData();
    form.append('profile', profile);
    form.append('target_role', target_role);
    form.append('history', history);
    // import.meta.env.* are replaced by Vite at build/dev time.
    const base = (import.meta.env.VITE_BACKEND_URL || '').replace(/\/$/, '');
    // If base is set use absolute URL, otherwise use relative path for same-origin
    const url = base ? `${base}/api/interview/chat` : '/api/interview/chat';
    const res = await fetch(url, { method: 'POST', body: form });
    if (!res.ok) {
        const text = await res.text();
        throw new Error(text);
    }
    return res.json();
}
