import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertEmailSchema, insertCategorySchema, insertActivitySchema } from "@shared/schema";
import { z } from "zod";

export async function registerRoutes(app: Express): Promise<Server> {
  // Dashboard stats
  app.get("/api/dashboard/stats", async (_req, res) => {
    try {
      const stats = await storage.getDashboardStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch dashboard stats" });
    }
  });

  // Categories
  app.get("/api/categories", async (_req, res) => {
    try {
      const categories = await storage.getAllCategories();
      res.json(categories);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch categories" });
    }
  });

  app.post("/api/categories", async (req, res) => {
    try {
      const categoryData = insertCategorySchema.parse(req.body);
      const category = await storage.createCategory(categoryData);
      res.status(201).json(category);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: "Invalid category data", errors: error.errors });
      } else {
        res.status(500).json({ message: "Failed to create category" });
      }
    }
  });

  app.put("/api/categories/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const updateData = req.body;
      const category = await storage.updateCategory(id, updateData);
      
      if (!category) {
        return res.status(404).json({ message: "Category not found" });
      }
      
      res.json(category);
    } catch (error) {
      res.status(500).json({ message: "Failed to update category" });
    }
  });

  // Emails
  app.get("/api/emails", async (req, res) => {
    try {
      const { category, search } = req.query;
      
      let emails;
      if (search && typeof search === 'string') {
        emails = await storage.searchEmails(search);
      } else if (category && typeof category === 'string') {
        const categoryId = parseInt(category);
        emails = await storage.getEmailsByCategory(categoryId);
      } else {
        emails = await storage.getAllEmails();
      }
      
      res.json(emails);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch emails" });
    }
  });

  app.get("/api/emails/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const email = await storage.getEmailById(id);
      
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }
      
      res.json(email);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch email" });
    }
  });

  app.post("/api/emails", async (req, res) => {
    try {
      const emailData = insertEmailSchema.parse(req.body);
      const email = await storage.createEmail(emailData);
      res.status(201).json(email);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: "Invalid email data", errors: error.errors });
      } else {
        res.status(500).json({ message: "Failed to create email" });
      }
    }
  });

  app.put("/api/emails/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      const updateData = req.body;
      const email = await storage.updateEmail(id, updateData);
      
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }
      
      res.json(email);
    } catch (error) {
      res.status(500).json({ message: "Failed to update email" });
    }
  });

  // Activities
  app.get("/api/activities", async (req, res) => {
    try {
      const { limit } = req.query;
      const activities = await storage.getRecentActivities(
        limit ? parseInt(limit as string) : undefined
      );
      res.json(activities);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch activities" });
    }
  });

  app.post("/api/activities", async (req, res) => {
    try {
      const activityData = insertActivitySchema.parse(req.body);
      const activity = await storage.createActivity(activityData);
      res.status(201).json(activity);
    } catch (error) {
      if (error instanceof z.ZodError) {
        res.status(400).json({ message: "Invalid activity data", errors: error.errors });
      } else {
        res.status(500).json({ message: "Failed to create activity" });
      }
    }
  });

  // Gmail sync simulation
  app.post("/api/gmail/sync", async (_req, res) => {
    try {
      const result = await storage.simulateGmailSync();
      res.json(result);
    } catch (error) {
      res.status(500).json({ message: "Failed to sync with Gmail" });
    }
  });

  // AI categorization simulation
  app.post("/api/ai/categorize", async (req, res) => {
    try {
      const { emailId, categoryId, confidence } = req.body;
      
      const email = await storage.updateEmail(emailId, {
        categoryId: categoryId,
        confidence: confidence || 95,
      });
      
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }

      // Create activity for AI categorization
      await storage.createActivity({
        type: "label",
        description: "AI categorized email",
        details: `Email "${email.subject}" categorized`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-brain",
        iconBg: "bg-blue-50 text-blue-600",
      });
      
      res.json({ success: true, email });
    } catch (error) {
      res.status(500).json({ message: "Failed to categorize email" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
