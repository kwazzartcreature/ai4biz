import { Message } from "./schemas";
import { boolean, z } from "zod";

export const globalState = $state({
  ws: null as WebSocket | null,
  messages: z
    .array(Message)
    .parse(JSON.parse(localStorage.getItem("messages") || "[]")),
  chatWindowOpen: false,
  typing: false,
  firstHandshake: false,
  isLargeScreen: false,
});
