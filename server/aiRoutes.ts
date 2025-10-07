/**
 * @file Defines the API routes for AI-related operations.
 *
 * This file creates an Express router and attaches routes for handling
 * AI-powered email analysis, categorization, batch processing, and health checks.
 * It uses the `aiService` to perform the actual business logic.
 */
import express from "express";
import { aiService } from "./services/aiService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

/**
 * @route POST /api/ai/analyze
 * @description Analyzes the subject and content of an email to extract insights.
 * @param {object} req.body - The request body.
 * @param {string} req.body.subject - The subject of the email.
 * @param {string} req.body.content - The content of the email.
 * @returns {object} The AI analysis results.
 */
router.post("/analyze", asyncHandler(async (req, res) => {
  const { subject, content } = req.body;
  const analysis = await aiService.analyzeEmail(subject, content);
  res.json(analysis);
}));

/**
 * @route POST /api/ai/categorize
 * @description Categorizes an email using the AI engine and validates its accuracy.
 * @param {object} req.body - The request body.
 * @param {string} req.body.emailId - The ID of the email to categorize.
 * @param {boolean} req.body.autoAnalyze - Whether to perform auto-analysis.
 * @param {string} req.body.categoryId - The ID of the category to assign.
 * @param {number} req.body.confidence - The confidence score of the categorization.
 * @returns {object} The result of the categorization.
 */
router.post("/categorize", asyncHandler(async (req, res) => {
  const { emailId, autoAnalyze, categoryId, confidence } = req.body;
  const result = await aiService.categorizeEmail(emailId, autoAnalyze, categoryId, confidence);
  res.json(result);
}));

/**
 * @route POST /api/ai/batch-analyze
 * @description Performs AI analysis on a batch of emails.
 * @param {object} req.body - The request body.
 * @param {string[]} req.body.emailIds - An array of email IDs to analyze.
 * @returns {object} The results of the batch analysis.
 */
router.post("/batch-analyze", asyncHandler(async (req, res) => {
  const { emailIds } = req.body;
  const results = await aiService.batchAnalyzeEmails(emailIds);
  res.json(results);
}));

/**
 * @route POST /api/ai/validate
 * @description Validates the AI analysis of an email based on user feedback.
 * @param {object} req.body - The request body.
 * @param {string} req.body.emailId - The ID of the email to validate.
 * @param {object} req.body.userFeedback - The user's feedback on the analysis.
 * @param {string} req.body.correctCategory - The correct category for the email.
 * @returns {object} The result of the validation.
 */
router.post("/validate", asyncHandler(async (req, res) => {
  const { emailId, userFeedback, correctCategory } = req.body;
  const result = await aiService.validateAnalysis(emailId, userFeedback, correctCategory);
  res.json(result);
}));

/**
 * @route GET /api/ai/health
 * @description Checks the health status of the AI engine.
 * @returns {object} The health status of the AI engine.
 */
router.get("/health", asyncHandler(async (_req, res) => {
  const health = await aiService.getHealth();
  res.json(health);
}));

export default router;