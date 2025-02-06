import { z } from "zod";

export const Message = z.object({
  content: z.string(),
  sentAt: z.string(),
  role: z.union([z.literal("user"), z.literal("operator"), z.literal("assistant")]),
});
