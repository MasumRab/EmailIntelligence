import { 
  users, emails, categories, activities,
  type User, type InsertUser,
  type Email, type InsertEmail, type EmailWithCategory,
  type Category, type InsertCategory,
  type Activity, type InsertActivity,
  type DashboardStats
} from "@shared/schema";
import { AIEngine, type AIAnalysis, type AccuracyValidation } from "./ai-engine";

export interface IStorage {
  // User methods
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;

  // Email methods
  getAllEmails(): Promise<EmailWithCategory[]>;
  getEmailById(id: number): Promise<EmailWithCategory | undefined>;
  createEmail(email: InsertEmail): Promise<Email>;
  updateEmail(id: number, email: Partial<Email>): Promise<Email | undefined>;
  getEmailsByCategory(categoryId: number): Promise<EmailWithCategory[]>;
  searchEmails(query: string): Promise<EmailWithCategory[]>;

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

export class MemStorage implements IStorage {
  private users: Map<number, User>;
  private emails: Map<number, Email>;
  private categories: Map<number, Category>;
  private activities: Map<number, Activity>;
  private currentUserId: number;
  private currentEmailId: number;
  private currentCategoryId: number;
  private currentActivityId: number;

  constructor() {
    this.users = new Map();
    this.emails = new Map();
    this.categories = new Map();
    this.activities = new Map();
    this.currentUserId = 1;
    this.currentEmailId = 1;
    this.currentCategoryId = 1;
    this.currentActivityId = 1;

    this.initializeData();
  }

  private initializeData(): void {
    // Initialize categories
    const defaultCategories: InsertCategory[] = [
      { name: "Work & Business", description: "Professional emails, meetings, projects", color: "#34A853", count: 234 },
      { name: "Personal & Family", description: "Personal conversations, family updates", color: "#4285F4", count: 156 },
      { name: "Finance & Banking", description: "Bills, statements, transactions", color: "#FBBC04", count: 89 },
      { name: "Promotions & Marketing", description: "Newsletters, offers, advertisements", color: "#EA4335", count: 145 },
      { name: "Travel", description: "Travel bookings, itineraries, confirmations", color: "#9C27B0", count: 23 },
      { name: "Healthcare", description: "Medical appointments, health updates", color: "#00BCD4", count: 12 },
    ];

    defaultCategories.forEach(category => {
      const id = this.currentCategoryId++;
      this.categories.set(id, { ...category, id });
    });

    // Initialize sample emails
    const sampleEmails: InsertEmail[] = [
      {
        sender: "John Doe",
        senderEmail: "john.doe@company.com",
        subject: "Q4 Budget Review Meeting - Tomorrow 2 PM",
        content: "Hi team, I've scheduled our quarterly budget review for tomorrow at 2 PM in the main conference room. Please bring your departmental budget reports and be prepared to discuss any variances from our projections.",
        preview: "Hi team, I've scheduled our quarterly budget review for tomorrow at 2 PM in the main conference room...",
        time: "2:30 PM",
        categoryId: 1,
        labels: ["Work & Business", "Meeting"],
        confidence: 95,
        isStarred: false,
        isRead: false,
      },
      {
        sender: "American Bank",
        senderEmail: "noreply@americanbank.com",
        subject: "Your Monthly Statement is Ready",
        content: "Dear Valued Customer, Your account statement for March 2024 is now available for download. You can access it through your online banking portal or mobile app.",
        preview: "Dear Valued Customer, Your account statement for March 2024 is now available for download...",
        time: "Yesterday",
        categoryId: 3,
        labels: ["Finance & Banking", "Statement"],
        confidence: 98,
        isStarred: false,
        isRead: false,
      },
      {
        sender: "Sarah Foster",
        senderEmail: "sarah.foster@gmail.com",
        subject: "Weekend Plans & Family BBQ",
        content: "Hey! Hope you're doing well. We're planning a family BBQ this weekend and would love for you to join us. Let me know if you can make it!",
        preview: "Hey! Hope you're doing well. We're planning a family BBQ this weekend and would love for you to join us...",
        time: "Mar 15",
        categoryId: 2,
        labels: ["Personal & Family", "Social"],
        confidence: 92,
        isStarred: true,
        isRead: false,
      },
    ];

    sampleEmails.forEach(email => {
      const id = this.currentEmailId++;
      this.emails.set(id, { ...email, id });
    });

    // Initialize recent activities
    const sampleActivities: InsertActivity[] = [
      {
        type: "label",
        description: "Auto-labeled 12 emails",
        details: "Work & Business category",
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        icon: "fas fa-tag",
        iconBg: "bg-green-50 text-green-600",
      },
      {
        type: "category",
        description: "Created new category",
        details: '"Healthcare" detected',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        icon: "fas fa-brain",
        iconBg: "bg-blue-50 text-blue-600",
      },
      {
        type: "sync",
        description: "Synced with Gmail",
        details: "45 new emails processed",
        timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        icon: "fas fa-sync",
        iconBg: "bg-purple-50 text-purple-600",
      },
      {
        type: "review",
        description: "Low confidence labels",
        details: "3 emails need review",
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        icon: "fas fa-exclamation-triangle",
        iconBg: "bg-yellow-50 text-yellow-600",
      },
    ];

    sampleActivities.forEach(activity => {
      const id = this.currentActivityId++;
      this.activities.set(id, { ...activity, id });
    });
  }

