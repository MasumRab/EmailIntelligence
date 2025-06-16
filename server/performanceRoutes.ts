import express from "express";
import { gmailAIService } from "./gmail-ai-service";

const router = express.Router();

// Performance Monitoring Routes
// Get comprehensive performance metrics
router.get("/", async (_req, res) => {
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
router.get("/overview", async (_req, res) => {
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

export default router;
