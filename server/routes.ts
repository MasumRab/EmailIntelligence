import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertEmailSchema, insertCategorySchema, insertActivitySchema, type EmailWithCategory } from "@shared/schema";
import { pythonNLP, type MappedNLPResult } from "./python-bridge"; // Import MappedNLPResult
import { gmailAIService } from "./gmail-ai-service";
import { z } from "zod";
import type { AIAnalysis, AccuracyValidation } from "./ai-engine"; /**
 * Registers all HTTP API routes for dashboard statistics, categories, emails, activities, AI analysis and categorization, Gmail synchronization, performance monitoring, AI training, optimization, and utility endpoints on the provided Express app, and returns an HTTP server instance.
 *
 * @param app - The Express application instance to register routes on.
 * @returns The created HTTP server with all routes registered.
 *
 * @remark
 * The registered routes include endpoints for CRUD operations on categories, emails, and activities; advanced AI-powered email analysis and categorization (including batch and validation workflows); Gmail synchronization and smart retrieval; performance and quota monitoring; AI model training and optimization; and utility endpoints for alerts and recommendations. Most endpoints handle errors by returning appropriate HTTP status codes and JSON error messages.
 */

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

      let analysis: MappedNLPResult | undefined; // Updated type to MappedNLPResult
      if (autoAnalyze) {
        // Use advanced AI analysis
        analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
        
        // Find matching category
        const categories = await storage.getAllCategories();
        // analysis is now MappedNLPResult, which includes 'validation'
        // and has camelCase 'suggestedLabels' and 'riskFlags'
        const matchingCategory = categories.find(cat => 
          analysis!.categories.some((aiCat: string) =>
            cat.name.toLowerCase().includes(aiCat.toLowerCase()) ||
            aiCat.toLowerCase().includes(cat.name.toLowerCase())
          )
        );

        if (matchingCategory) {
          // Update email with AI analysis results
          const updatedEmail = await storage.updateEmail(emailId, {
            categoryId: matchingCategory.id,
            confidence: Math.round(analysis!.confidence * 100), // Used non-null assertion
            labels: analysis!.suggestedLabels, // Fixed typo: suggested_labels to suggestedLabels
          });

          // Create detailed activity
          await storage.createActivity({
            type: "label",
            description: "Advanced AI analysis completed",
            details: `${analysis!.categories.join(", ")} | Confidence: ${Math.round(analysis!.confidence * 100)}% | ${analysis!.validation.reliable ? 'High' : 'Low'} reliability`,
            timestamp: new Date().toISOString(),
            icon: "fas fa-brain",
            iconBg: analysis!.validation.reliable ? "bg-green-50 text-green-600" : "bg-yellow-50 text-yellow-600",
          });

          res.json({ 
            success: true, 
            email: updatedEmail, 
            analysis, // analysis can be undefined here if autoAnalyze is false, but it's guarded by if (autoAnalyze)
            categoryAssigned: matchingCategory.name
          });
        } else {
          // No matching category found, suggest creating new one
          res.json({ 
            success: false, 
            analysis, // analysis can be undefined here
            suggestion: "create_category",
            suggestedCategory: analysis!.categories[0], // Used non-null assertion, potentially unsafe if analysis is undefined
            message: "No matching category found. Consider creating a new category."
          });
        }
      } else {
        // Manual categorization (existing logic)
        // analysis remains undefined here
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

          const analysis: MappedNLPResult = await pythonNLP.analyzeEmail(email.subject, email.content); // Updated type to MappedNLPResult
          
          // Find best matching category
          const matchingCategory = categories.find(cat => 
            analysis.categories.some((aiCat: string) =>
              cat.name.toLowerCase().includes(aiCat.toLowerCase()) ||
              aiCat.toLowerCase().includes(cat.name.toLowerCase())
            )
          );

          if (matchingCategory && analysis.validation.reliable) {
            await storage.updateEmail(emailId, {
              categoryId: matchingCategory.id,
              confidence: Math.round(analysis.confidence * 100),
              labels: analysis.suggestedLabels, // Fixed typo: suggested_labels to suggestedLabels
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
        } catch (error) { // error is unknown here
          results.push({
            emailId,
            success: false,
            reason: 'analysis_error',
            error: error instanceof Error ? error.message : String(error) // Handled unknown error
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
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      });
    }
  });

  // Gmail Smart Retrieval Routes
  
  // Execute smart Gmail retrieval with multiple strategies
  app.post("/api/gmail/smart-retrieval", async (req, res) => {
    try {
      const { strategies = [], maxApiCalls = 100, timeBudgetMinutes = 30 } = req.body;
      
      const result = await gmailAIService.executeSmartRetrieval(
        strategies,
        maxApiCalls,
        timeBudgetMinutes
      );
      
      res.json(result);
    } catch (error) {
      console.error("Smart retrieval failed:", error);
      res.status(500).json({ 
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        processedCount: 0 
      });
    }
  });

  // Get available retrieval strategies
  app.get("/api/gmail/strategies", async (_req, res) => {
    try {
      const strategies = await gmailAIService.getRetrievalStrategies();
      res.json({ strategies });
    } catch (error) {
      console.error("Failed to get strategies:", error);
      res.status(500).json({ 
        error: error instanceof Error ? error.message : 'Unknown error',
        strategies: [] 
      });
    }
  });

  // Sync Gmail emails with specific configuration
  app.post("/api/gmail/sync", async (req, res) => {
    try {
      const {
        maxEmails = 500,
        queryFilter = "newer_than:1d",
        includeAIAnalysis = true,
        strategies = [],
        timeBudgetMinutes = 15
      } = req.body;

      const result = await gmailAIService.syncGmailEmails({
        maxEmails,
        queryFilter,
        includeAIAnalysis,
        strategies,
        timeBudgetMinutes
      });

      res.json(result);
    } catch (error) {
      console.error("Gmail sync failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        processedCount: 0
      });
    }
  });

  // Quick inbox sync
  app.post("/api/gmail/sync-inbox", async (req, res) => {
    try {
      const { maxEmails = 500 } = req.body;
      const result = await gmailAIService.syncInboxEmails(maxEmails);
      res.json(result);
    } catch (error) {
      console.error("Inbox sync failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        processedCount: 0
      });
    }
  });

  // Sync important emails
  app.post("/api/gmail/sync-important", async (req, res) => {
    try {
      const { maxEmails = 200 } = req.body;
      const result = await gmailAIService.syncImportantEmails(maxEmails);
      res.json(result);
    } catch (error) {
      console.error("Important emails sync failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        processedCount: 0
      });
    }
  });

  // Weekly batch processing
  app.post("/api/gmail/weekly-batch", async (req, res) => {
    try {
      const { maxEmails = 2000 } = req.body;
      const result = await gmailAIService.syncWeeklyBatch(maxEmails);
      res.json(result);
    } catch (error) {
      console.error("Weekly batch failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        processedCount: 0
      });
    }
  });

  // Performance Monitoring Routes

  // Get comprehensive performance metrics
  app.get("/api/gmail/performance", async (_req, res) => {
    try {
      const metrics = await gmailAIService.getPerformanceMetrics();
      if (metrics) {
        res.json(metrics);
      } else {
        res.json({
          timestamp: new Date().toISOString(),
          overallStatus: { status: 'no_data' },
          quotaStatus: { dailyUsage: { percentage: 0 } },
          strategyPerformance: [],
          alerts: [],
          recommendations: []
        });
      }
    } catch (error) {
      console.error("Failed to get performance metrics:", error);
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      });
    }
  });

  // Get quick performance overview
  app.get("/api/gmail/performance/overview", async (_req, res) => {
    try {
      const overview = await gmailAIService.getQuickPerformanceOverview();
      res.json(overview || {
        status: 'unknown',
        efficiency: 0,
        quotaUsed: 0,
        activeStrategies: 0,
        alertCount: 0,
        recommendationCount: 0
      });
    } catch (error) {
      console.error("Failed to get performance overview:", error);
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });

  // AI Training Routes

  // Train models from Gmail data
  app.post("/api/gmail/train-models", async (req, res) => {
    try {
      const {
        trainingQuery = "newer_than:30d",
        maxTrainingEmails = 5000
      } = req.body;

      const result = await gmailAIService.trainModelsFromGmail(
        trainingQuery,
        maxTrainingEmails
      );

      res.json(result);
    } catch (error) {
      console.error("Model training failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });

  // Apply adaptive optimization to a strategy
  app.post("/api/gmail/optimize", async (req, res) => {
    try {
      const { strategyName } = req.body;
      
      if (!strategyName) {
        return res.status(400).json({
          success: false,
          error: "Strategy name is required"
        });
      }

      const result = await gmailAIService.applyAdaptiveOptimization(strategyName);
      res.json(result);
    } catch (error) {
      console.error("Optimization failed:", error);
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });

  // Utility Routes

  // Get Gmail API rate limit status
  app.get("/api/gmail/quota-status", async (_req, res) => {
    try {
      const metrics = await gmailAIService.getPerformanceMetrics();
      if (metrics?.quotaStatus) {
        res.json(metrics.quotaStatus);
      } else {
        res.json({
          dailyUsage: { used: 0, limit: 1000000000, percentage: 0, remaining: 1000000000 },
          hourlyUsage: { used: 0, limit: 250, percentage: 0, remaining: 250 },
          projectedDailyUsage: 0
        });
      }
    } catch (error) {
      console.error("Failed to get quota status:", error);
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  });

  // Get active alerts
  app.get("/api/gmail/alerts", async (_req, res) => {
    try {
      const metrics = await gmailAIService.getPerformanceMetrics();
      res.json({
        alerts: metrics?.alerts || [],
        count: metrics?.alerts?.length || 0
      });
    } catch (error) {
      console.error("Failed to get alerts:", error);
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Unknown error',
        alerts: [],
        count: 0
      });
    }
  });

  // Get optimization recommendations
  app.get("/api/gmail/recommendations", async (_req, res) => {
    try {
      const metrics = await gmailAIService.getPerformanceMetrics();
      res.json({
        recommendations: metrics?.recommendations || [],
        count: metrics?.recommendations?.length || 0
      });
    } catch (error) {
      console.error("Failed to get recommendations:", error);
      res.status(500).json({
        error: error instanceof Error ? error.message : 'Unknown error',
        recommendations: [],
        count: 0
      });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
