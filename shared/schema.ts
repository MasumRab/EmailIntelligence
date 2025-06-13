import { pgTable, text, serial, integer, boolean, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const categories = pgTable("categories", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  color: text("color").notNull(),
  count: integer("count").default(0),
});

export const emails = pgTable("emails", {
  id: serial("id").primaryKey(),
  
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
  toAddresses: text("to_addresses").array(),
  ccAddresses: text("cc_addresses").array(),
  bccAddresses: text("bcc_addresses").array(),
  replyTo: text("reply_to"),
  
  // Timestamps
  time: text("time").notNull(),
  internalDate: text("internal_date"),
  
  // Gmail-specific properties
  labelIds: text("label_ids").array(),
  labels: text("labels").array(),
  category: text("category"), // primary, social, promotions, updates, forums
  
  // Message state
  isUnread: boolean("is_unread").default(true),
  isStarred: boolean("is_starred").default(false),
  isImportant: boolean("is_important").default(false),
  isDraft: boolean("is_draft").default(false),
  isSent: boolean("is_sent").default(false),
  isSpam: boolean("is_spam").default(false),
  isTrash: boolean("is_trash").default(false),
  isChat: boolean("is_chat").default(false),
  
  // Content properties
  hasAttachments: boolean("has_attachments").default(false),
  attachmentCount: integer("attachment_count").default(0),
  sizeEstimate: integer("size_estimate"),
  
  // Security and authentication
  spfStatus: text("spf_status"), // pass, fail, neutral, etc.
  dkimStatus: text("dkim_status"),
  dmarcStatus: text("dmarc_status"),
  isEncrypted: boolean("is_encrypted").default(false),
  isSigned: boolean("is_signed").default(false),
  
  // Priority and handling
  priority: text("priority").default("normal"), // low, normal, high
  isAutoReply: boolean("is_auto_reply").default(false),
  mailingList: text("mailing_list"),
  
  // Thread and conversation
  inReplyTo: text("in_reply_to"),
  references: text("references").array(),
  isFirstInThread: boolean("is_first_in_thread").default(true),
  
  // AI analysis results
  categoryId: integer("category_id").references(() => categories.id),
  confidence: integer("confidence").default(95),
  analysisMetadata: text("analysis_metadata"), // JSON string for additional metadata
  
  // Legacy compatibility
  isRead: boolean("is_read").default(false), // Computed from isUnread

  // Timestamps for record creation and updates
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const activities = pgTable("activities", {
  id: serial("id").primaryKey(),
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
  category?: Category;
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
