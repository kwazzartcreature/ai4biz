<script lang="ts">
  import ChevronBottom from "../../assets/icons/ChevronBottom.svelte";
  import { fade } from "svelte/transition";

  interface Props {
    onclick: (behavior: ScrollBehavior) => void;
    hidden: boolean;
  }

  let { onclick, hidden }: Props = $props();
</script>

<button
  transition:fade
  onclick={() => onclick("smooth")}
  class={`bottom-scroller ${hidden ? "hidden" : ""}`}
>
  <ChevronBottom />
</button>

<style>
  .bottom-scroller {
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: var(--border);
    border: 2px solid var(--background);
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    width: min-content;
    position: sticky;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    transition: 0.3s;
  }

  .bottom-scroller:hover {
    border-color: var(--primary);
  }

  .hidden {
    pointer-events: none;
    opacity: 0;
  }
</style>
