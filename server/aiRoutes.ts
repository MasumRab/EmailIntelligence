import express from "express";
import { aiService } from "./services/aiService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

// Advanced AI Analysis
router.post("/analyze", asyncHandler(async (req, res) => {
  const { subject, content } = req.body;
  const analysis = await aiService.analyzeEmail(subject, content);
  res.json(analysis);
}));

// Enhanced AI categorization with accuracy validation
router.post("/categorize", asyncHandler(async (req, res) => {
  const { emailId, autoAnalyze, categoryId, confidence } = req.body;
  const result = await aiService.categorizeEmail(emailId, autoAnalyze, categoryId, confidence);
  res.json(result);
}));

// Batch AI processing
router.post("/batch-analyze", asyncHandler(async (req, res) => {
  const { emailIds } = req.body;
  const results = await aiService.batchAnalyzeEmails(emailIds);
  res.json(results);
}));

// AI accuracy validation endpoint
router.post("/validate", asyncHandler(async (req, res) => {
  const { emailId, userFeedback, correctCategory } = req.body;
  const result = await aiService.validateAnalysis(emailId, userFeedback, correctCategory);
  res.json(result);
}));

// AI engine health check
router.get("/health", asyncHandler(async (_req, res) => {
  const health = await aiService.getHealth();
  res.json(health);
}));

export default router;
