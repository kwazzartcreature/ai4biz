import { globalState } from "../state.svelte";
import { Message } from "../schemas";
import { formatDate } from "./formatDate";

export const connectWS = () => {
  const ws = new WebSocket("wss://inchatai.5dgo.dev/ws");
  ws.onmessage = (event) => {
    globalState.typing = false;
    const message = Message.parse(JSON.parse(event.data));
    message.sentAt = formatDate(new Date());
    globalState.messages.push(message);

    console.log("Message: ", event.data);
  };

  ws.onerror = (event) => {
    console.error("Error: ", event);
  };

  ws.onopen = () => {
    globalState.ws = ws;
    globalState.firstHandshake = true;
    ws.send("[]");
    console.log("Connected to the server");
  };

  ws.onclose = (error) => {
    globalState.ws = null;

    console.log("Reconnecting to the server", error.code);
    setTimeout(() => {
      connectWS();
    }, 1500);
  };
};
