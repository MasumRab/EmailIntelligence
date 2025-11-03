import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";
import { sql } from 'drizzle-orm';
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = sqliteTable("users", {
  id: integer('id').primaryKey({ autoIncrement: true }),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const categories = sqliteTable("categories", {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text("name").notNull(),
  description: text("description"),
  color: text("color").notNull(),
  count: integer("count").default(0),
});

export const emails = sqliteTable("emails", {
  id: integer('id').primaryKey({ autoIncrement: true }),
  
  // Core identifiers
  messageId: text("message_id").unique(),
  threadId: text("thread_id"),
  historyId: text("history_id"),
  
  // Basic email properties
  sender: text("sender").notNull(),
  senderEmail: text("sender_email").notNull(),
  subject: text("subject").notNull(),
  content: text("content").notNull(),
  contentHtml: text("content_html"),
  preview: text("preview").notNull(),
  snippet: text("snippet"),
  
  // Recipients
  toAddresses: text("to_addresses"), // Changed from .array()
  ccAddresses: text("cc_addresses"), // Changed from .array()
  bccAddresses: text("bcc_addresses"), // Changed from .array()
  replyTo: text("reply_to"),
  
  // Timestamps
  time: text("time").notNull(),
  internalDate: text("internal_date"),
  
  // Gmail-specific properties
  labelIds: text("label_ids"), // Changed from .array()
  labels: text("labels"), // Changed from .array()
  category: text("category"), // primary, social, promotions, updates, forums
  
  // Message state
  isUnread: integer("is_unread", { mode: 'boolean' }).default(true),
  isStarred: integer("is_starred", { mode: 'boolean' }).default(false),
  isImportant: integer("is_important", { mode: 'boolean' }).default(false),
  isDraft: integer("is_draft", { mode: 'boolean' }).default(false),
  isSent: integer("is_sent", { mode: 'boolean' }).default(false),
  isSpam: integer("is_spam", { mode: 'boolean' }).default(false),
  isTrash: integer("is_trash", { mode: 'boolean' }).default(false),
  isChat: integer("is_chat", { mode: 'boolean' }).default(false),
  
  // Content properties
  hasAttachments: integer("has_attachments", { mode: 'boolean' }).default(false),
  attachmentCount: integer("attachment_count").default(0),
  sizeEstimate: integer("size_estimate"),
  
  // Security and authentication
  spfStatus: text("spf_status"), // pass, fail, neutral, etc.
  dkimStatus: text("dkim_status"),
  dmarcStatus: text("dmarc_status"),
  isEncrypted: integer("is_encrypted", { mode: 'boolean' }).default(false),
  isSigned: integer("is_signed", { mode: 'boolean' }).default(false),
  
  // Priority and handling
  priority: text("priority").default("normal"), // low, normal, high
  isAutoReply: integer("is_auto_reply", { mode: 'boolean' }).default(false),
  mailingList: text("mailing_list"),
  
  // Thread and conversation
  inReplyTo: text("in_reply_to"),
  references: text("references"), // Changed from .array()
  isFirstInThread: integer("is_first_in_thread", { mode: 'boolean' }).default(true),
  
  // AI analysis results
  categoryId: integer("category_id").references(() => categories.id),
  confidence: integer("confidence").default(95),
  analysisMetadata: text("analysis_metadata"), // JSON string for additional metadata
  
  // Legacy compatibility
  isRead: integer("is_read", { mode: 'boolean' }).default(false), // Computed from isUnread

  // Timestamps for record creation and updates
  createdAt: text("created_at").default(sql`CURRENT_TIMESTAMP`).notNull(),
  updatedAt: text("updated_at").default(sql`CURRENT_TIMESTAMP`).notNull(),
});

export const activities = sqliteTable("activities", {
  id: integer('id').primaryKey({ autoIncrement: true }),
  type: text("type").notNull(), // 'label', 'category', 'sync', 'review'
  description: text("description").notNull(),
  details: text("details"),
  timestamp: text("timestamp").notNull(),
  icon: text("icon").notNull(),
  iconBg: text("icon_bg").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertCategorySchema = createInsertSchema(categories).omit({
  id: true,
});

export const insertEmailSchema = createInsertSchema(emails).omit({
  id: true,
});

export const insertActivitySchema = createInsertSchema(activities).omit({
  id: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export type InsertCategory = z.infer<typeof insertCategorySchema>;
export type Category = typeof categories.$inferSelect;

export type InsertEmail = z.infer<typeof insertEmailSchema>;
export type Email = typeof emails.$inferSelect;

export type InsertActivity = z.infer<typeof insertActivitySchema>;
export type Activity = typeof activities.$inferSelect;

export type EmailWithCategory = Email & {
  categoryData?: Category; // Renamed from 'category' to avoid collision
};

export type DashboardStats = {
  totalEmails: number;
  autoLabeled: number;
  categories: number;
  timeSaved: string;
  weeklyGrowth: {
    totalEmails: number;
    autoLabeled: number;
    categories: number;
    timeSaved: number;
  };
};
