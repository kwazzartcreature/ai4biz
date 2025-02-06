<svelte:options customElement="inchatai-widget" />

<script lang="ts">
  import ChatButton from "./lib/ui/ChatButton.svelte";
  import ChatWindow from "./lib/ui/ChatWindow.svelte";
  import { onMount, onDestroy } from "svelte";
  import { connectWS } from "./lib/utils/ws";
  import { globalState } from "./lib/state.svelte";

  const checkScreenSize = () => {
    if (window.innerWidth < 1024) {
      globalState.isLargeScreen = false;
    } else {
      globalState.isLargeScreen = true;
    }
  };

  onMount(async () => {
    const res = await fetch("https://inchatai.5dgo.dev/get-token", {
      method: "GET",
      credentials: "include",
    });

    if (!res.ok) {
      throw new Error("Failed to get token");
    }

    connectWS();

    window.addEventListener("resize", checkScreenSize);
  });

  onDestroy(() => {
    window.removeEventListener("resize", checkScreenSize);
  });

  $effect(() => {
    localStorage.setItem("messages", JSON.stringify(globalState.messages));
  });

  // $effect(() => {
  //   if (!globalState.chatWindowOpen || globalState.isLargeScreen) {
  //     document.body.style.overflow = "auto";
  //   } else {
  //     document.body.style.overflow = "hidden";
  //   }
  // });
</script>

<div class="inchat-assistant">
  {#if globalState.firstHandshake}
    <ChatButton
      onclick={() => (globalState.chatWindowOpen = !globalState.chatWindowOpen)}
    />
  {/if}

  {#if globalState.chatWindowOpen && globalState.firstHandshake}
    <ChatWindow bind:chatWindowOpen={globalState.chatWindowOpen} />
  {/if}
</div>

<style>
  :global(.inchat-assistant) {
    font-family: Inter, sans-serif;
    --neutral: #f5f5f5;
    --text: #fff;
    --primary: #f0d58c;
    --primary-dark: #8e7849;
    --primary-gradient: linear-gradient(45deg, #f0d58c, #fde4a1, #f4d68a);
    --dark-gradient: linear-gradient(
      45deg,
      var(--border) 20%,
      var(--text-gold) 76%
    );
    --background: #171717;
    --border: #0a0a0a;
    --text-gold: #333333;
  }

  :global(.inchat-assistant *) {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    z-index: 9999;
  }

  :global(.inchat-assistant button) {
    background-color: transparent;
    border: none;
    cursor: pointer;
  }
</style>
