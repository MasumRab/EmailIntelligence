import express from "express";
import { storage } from "./storage";
import { gmailAIService } from "./gmail-ai-service";

const router = express.Router();

// Gmail sync simulation
router.post("/sync", async (req, res) => {
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

// Gmail Smart Retrieval Routes
// Execute smart Gmail retrieval with multiple strategies
router.post("/smart-retrieval", async (req, res) => {
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
router.get("/strategies", async (_req, res) => {
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

// Quick inbox sync
router.post("/sync-inbox", async (req, res) => {
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
router.post("/sync-important", async (req, res) => {
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
router.post("/weekly-batch", async (req, res) => {
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

// AI Training Routes
// Train models from Gmail data
router.post("/train-models", async (req, res) => {
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
router.post("/optimize", async (req, res) => {
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
router.get("/quota-status", async (_req, res) => {
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
router.get("/alerts", async (_req, res) => {
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
router.get("/recommendations", async (_req, res) => {
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

export default router;
