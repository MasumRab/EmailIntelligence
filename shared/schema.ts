import { z } from 'zod';

export const categorySchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().optional(),
  color: z.string().optional(),
  count: z.number().optional(),
});

export const emailSchema = z.object({
  id: z.number(),
  sender: z.string(),
  senderEmail: z.string().email(),
  subject: z.string(),
  content: z.string(),
  time: z.string(), // or z.date() if you parse it
  messageId: z.string().optional(),
  threadId: z.string().optional(),
  preview: z.string(),
  category: z.string().optional(),
  categoryId: z.number().optional(),
  labels: z.array(z.string()),
  confidence: z.number(),
  isImportant: z.boolean(),
  isStarred: z.boolean(),
  isUnread: z.boolean(),
  hasAttachments: z.boolean(),
  attachmentCount: z.number(),
  sizeEstimate: z.number(),
  aiAnalysis: z.record(z.any()).optional(),
  filterResults: z.record(z.any()).optional(),
});

export const insertEmailSchema = emailSchema.omit({ id: true });
export const updateEmailSchema = emailSchema.partial();

export const emailWithCategorySchema = emailSchema.extend({
  categoryData: categorySchema.optional(),
});

export type Category = z.infer<typeof categorySchema>;
export type Email = z.infer<typeof emailSchema>;
export type InsertEmail = z.infer<typeof insertEmailSchema>;
export type UpdateEmail = z.infer<typeof updateEmailSchema>;
export type EmailWithCategory = z.infer<typeof emailWithCategorySchema>;
