<script lang="ts">
  import { fly } from "svelte/transition";
  import Chat from "../../assets/icons/Chat.svelte";
  import { globalState } from "../state.svelte";
  interface Props {
    onclick: () => void;
  }

  const { onclick }: Props = $props();
</script>

<button
  transition:fly
  {onclick}
  class={`chat-button ${globalState.chatWindowOpen ? "chat-button_active" : ""}`}
>
  <Chat />
</button>

<style>
  .chat-button {
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid var(--border);
    position: fixed;
    font-weight: bold;
    bottom: 1rem;
    right: 1rem;
    padding: 1.5rem;
    border-radius: 50%;
    background-color: #262626;
    transition: 0.2s ease-in-out;
  }

  .chat-button:hover {
    border-color: var(--primary);
  }

  .chat-button_active {
    border-color: var(--primary);
    background-color: var(--background);
  }
</style>
