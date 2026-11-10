import { fileURLToPath, URL } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";

// Dev: /api được proxy sang backend nên trình duyệt không cần cấu hình CORS.
// Đổi địa chỉ backend bằng VITE_PROXY_TARGET (xem .env.example).
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
    },
    server: {
      port: 5173,
      proxy: { "/api": env.VITE_PROXY_TARGET || "http://127.0.0.1:8000" },
    },
  };
});
