import { 
  users, emails, categories, activities,
  type User, type InsertUser,
  type Email, type InsertEmail, type EmailWithCategory,
  type Category, type InsertCategory,
  type Activity, type InsertActivity,
  type DashboardStats
} from "@shared/schema";
import { db } from "./db.js";
import { eq, desc, ilike, count, sql } from "drizzle-orm";
import { pythonNLP } from "./python-bridge.js";

export interface IStorage {
  // User methods
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // Category methods
  getAllCategories(): Promise<Category[]>;
  getCategoryById(id: number): Promise<Category | undefined>;
  createCategory(category: InsertCategory): Promise<Category>;
  updateCategory(id: number, category: Partial<Category>): Promise<Category | undefined>;
  updateCategoryCount(categoryId: number): Promise<void>;

  // Activity methods
  getAllActivities(): Promise<Activity[]>;
  createActivity(activity: InsertActivity): Promise<Activity>;
  getRecentActivities(limit?: number): Promise<Activity[]>;

  // Dashboard methods
  getDashboardStats(): Promise<DashboardStats>;
  simulateGmailSync(): Promise<{ synced: number; newEmails: Email[] }>;
}

export class DatabaseStorage implements IStorage {
  async getUser(id: number): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user || undefined;
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.username, username));
    return user || undefined;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const [user] = await db
      .insert(users)
      .values(insertUser)
      .returning();
    return user;
  }

  // Category methods
  async getAllCategories(): Promise<Category[]> {
    return await db.select().from(categories).orderBy(categories.name);
  }

  async getCategoryById(id: number): Promise<Category | undefined> {
    const [category] = await db.select().from(categories).where(eq(categories.id, id));
    return category || undefined;
  }

  async createCategory(insertCategory: InsertCategory): Promise<Category> {
    const [category] = await db
      .insert(categories)
      .values(insertCategory)
      .returning();
    return category;
  }

  async updateCategory(id: number, categoryUpdate: Partial<Category>): Promise<Category | undefined> {
    const [updatedCategory] = await db
      .update(categories)
      .set(categoryUpdate)
      .where(eq(categories.id, id))
      .returning();
    
    return updatedCategory || undefined;
  }

  async updateCategoryCount(categoryId: number): Promise<void> {
    const [{ emailCount }] = await db
      .select({ emailCount: count() })
      .from(emails)
      .where(eq(emails.categoryId, categoryId));

    await db
      .update(categories)
      .set({ count: emailCount })
      .where(eq(categories.id, categoryId));
  }

  // Activity methods
  async getAllActivities(): Promise<Activity[]> {
    return await db.select().from(activities).orderBy(desc(activities.timestamp));
  }

  async createActivity(insertActivity: InsertActivity): Promise<Activity> {
    const [activity] = await db
      .insert(activities)
      .values(insertActivity)
      .returning();
    return activity;
  }

  async getRecentActivities(limit: number = 10): Promise<Activity[]> {
    return await db
      .select()
      .from(activities)
      .orderBy(desc(activities.timestamp))
      .limit(limit);
  }

  // Dashboard methods
  async getDashboardStats(): Promise<DashboardStats> {
    const [totalEmailsResult] = await db
      .select({ count: count() })
      .from(emails);

    const [autoLabeledResult] = await db
      .select({ count: count() })
      .from(emails)
      .where(sql`${emails.confidence} > 80`);

    const [categoriesResult] = await db
      .select({ count: count() })
      .from(categories);

    return {
      totalEmails: totalEmailsResult.count,
      autoLabeled: autoLabeledResult.count,
      categories: categoriesResult.count,
      timeSaved: "14.2h",
      weeklyGrowth: {
        totalEmails: 12,
        autoLabeled: 8,
        categories: 3,
        timeSaved: 23,
      },
    };
  }

  async simulateGmailSync(): Promise<{ synced: number; newEmails: Email[] }> {
    // Simulate finding new emails during sync
    const newEmailsData: InsertEmail[] = [
      {
        sender: "Tech Newsletter",
        senderEmail: "newsletter@techworld.com",
        subject: "Weekly Tech Updates - AI Advances",
        content: "This week in technology: Major breakthroughs in AI, new framework releases, and industry insights you shouldn't miss.",
        preview: "This week in technology: Major breakthroughs in AI, new framework releases...",
        time: "Just now",
        categoryId: null,
        labels: ["Newsletter", "Technology"],
        confidence: 89,
        isStarred: false,
        isRead: false,
      },
      {
        sender: "Dr. Smith's Office",
        senderEmail: "appointments@drsmith.com",
        subject: "Appointment Reminder - Tomorrow 3 PM",
        content: "This is a reminder that you have an appointment scheduled for tomorrow at 3:00 PM. Please arrive 15 minutes early.",
        preview: "This is a reminder that you have an appointment scheduled for tomorrow at 3:00 PM...",
        time: "5 min ago",
        categoryId: null,
        labels: ["Healthcare", "Appointment"],
        confidence: 96,
        isStarred: false,
        isRead: false,
      },
    ];

    const newEmails: Email[] = [];
    for (const emailData of newEmailsData) {
      const email = await pythonNLP.createEmail(emailData);
      newEmails.push(email);
    }

    // Create sync activity
    await this.createActivity({
      type: "sync",
      description: "Synced with Gmail",
      details: `${newEmails.length} new emails processed`,
      timestamp: new Date().toISOString(),
      icon: "fas fa-sync",
      iconBg: "bg-purple-50 text-purple-600",
    });

    return {
      synced: newEmails.length,
      newEmails,
    };
  }
}

export const storage = new DatabaseStorage();
