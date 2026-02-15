import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), ""); // prefixなしで読む
  const target = env.API_PROXY_TARGET || "http://backend:8000";
  console.log(`API proxy target: ${target}`);

  return {
    plugins: [react()],
    server: {
      host: true,
      port: 5173,
      watch: { usePolling: true, interval: 300 },
      proxy: {
        "/api": {
          target,
          changeOrigin: true,
        },
      },
    },
  };
});
