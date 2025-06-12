import { db } from "./db";
import { categories, emails, activities } from "@shared/schema";
import { eq } from "drizzle-orm";

export async function initializeDatabase() {
  try {
    // Check if categories already exist
    const existingCategories = await db.select().from(categories).limit(1);
    if (existingCategories.length > 0) {
      console.log("Database already initialized");
      return;
    }

    // Insert default categories
    const defaultCategories = [
      {
        name: "Work & Business",
        description: "Professional emails, meetings, projects",
        color: "#34A853",
        count: 0
      },
      {
        name: "Personal & Family", 
        description: "Personal conversations, family updates",
        color: "#4285F4",
        count: 0
      },
      {
        name: "Finance & Banking",
        description: "Bills, statements, transactions", 
        color: "#FBBC04",
        count: 0
      },
      {
        name: "Promotions & Marketing",
        description: "Newsletters, offers, advertisements",
        color: "#EA4335", 
        count: 0
      },
      {
        name: "Travel",
        description: "Travel bookings, itineraries, confirmations",
        color: "#9C27B0",
        count: 0
      },
      {
        name: "Healthcare",
        description: "Medical appointments, health updates",
        color: "#00BCD4",
        count: 0
      }
    ];

    const insertedCategories = await db.insert(categories).values(defaultCategories).returning();
    console.log(`Inserted ${insertedCategories.length} categories`);

    // Insert sample emails
    const sampleEmails = [
      {
        sender: "John Doe",
        senderEmail: "john.doe@company.com", 
        subject: "Q4 Budget Review Meeting - Tomorrow 2 PM",
        content: "Hi team, I've scheduled our quarterly budget review for tomorrow at 2 PM in the main conference room. Please bring your departmental budget reports and be prepared to discuss any variances from our projections.",
        preview: "Hi team, I've scheduled our quarterly budget review for tomorrow at 2 PM in the main conference room...",
        time: "2:30 PM",
        categoryId: insertedCategories[0].id, // Work & Business
        labels: ["Work & Business", "Meeting"],
        confidence: 95,
        isStarred: false,
        isRead: false
      },
      {
        sender: "American Bank",
        senderEmail: "noreply@americanbank.com",
        subject: "Your Monthly Statement is Ready", 
        content: "Dear Valued Customer, Your account statement for March 2024 is now available for download. You can access it through your online banking portal or mobile app.",
        preview: "Dear Valued Customer, Your account statement for March 2024 is now available for download...",
        time: "Yesterday",
        categoryId: insertedCategories[2].id, // Finance & Banking
        labels: ["Finance & Banking", "Statement"],
        confidence: 98,
        isStarred: false,
        isRead: false
      },
      {
        sender: "Sarah Foster",
        senderEmail: "sarah.foster@gmail.com",
        subject: "Weekend Plans & Family BBQ",
        content: "Hey! Hope you're doing well. We're planning a family BBQ this weekend and would love for you to join us. Let me know if you can make it!",
        preview: "Hey! Hope you're doing well. We're planning a family BBQ this weekend and would love for you to join us...",
        time: "Mar 15",
        categoryId: insertedCategories[1].id, // Personal & Family
        labels: ["Personal & Family", "Social"],
        confidence: 92,
        isStarred: true,
        isRead: false
      }
    ];

    const insertedEmails = await db.insert(emails).values(sampleEmails).returning();
    console.log(`Inserted ${insertedEmails.length} sample emails`);

    // Update category counts
    for (const category of insertedCategories) {
      const emailCount = sampleEmails.filter(email => email.categoryId === category.id).length;
      if (emailCount > 0) {
        await db.update(categories)
          .set({ count: emailCount })
          .where(eq(categories.id, category.id));
      }
    }

    // Insert initial activities
    const sampleActivities = [
      {
        type: "label",
        description: "Auto-labeled 12 emails",
        details: "Work & Business category",
        timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
        icon: "fas fa-tag",
        iconBg: "bg-green-50 text-green-600"
      },
      {
        type: "category", 
        description: "Created new category",
        details: '"Healthcare" detected',
        timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
        icon: "fas fa-brain",
        iconBg: "bg-blue-50 text-blue-600"
      },
      {
        type: "sync",
        description: "Synced with Gmail", 
        details: "45 new emails processed",
        timestamp: new Date(Date.now() - 60 * 60 * 1000).toISOString(),
        icon: "fas fa-sync",
        iconBg: "bg-purple-50 text-purple-600"
      }
    ];

    const insertedActivities = await db.insert(activities).values(sampleActivities).returning();
    console.log(`Inserted ${insertedActivities.length} activities`);

    console.log("Database initialization completed successfully");
  } catch (error) {
    console.error("Error initializing database:", error);
    throw error;
  }
}