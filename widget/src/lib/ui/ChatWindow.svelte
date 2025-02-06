<script lang="ts">
  import Close from "../../assets/icons/Close.svelte";
  import Send from "../../assets/icons/Send.svelte";
  import { fly } from "svelte/transition";
  import MessageBox from "./MessageBox.svelte";
  import { Message } from "../schemas";
  import { formatDate } from "../utils/formatDate";
  import { globalState } from "../state.svelte";
  import BottomScroller from "./BottomScroller.svelte";
  import { onMount } from "svelte";

  interface Props {
    chatWindowOpen: boolean;
  }
  let { chatWindowOpen = $bindable() }: Props = $props();

  let textarea = $state<HTMLTextAreaElement | null>(null);
  let messagesContainer = $state<HTMLDivElement | null>(null);

  const messages = globalState.messages;
  const ws = globalState.ws;

  let isBottomScrollerVisible = $state(false);

  const sendMessage = (e: SubmitEvent) => {
    e.preventDefault();
    const message = textarea?.value;
    if (message) {
      messages.push(
        Message.parse({
          content: message,
          sentAt: formatDate(new Date()),
          role: "user",
        })
      );
      setTimeout(() => {
        ws?.send(message);
      }, 3000);

      setTimeout(() => {
        globalState.typing = true;
      }, 1500);
    }

    textarea!.value = "";
  };

  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      sendMessage(new SubmitEvent("submit"));
    }
  };

  const scrollMessagesToBottom = (behavior: ScrollBehavior = "smooth") => {
    messagesContainer?.scrollTo({
      top: messagesContainer.scrollHeight,
      behavior,
    });
  };

  const bottomScrollEventCB = () => {
    if (!messagesContainer) return;

    const { scrollTop, scrollHeight, clientHeight } = messagesContainer!;
    if (scrollHeight <= clientHeight) {
      isBottomScrollerVisible = false;
      return;
    }
    isBottomScrollerVisible = scrollTop + clientHeight >= scrollHeight - 5;
  };

  onMount(() => {
    if (messagesContainer) {
      scrollMessagesToBottom("smooth");
      bottomScrollEventCB();

      messagesContainer.addEventListener("scroll", bottomScrollEventCB);
    }

    return () => {
      messagesContainer?.removeEventListener("scroll", bottomScrollEventCB);
    };
  });

  $effect(() => {
    if (messages.length) {
      scrollMessagesToBottom("smooth");
    }
  });
</script>

<div class="chat-window" transition:fly>
  <div class="chat-header">
    <div class="header-content">
      <div class="header-content__left">
        <h2>Chat with us!</h2>
        <p>
          <span class={`status ${ws ? "status_okay" : "status_bad"}`}> </span>
          <span class="status__text">
            {ws ? "Connected" : "Disconnected"}
          </span>
        </p>
      </div>
      <button class="close-button" onclick={() => (chatWindowOpen = false)}>
        <Close />
      </button>
    </div>
  </div>
  <div class="chat-messages" bind:this={messagesContainer}>
    {#each messages as message, index (index)}
      <MessageBox message={Message.parse(message)} />
    {/each}
    <BottomScroller
      hidden={isBottomScrollerVisible}
      onclick={scrollMessagesToBottom}
    />
  </div>
  {#if globalState.typing}
    <span class="typing">Typing...</span>
  {/if}
  <form onsubmit={sendMessage} class="chat-input">
    <textarea
      bind:this={textarea}
      onkeydown={handleKeydown}
      placeholder="Please, ask anything you'd like to know!"
    ></textarea>
    <button type="submit">
      <Send />
    </button>
  </form>
</div>

<style>
  .chat-window {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 100%;
    height: 100vh;
    background-color: var(--background);
    border: 2px solid #000;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .chat-header {
    position: relative;
    background: var(--dark-gradient);
    border-bottom: 2px solid var(--primary);
    color: var(--text);
    max-height: max-content;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
  }

  .header-content {
    position: relative;
    z-index: 2;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .header-content__left {
    display: flex;
    flex-direction: column;
  }

  h2 {
    text-transform: uppercase;
    color: var(--text-gold);
    font-weight: 800;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--text);
  }

  .wavy-line {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 125px;
    z-index: -1;
  }

  .chat-messages {
    display: flex;
    flex: 1;
    position: relative;
    flex-direction: column;
    overflow-y: auto;
    padding: 1.5rem 1.5rem 0 1.5rem;
    height: 100%;
    gap: 2.5rem;
    background-color: var(--background);
  }

  .typing {
    color: var(--primary);
    font-weight: 700;
    padding: 0.5rem;
  }

  .chat-input > textarea {
    height: 100%;
    width: 100%;
    border: none;
    outline: none;
    resize: none;
    color: var(--text);
    font-size: 1rem;
    background-color: var(--border);
  }

  .chat-input > textarea::placeholder {
    font-weight: 600;
    font-size: 1rem;
    color: grey;
  }

  .chat-input > button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: max-content;
    border: none;
    cursor: pointer;
    background-color: var(--primary);
    padding: 1rem;
    border-radius: 50%;
    transition: 0.2s ease-in-out;
  }

  .chat-input > button:hover {
    background-color: var(--primary-dark);
  }

  .chat-input {
    display: flex;
    align-items: center;
    height: 8rem;
    border-top: 2px solid var(--primary);
    border-right: 0;
    border-left: 0;
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background-color: var(--border);
  }

  h2 {
    color: var(--primary);
    text-transform: uppercase;
  }

  @media (min-width: 1024px) {
    .chat-window {
      right: 7rem;
      bottom: 7rem;
      max-width: 550px;
      height: 80vh;
      border-radius: 1.2rem 1.2rem 0 1.2rem;
      border: 4px solid var(--primary);
    }
  }

  .status {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: blink 1s infinite;
  }

  .status__text {
    font-weight: 600;
  }

  .status_okay {
    background-color: #00ff00;
  }

  .status_bad {
    background-color: #ff0000;
  }

  @keyframes blink {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }

  .typing {
    background-color: transparent;
  }
</style>