  // User methods
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(user => user.username === username);
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = this.currentUserId++;
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  // Email methods
  async getAllEmails(): Promise<EmailWithCategory[]> {
    const emails = Array.from(this.emails.values());
    return emails.map(email => ({
      ...email,
      category: email.categoryId ? this.categories.get(email.categoryId) : undefined,
    }));
  }

  async getEmailById(id: number): Promise<EmailWithCategory | undefined> {
    const email = this.emails.get(id);
    if (!email) return undefined;
    return {
      ...email,
      category: email.categoryId ? this.categories.get(email.categoryId) : undefined,
    };
  }

  async createEmail(insertEmail: InsertEmail): Promise<Email> {
    const id = this.currentEmailId++;
    const email: Email = { ...insertEmail, id };
    this.emails.set(id, email);
    
    // Update category count
    if (email.categoryId) {
      await this.updateCategoryCount(email.categoryId);
    }
    
    return email;
  }

  async updateEmail(id: number, emailUpdate: Partial<Email>): Promise<Email | undefined> {
    const email = this.emails.get(id);
    if (!email) return undefined;
    
    const updatedEmail = { ...email, ...emailUpdate };
    this.emails.set(id, updatedEmail);
    return updatedEmail;
  }

  async getEmailsByCategory(categoryId: number): Promise<EmailWithCategory[]> {
    const emails = Array.from(this.emails.values()).filter(email => email.categoryId === categoryId);
    return emails.map(email => ({
      ...email,
      category: this.categories.get(categoryId),
    }));
  }

  async searchEmails(query: string): Promise<EmailWithCategory[]> {
    const lowerQuery = query.toLowerCase();
    const emails = Array.from(this.emails.values()).filter(email =>
      email.subject.toLowerCase().includes(lowerQuery) ||
      email.sender.toLowerCase().includes(lowerQuery) ||
      email.content.toLowerCase().includes(lowerQuery)
    );
    
    return emails.map(email => ({
      ...email,
      category: email.categoryId ? this.categories.get(email.categoryId) : undefined,
    }));
  }

  // Category methods
  async getAllCategories(): Promise<Category[]> {
    return Array.from(this.categories.values());
  }

  async getCategoryById(id: number): Promise<Category | undefined> {
    return this.categories.get(id);
  }

  async createCategory(insertCategory: InsertCategory): Promise<Category> {
    const id = this.currentCategoryId++;
    const category: Category = { ...insertCategory, id };
    this.categories.set(id, category);
    return category;
  }

  async updateCategory(id: number, categoryUpdate: Partial<Category>): Promise<Category | undefined> {
    const category = this.categories.get(id);
    if (!category) return undefined;
    
    const updatedCategory = { ...category, ...categoryUpdate };
    this.categories.set(id, updatedCategory);
    return updatedCategory;
  }

  async updateCategoryCount(categoryId: number): Promise<void> {
    const category = this.categories.get(categoryId);
    if (!category) return;
    
    const emailCount = Array.from(this.emails.values()).filter(email => email.categoryId === categoryId).length;
    category.count = emailCount;
    this.categories.set(categoryId, category);
  }

  // Activity methods
  async getAllActivities(): Promise<Activity[]> {
    return Array.from(this.activities.values()).sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  async createActivity(insertActivity: InsertActivity): Promise<Activity> {
    const id = this.currentActivityId++;
    const activity: Activity = { ...insertActivity, id };
    this.activities.set(id, activity);
    return activity;
  }

  async getRecentActivities(limit: number = 10): Promise<Activity[]> {
    const activities = await this.getAllActivities();
    return activities.slice(0, limit);
  }

  // Dashboard methods
  async getDashboardStats(): Promise<DashboardStats> {
    const totalEmails = this.emails.size;
    const autoLabeled = Array.from(this.emails.values()).filter(email => email.confidence && email.confidence > 80).length;
    const categoriesCount = this.categories.size;
    
    return {
      totalEmails,
      autoLabeled,
      categories: categoriesCount,
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
    const newEmailsData = [
      {
        sender: "Tech Newsletter",
        senderEmail: "newsletter@techworld.com",
        subject: "Weekly Tech Updates - AI Advances",
        content: "This week in technology: Major breakthroughs in AI, new framework releases, and industry insights you shouldn't miss.",
        preview: "This week in technology: Major breakthroughs in AI, new framework releases...",
        time: "Just now",
        categoryId: 4, // Promotions
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
        categoryId: 6, // Healthcare
        labels: ["Healthcare", "Appointment"],
        confidence: 96,
        isStarred: false,
        isRead: false,
      },
    ];

    const newEmails: Email[] = [];
    for (const emailData of newEmailsData) {
      const email = await this.createEmail(emailData);
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

export const storage = new MemStorage();
