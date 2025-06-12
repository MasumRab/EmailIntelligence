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
  sender: text("sender").notNull(),
  senderEmail: text("sender_email").notNull(),
  subject: text("subject").notNull(),
  content: text("content").notNull(),
  preview: text("preview").notNull(),
  time: text("time").notNull(),
  categoryId: integer("category_id").references(() => categories.id),
  labels: text("labels").array(),
  confidence: integer("confidence").default(95),
  isStarred: boolean("is_starred").default(false),
  isRead: boolean("is_read").default(false),
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
