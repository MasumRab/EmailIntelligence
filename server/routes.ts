import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertEmailSchema, insertCategorySchema, insertActivitySchema } from "@shared/schema";
import { pythonNLP } from "./python-bridge";
import { gmailAIService } from "./gmail-ai-service";
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

  // Advanced AI Analysis
  app.post("/api/ai/analyze", async (req, res) => {
    try {
      const { subject, content } = req.body;
      
      if (!subject || !content) {
        return res.status(400).json({ message: "Subject and content are required" });
      }

      const analysis = await pythonNLP.analyzeEmail(subject, content);
      
      res.json(analysis);
    } catch (error) {
      console.error("AI analysis error:", error);
      res.status(500).json({ message: "Failed to analyze email with AI" });
    }
  });

  // Enhanced AI categorization with accuracy validation
  app.post("/api/ai/categorize", async (req, res) => {
    try {
      const { emailId, autoAnalyze } = req.body;
      
      const email = await storage.getEmailById(emailId);
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }

      let analysis;
      if (autoAnalyze) {
        // Use advanced AI analysis
        analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
        
        // Find matching category
        const categories = await storage.getAllCategories();
        const matchingCategory = categories.find(cat => 
          analysis.categories.some(aiCat => 
            cat.name.toLowerCase().includes(aiCat.toLowerCase()) ||
            aiCat.toLowerCase().includes(cat.name.toLowerCase())
          )
        );

        if (matchingCategory) {
          // Update email with AI analysis results
          const updatedEmail = await storage.updateEmail(emailId, {
            categoryId: matchingCategory.id,
            confidence: Math.round(analysis.confidence * 100),
            labels: analysis.suggested_labels,
          });

          // Create detailed activity
          await storage.createActivity({
            type: "label",
            description: "Advanced AI analysis completed",
            details: `${analysis.categories.join(", ")} | Confidence: ${Math.round(analysis.confidence * 100)}% | ${analysis.validation.reliable ? 'High' : 'Low'} reliability`,
            timestamp: new Date().toISOString(),
            icon: "fas fa-brain",
            iconBg: analysis.validation.reliable ? "bg-green-50 text-green-600" : "bg-yellow-50 text-yellow-600",
          });

          res.json({ 
            success: true, 
            email: updatedEmail, 
            analysis,
            categoryAssigned: matchingCategory.name
          });
        } else {
          // No matching category found, suggest creating new one
          res.json({ 
            success: false, 
            analysis,
            suggestion: "create_category",
            suggestedCategory: analysis.categories[0],
            message: "No matching category found. Consider creating a new category."
          });
        }
      } else {
        // Manual categorization (existing logic)
        const { categoryId, confidence } = req.body;
        
        const updatedEmail = await storage.updateEmail(emailId, {
          categoryId: categoryId,
          confidence: confidence || 95,
        });

        await storage.createActivity({
          type: "label",
          description: "Manual email categorization",
          details: `Email "${email.subject}" manually categorized`,
          timestamp: new Date().toISOString(),
          icon: "fas fa-user",
          iconBg: "bg-blue-50 text-blue-600",
        });
        
        res.json({ success: true, email: updatedEmail });
      }
    } catch (error) {
      console.error("Categorization error:", error);
      res.status(500).json({ message: "Failed to categorize email" });
    }
  });

  // Batch AI processing
  app.post("/api/ai/batch-analyze", async (req, res) => {
    try {
      const { emailIds } = req.body;
      
      if (!emailIds || !Array.isArray(emailIds)) {
        return res.status(400).json({ message: "Email IDs array is required" });
      }

      const results = [];
      const categories = await storage.getAllCategories();
      
      for (const emailId of emailIds.slice(0, 10)) { // Limit to 10 emails for performance
        try {
          const email = await storage.getEmailById(emailId);
          if (!email) continue;

          const analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
          
          // Find best matching category
          const matchingCategory = categories.find(cat => 
            analysis.categories.some(aiCat => 
              cat.name.toLowerCase().includes(aiCat.toLowerCase()) ||
              aiCat.toLowerCase().includes(cat.name.toLowerCase())
            )
          );

          if (matchingCategory && analysis.validation.reliable) {
            await storage.updateEmail(emailId, {
              categoryId: matchingCategory.id,
              confidence: Math.round(analysis.confidence * 100),
              labels: analysis.suggested_labels,
            });

            results.push({
              emailId,
              success: true,
              category: matchingCategory.name,
              confidence: analysis.confidence,
              analysis
            });
          } else {
            results.push({
              emailId,
              success: false,
              reason: matchingCategory ? 'low_confidence' : 'no_matching_category',
              analysis
            });
          }
        } catch (error) {
          results.push({
            emailId,
            success: false,
            reason: 'analysis_error',
            error: error.message
          });
        }
      }

      // Create batch activity
      const successCount = results.filter(r => r.success).length;
      await storage.createActivity({
        type: "label",
        description: "Batch AI analysis completed",
        details: `${successCount}/${emailIds.length} emails successfully analyzed and categorized`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-layer-group",
        iconBg: "bg-purple-50 text-purple-600",
      });

      res.json({
        success: true,
        results,
        summary: {
          total: emailIds.length,
          processed: results.length,
          successful: successCount,
          failed: results.length - successCount
        }
      });
    } catch (error) {
      console.error("Batch analysis error:", error);
      res.status(500).json({ message: "Failed to perform batch analysis" });
    }
  });

  // AI accuracy validation endpoint
  app.post("/api/ai/validate", async (req, res) => {
    try {
      const { emailId, userFeedback, correctCategory } = req.body;
      
      const email = await storage.getEmailById(emailId);
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }

      // Perform fresh analysis
      const analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
      
      // Calculate accuracy based on user feedback
      const isCorrect = userFeedback === 'correct';
      const accuracyScore = isCorrect ? 1.0 : 0.0;
      
      // Update email if user provided correction
      if (correctCategory && !isCorrect) {
        const categories = await storage.getAllCategories();
        const category = categories.find(c => c.name === correctCategory);
        
        if (category) {
          await storage.updateEmail(emailId, {
            categoryId: category.id,
            confidence: 90, // High confidence for human correction
          });
        }
      }

      // Log validation activity
      await storage.createActivity({
        type: "review",
        description: "AI accuracy validation",
        details: `User feedback: ${userFeedback}${correctCategory ? ` | Corrected to: ${correctCategory}` : ''}`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-check-circle",
        iconBg: isCorrect ? "bg-green-50 text-green-600" : "bg-orange-50 text-orange-600",
      });

      res.json({
        success: true,
        validation: {
          original_analysis: analysis,
          user_feedback: userFeedback,
          accuracy_score: accuracyScore,
          corrected_category: correctCategory
        }
      });
    } catch (error) {
      console.error("Validation error:", error);
      res.status(500).json({ message: "Failed to validate AI analysis" });
    }
  });

  // AI engine health check
  app.get("/api/ai/health", async (_req, res) => {
    try {
      const isHealthy = await pythonNLP.testConnection();
      
      res.json({
        status: isHealthy ? 'healthy' : 'degraded',
        python_nlp: isHealthy,
        fallback_available: true,
        timestamp: new Date().toISOString()
      });
    } catch (error) {
      res.json({
        status: 'error',
        python_nlp: false,
        fallback_available: true,
        error: error.message,
        timestamp: new Date().toISOString()
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
