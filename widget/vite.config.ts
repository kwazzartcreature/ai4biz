import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
  plugins: [svelte({compilerOptions: {customElement: true}})],
  build: {
    lib: {
      entry: "src/main.ts", // Your Svelte app's entry file
      name: "InchatAIWidget",
      fileName: "inchat-widget",
      formats: ["iife"], // Use IIFE for script-tag inclusion
    },
    outDir: "dist", // Output directory for the bundled code
  },
});
