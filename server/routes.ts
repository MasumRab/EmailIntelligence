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
      console.time("storage.getDashboardStats");
      const stats = await storage.getDashboardStats();
      console.timeEnd("storage.getDashboardStats");
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch dashboard stats" });
    }
  });

  // Categories
  app.get("/api/categories", async (_req, res) => {
    try {
      console.time("storage.getAllCategories");
      const categories = await storage.getAllCategories();
      console.timeEnd("storage.getAllCategories");
      res.json(categories);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch categories" });
    }
  });

  app.post("/api/categories", async (req, res) => {
    try {
      const categoryData = insertCategorySchema.parse(req.body);
      console.time("storage.createCategory");
      const category = await storage.createCategory(categoryData);
      console.timeEnd("storage.createCategory");
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
      console.time("storage.updateCategory");
      const category = await storage.updateCategory(id, updateData);
      console.timeEnd("storage.updateCategory");
      
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
        console.time("storage.searchEmails");
        emails = await storage.searchEmails(search);
        console.timeEnd("storage.searchEmails");
      } else if (category && typeof category === 'string') {
        const categoryId = parseInt(category);
        console.time("storage.getEmailsByCategory");
        emails = await storage.getEmailsByCategory(categoryId);
        console.timeEnd("storage.getEmailsByCategory");
      } else {
        console.time("storage.getAllEmails");
        emails = await storage.getAllEmails();
        console.timeEnd("storage.getAllEmails");
      }
      
      res.json(emails);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch emails" });
    }
  });

  app.get("/api/emails/:id", async (req, res) => {
    try {
      const id = parseInt(req.params.id);
      console.time("storage.getEmailById");
      const email = await storage.getEmailById(id);
      console.timeEnd("storage.getEmailById");
      
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
      console.time("storage.createEmail");
      const email = await storage.createEmail(emailData);
      console.timeEnd("storage.createEmail");
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
      console.time("storage.updateEmail");
      const email = await storage.updateEmail(id, updateData);
      console.timeEnd("storage.updateEmail");
      
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
      console.time("storage.getRecentActivities");
      const activities = await storage.getRecentActivities(
        limit ? parseInt(limit as string) : undefined
      );
      console.timeEnd("storage.getRecentActivities");
      res.json(activities);
    } catch (error) {
      res.status(500).json({ message: "Failed to fetch activities" });
    }
  });

  app.post("/api/activities", async (req, res) => {
    try {
      const activityData = insertActivitySchema.parse(req.body);
      console.time("storage.createActivity");
      const activity = await storage.createActivity(activityData);
      console.timeEnd("storage.createActivity");
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
      console.time("storage.simulateGmailSync");
      const result = await storage.simulateGmailSync();
      console.timeEnd("storage.simulateGmailSync");
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

      console.time("pythonNLP.analyzeEmail");
      const analysis = await pythonNLP.analyzeEmail(subject, content);
      console.timeEnd("pythonNLP.analyzeEmail");
      
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
      
      console.time("storage.getEmailById_categorize"); // Unique label
      const email = await storage.getEmailById(emailId);
      console.timeEnd("storage.getEmailById_categorize");
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }

      let analysis: MappedNLPResult | undefined; // Updated type to MappedNLPResult
      if (autoAnalyze) {
        // Use advanced AI analysis
        console.time("pythonNLP.analyzeEmail_categorize"); // Unique label
        analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
        console.timeEnd("pythonNLP.analyzeEmail_categorize");
        
        // Find matching category
        console.time("storage.getAllCategories_categorize"); // Unique label
        const categories = await storage.getAllCategories();
        console.timeEnd("storage.getAllCategories_categorize");
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
          console.time("storage.updateEmail_categorize_auto"); // Unique label
          const updatedEmail = await storage.updateEmail(emailId, {
            categoryId: matchingCategory.id,
            confidence: Math.round(analysis!.confidence * 100), // Used non-null assertion
            labels: analysis!.suggestedLabels, // Fixed typo: suggested_labels to suggestedLabels
          });
          console.timeEnd("storage.updateEmail_categorize_auto");

          // Create detailed activity
          console.time("storage.createActivity_categorize_auto"); // Unique label
          await storage.createActivity({
            type: "label",
            description: "Advanced AI analysis completed",
            details: `${analysis!.categories.join(", ")} | Confidence: ${Math.round(analysis!.confidence * 100)}% | ${analysis!.validation.reliable ? 'High' : 'Low'} reliability`,
            timestamp: new Date().toISOString(),
            icon: "fas fa-brain",
            iconBg: analysis!.validation.reliable ? "bg-green-50 text-green-600" : "bg-yellow-50 text-yellow-600",
          });
          console.timeEnd("storage.createActivity_categorize_auto");

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
        
        console.time("storage.updateEmail_categorize_manual"); // Unique label
        const updatedEmail = await storage.updateEmail(emailId, {
          categoryId: categoryId,
          confidence: confidence || 95,
        });
        console.timeEnd("storage.updateEmail_categorize_manual");

        console.time("storage.createActivity_categorize_manual"); // Unique label
        await storage.createActivity({
          type: "label",
          description: "Manual email categorization",
          details: `Email "${email.subject}" manually categorized`,
          timestamp: new Date().toISOString(),
          icon: "fas fa-user",
          iconBg: "bg-blue-50 text-blue-600",
        });
        console.timeEnd("storage.createActivity_categorize_manual");
        
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
      console.time("storage.getAllCategories_batch_analyze");
      const categories = await storage.getAllCategories();
      console.timeEnd("storage.getAllCategories_batch_analyze");
      
      for (const emailId of emailIds.slice(0, 10)) { // Limit to 10 emails for performance
        try {
          console.time(`storage.getEmailById_batch_analyze_${emailId}`);
          const email = await storage.getEmailById(emailId);
          console.timeEnd(`storage.getEmailById_batch_analyze_${emailId}`);
          if (!email) continue;

          console.time(`pythonNLP.analyzeEmail_batch_analyze_${emailId}`);
          const analysis: MappedNLPResult = await pythonNLP.analyzeEmail(email.subject, email.content); // Updated type to MappedNLPResult
          console.timeEnd(`pythonNLP.analyzeEmail_batch_analyze_${emailId}`);
          
          // Find best matching category
          const matchingCategory = categories.find(cat => 
            analysis.categories.some((aiCat: string) =>
              cat.name.toLowerCase().includes(aiCat.toLowerCase()) ||
              aiCat.toLowerCase().includes(cat.name.toLowerCase())
            )
          );

          if (matchingCategory && analysis.validation.reliable) {
            console.time(`storage.updateEmail_batch_analyze_${emailId}`);
            await storage.updateEmail(emailId, {
              categoryId: matchingCategory.id,
              confidence: Math.round(analysis.confidence * 100),
              labels: analysis.suggestedLabels, // Fixed typo: suggested_labels to suggestedLabels
            });
            console.timeEnd(`storage.updateEmail_batch_analyze_${emailId}`);

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
      console.time("storage.createActivity_batch_analyze");
      await storage.createActivity({
        type: "label",
        description: "Batch AI analysis completed",
        details: `${successCount}/${emailIds.length} emails successfully analyzed and categorized`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-layer-group",
        iconBg: "bg-purple-50 text-purple-600",
      });
      console.timeEnd("storage.createActivity_batch_analyze");

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
      
      console.time("storage.getEmailById_validate");
      const email = await storage.getEmailById(emailId);
      console.timeEnd("storage.getEmailById_validate");
      if (!email) {
        return res.status(404).json({ message: "Email not found" });
      }

      // Perform fresh analysis
      console.time("pythonNLP.analyzeEmail_validate");
      const analysis = await pythonNLP.analyzeEmail(email.subject, email.content);
      console.timeEnd("pythonNLP.analyzeEmail_validate");
      
      // Calculate accuracy based on user feedback
      const isCorrect = userFeedback === 'correct';
      const accuracyScore = isCorrect ? 1.0 : 0.0;
      
      // Update email if user provided correction
      if (correctCategory && !isCorrect) {
        console.time("storage.getAllCategories_validate");
        const categories = await storage.getAllCategories();
        console.timeEnd("storage.getAllCategories_validate");
        const category = categories.find(c => c.name === correctCategory);
        
        if (category) {
          console.time("storage.updateEmail_validate");
          await storage.updateEmail(emailId, {
            categoryId: category.id,
            confidence: 90, // High confidence for human correction
          });
          console.timeEnd("storage.updateEmail_validate");
        }
      }

      // Log validation activity
      console.time("storage.createActivity_validate");
      await storage.createActivity({
        type: "review",
        description: "AI accuracy validation",
        details: `User feedback: ${userFeedback}${correctCategory ? ` | Corrected to: ${correctCategory}` : ''}`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-check-circle",
        iconBg: isCorrect ? "bg-green-50 text-green-600" : "bg-orange-50 text-orange-600",
      });
      console.timeEnd("storage.createActivity_validate");

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
      console.time("pythonNLP.testConnection");
      const isHealthy = await pythonNLP.testConnection();
      console.timeEnd("pythonNLP.testConnection");
      
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
      
      console.time("gmailAIService.executeSmartRetrieval");
      const result = await gmailAIService.executeSmartRetrieval(
        strategies,
        maxApiCalls,
        timeBudgetMinutes
      );
      console.timeEnd("gmailAIService.executeSmartRetrieval");
      
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
      console.time("gmailAIService.getRetrievalStrategies");
      const strategies = await gmailAIService.getRetrievalStrategies();
      console.timeEnd("gmailAIService.getRetrievalStrategies");
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

      console.time("gmailAIService.syncGmailEmails");
      const result = await gmailAIService.syncGmailEmails({
        maxEmails,
        queryFilter,
        includeAIAnalysis,
        strategies,
        timeBudgetMinutes
      });
      console.timeEnd("gmailAIService.syncGmailEmails");

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
      console.time("gmailAIService.syncInboxEmails");
      const result = await gmailAIService.syncInboxEmails(maxEmails);
      console.timeEnd("gmailAIService.syncInboxEmails");
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
      console.time("gmailAIService.syncImportantEmails");
      const result = await gmailAIService.syncImportantEmails(maxEmails);
      console.timeEnd("gmailAIService.syncImportantEmails");
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
      console.time("gmailAIService.syncWeeklyBatch");
      const result = await gmailAIService.syncWeeklyBatch(maxEmails);
      console.timeEnd("gmailAIService.syncWeeklyBatch");
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
      console.time("gmailAIService.getPerformanceMetrics");
      const metrics = await gmailAIService.getPerformanceMetrics();
      console.timeEnd("gmailAIService.getPerformanceMetrics");
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
      console.time("gmailAIService.getQuickPerformanceOverview");
      const overview = await gmailAIService.getQuickPerformanceOverview();
      console.timeEnd("gmailAIService.getQuickPerformanceOverview");
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

      console.time("gmailAIService.trainModelsFromGmail");
      const result = await gmailAIService.trainModelsFromGmail(
        trainingQuery,
        maxTrainingEmails
      );
      console.timeEnd("gmailAIService.trainModelsFromGmail");

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

      console.time("gmailAIService.applyAdaptiveOptimization");
      const result = await gmailAIService.applyAdaptiveOptimization(strategyName);
      console.timeEnd("gmailAIService.applyAdaptiveOptimization");
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
      console.time("gmailAIService.getPerformanceMetrics_quota");
      const metrics = await gmailAIService.getPerformanceMetrics();
      console.timeEnd("gmailAIService.getPerformanceMetrics_quota");
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
      console.time("gmailAIService.getPerformanceMetrics_alerts");
      const metrics = await gmailAIService.getPerformanceMetrics();
      console.timeEnd("gmailAIService.getPerformanceMetrics_alerts");
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
      console.time("gmailAIService.getPerformanceMetrics_recommendations");
      const metrics = await gmailAIService.getPerformanceMetrics();
      console.timeEnd("gmailAIService.getPerformanceMetrics_recommendations");
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
