<script lang="ts">
  import { Message } from "../schemas";
  import z from "zod";
  import { fade } from "svelte/transition";
  import Robot from "../../assets/icons/Robot.svelte";
  import HumanSupport from "../../assets/icons/HumanSupport.svelte";

  interface Props {
    message: z.infer<typeof Message>;
  }

  let { message }: Props = $props();

  const { content, sentAt, role } = message;
</script>

<div
  transition:fade
  class={`container ${role === "user" ? "container_sender" : "container_reciever"}`}
>
  <div
    class={`message-box ${role === "user" ? "message-box_sender" : "message-box_reciever"}`}
  >
    <div class="operator">
      {#if role === "assistant"}
        <Robot />
        <span class="sender">{role}</span>
      {:else if role === "operator"}
        <HumanSupport />
        <span class="sender">{role}</span>
      {:else}
        <span class="reciever">You</span>
      {/if}
      
    </div>
    <div class="message-box__secondary">
      <span
        class={`content ${role === "user" ? "content_sender" : "content_reciever"}`}
        >{@html content}</span
      >
      <span class={`sent ${role === "user" ? "sent_sender" : "sent_reciever"}`}
        >{sentAt}</span
      >
    </div>
  </div>
</div>

<style>
  .container {
    min-width: 35%;
    width: fit-content;
    position: relative;
    max-width: 75%;
  }

  .content {
    word-break: normal;
    font-size: 1.1rem;
    font-weight: 600;
  }

  .content_reciever {
    color: var(--text-gold);
  }

  .container_sender {
    margin-left: auto;
  }

  .message-box {
    color: #fff;
    display: flex;
    width: 100%;
    border-radius: 2rem 2rem 2rem 0;
    background-color: var(--border);
    flex-direction: column;
    border: 1px solid var(--primary);
    padding: 1rem 1rem 0.5rem 1rem;
  }

  .message-box__secondary {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 1rem;
    position: relative;
  }

  .operator {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    text-transform: capitalize;
    color: var(--primary);
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .reciever {
    margin-left: auto;
    color: var(--primary);
  }

  .sender {
    color: var(--border);
  }

  .message-box_sender {
    border-radius: 2rem 2rem 0 2rem;
  }

  .message-box_reciever {
    border-radius: 2rem 2rem 2rem 0;
    background: var(--primary-gradient);
    border-width: 4px;
  }

  .sent {
    text-wrap: nowrap;
    font-size: 0.9rem;
  }

.sent_reciever {
    color: var(--primary-dark);
}

  .sent_sender {
    color: grey;
  }
</style>
