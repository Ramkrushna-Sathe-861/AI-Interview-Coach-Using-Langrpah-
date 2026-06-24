import { defineConfig } from 'vite'

// vite.config.ts
// This file configures Vite's dev server. The `server.proxy` option below
// forwards requests from the browser dev server (port 5173) to the backend
// at http://localhost:8000 when the path starts with /api.
//
// Important: this proxy runs only during development (`npm run dev`). The
// production build (vite build) produces static files and does not include
// the proxy logic. In production you should serve the built files from your
// backend or use a reverse proxy such as nginx.
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
