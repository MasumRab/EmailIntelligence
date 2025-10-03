/**
 * @file Defines the shared data schemas and types using Zod.
 *
 * This file contains the Zod schemas that are used for data validation and
 * type inference across both the frontend and backend of the application.
 * It ensures data consistency and provides a single source of truth for the
 * data structures.
 */
import { z } from 'zod';

/**
 * @const categorySchema
 * @description The Zod schema for an email category.
 */
export const categorySchema = z.object({
  id: z.number(),
  name: z.string(),
  description: z.string().optional(),
  color: z.string().optional(),
  count: z.number().optional(),
});

/**
 * @const emailSchema
 * @description The Zod schema for an email.
 */
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
  aiAnalysis: z.record(z.string(), z.any()).optional(),
  filterResults: z.record(z.string(), z.any()).optional(),
});

/**
 * @const insertEmailSchema
 * @description The Zod schema for creating a new email (omits the 'id' field).
 */
export const insertEmailSchema = emailSchema.omit({ id: true });

/**
 * @const updateEmailSchema
 * @description The Zod schema for updating an email (all fields are optional).
 */
export const updateEmailSchema = emailSchema.partial();

/**
 * @const emailWithCategorySchema
 * @description The Zod schema for an email that includes its category data.
 */
export const emailWithCategorySchema = emailSchema.extend({
  categoryData: categorySchema.optional(),
});

/**
 * @const dashboardStatsSchema
 * @description The Zod schema for the dashboard statistics.
 */
export const dashboardStatsSchema = z.object({
  totalEmails: z.number(),
  unreadEmails: z.number(),
  importantEmails: z.number(),
  categorizedEmails: z.number(),
  categories: z.array(categorySchema),
});

/**
 * @const activitySchema
 * @description The Zod schema for a user or system activity.
 */
export const activitySchema = z.object({
  id: z.number(),
  type: z.string(),
  description: z.string(),
  timestamp: z.string(),
  metadata: z.record(z.string(), z.any()).optional(),
});

/**
 * @type Category
 * @description The TypeScript type for an email category, inferred from the Zod schema.
 */
export type Category = z.infer<typeof categorySchema>;

/**
 * @type Email
 * @description The TypeScript type for an email, inferred from the Zod schema.
 */
export type Email = z.infer<typeof emailSchema>;

/**
 * @type InsertEmail
 * @description The TypeScript type for creating a new email, inferred from the Zod schema.
 */
export type InsertEmail = z.infer<typeof insertEmailSchema>;

/**
 * @type UpdateEmail
 * @description The TypeScript type for updating an email, inferred from the Zod schema.
 */
export type UpdateEmail = z.infer<typeof updateEmailSchema>;

/**
 * @type EmailWithCategory
 * @description The TypeScript type for an email with its category data, inferred from the Zod schema.
 */
export type EmailWithCategory = z.infer<typeof emailWithCategorySchema>;

/**
 * @type DashboardStats
 * @description The TypeScript type for the dashboard statistics, inferred from the Zod schema.
 */
export type DashboardStats = z.infer<typeof dashboardStatsSchema>;

/**
 * @type Activity
 * @description The TypeScript type for a user or system activity, inferred from the Zod schema.
 */
export type Activity = z.infer<typeof activitySchema>;