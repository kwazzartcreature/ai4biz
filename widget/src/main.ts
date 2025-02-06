import { mount } from "svelte";
import App from "./App.svelte";

declare global {
  interface Window {
    mountInchatWidget: (selector?: string) => void;
  }
}

let app;

(function () {
  function mountInchatWidget(selector = "body") {
    const el = document.querySelector(selector);
    if (!el) {
      console.error(
        `Svelte mount error: No element found for selector "${selector}"`
      );
      return;
    }

    app = mount(App, {
      target: el,
    });
  }

  window.mountInchatWidget = mountInchatWidget;

  if (document.readyState !== "loading") {
    mountInchatWidget();
  } else {
    document.addEventListener("DOMContentLoaded", () => {
      mountInchatWidget();
    });
  }
})();

export default app;
