import express from "express";
import { storage } from "./storage";
import { pythonNLP, type MappedNLPResult } from "./python-bridge"; // Import MappedNLPResult

const router = express.Router();

// Advanced AI Analysis
router.post("/analyze", async (req, res) => {
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
router.post("/categorize", async (req, res) => {
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
      analysis = await pythonNLP.analyzeEmail(email.subject, email.content); // analysis contains categoryId
      console.timeEnd("pythonNLP.analyzeEmail_categorize");

      if (analysis && analysis.categoryId) {
        // Update email with AI analysis results
        console.time("storage.updateEmail_categorize_auto");
        const updatedEmail = await storage.updateEmail(emailId, {
          categoryId: analysis.categoryId, // Use categoryId from Python analysis
          confidence: Math.round(analysis.confidence * 100),
          labels: analysis.suggestedLabels,
        });
        console.timeEnd("storage.updateEmail_categorize_auto");

        // Fetch category name for response
        const assignedCategory = await storage.getCategoryById(analysis.categoryId);

        // Create detailed activity
        console.time("storage.createActivity_categorize_auto");
        await storage.createActivity({
          type: "label",
          description: "Advanced AI analysis completed",
          details: `${analysis.categories.join(", ")} | Confidence: ${Math.round(analysis.confidence * 100)}% | ${analysis.validation.reliable ? 'High' : 'Low'} reliability`,
          timestamp: new Date().toISOString(),
          icon: "fas fa-brain",
          iconBg: analysis.validation.reliable ? "bg-green-50 text-green-600" : "bg-yellow-50 text-yellow-600",
        });
        console.timeEnd("storage.createActivity_categorize_auto");

        res.json({
          success: true,
          email: updatedEmail,
          analysis,
          categoryAssigned: assignedCategory ? assignedCategory.name : "Unknown"
        });
      } else {
        // No matching category found by Python, or analysis failed to provide categoryId
        res.json({
          success: false,
          analysis,
          suggestion: analysis && analysis.categories.length > 0 ? "create_category" : "no_suggestion",
          suggestedCategory: analysis && analysis.categories.length > 0 ? analysis.categories[0] : undefined,
          message: "No matching category found or AI analysis did not provide a category ID."
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
router.post("/batch-analyze", async (req, res) => {
  try {
    const { emailIds } = req.body;

    if (!emailIds || !Array.isArray(emailIds)) {
      return res.status(400).json({ message: "Email IDs array is required" });
    }

    const results = [];
    // No longer need to fetch all categories here for matching

    for (const emailId of emailIds.slice(0, 10)) { // Limit to 10 emails for performance
      try {
        console.time(`storage.getEmailById_batch_analyze_${emailId}`);
        const email = await storage.getEmailById(emailId);
        console.timeEnd(`storage.getEmailById_batch_analyze_${emailId}`);
        if (!email) continue;

        console.time(`pythonNLP.analyzeEmail_batch_analyze_${emailId}`);
        const analysis: MappedNLPResult = await pythonNLP.analyzeEmail(email.subject, email.content); // analysis contains categoryId
        console.timeEnd(`pythonNLP.analyzeEmail_batch_analyze_${emailId}`);

        let assignedCategoryName: string | undefined = undefined;
        if (analysis.categoryId && analysis.validation.reliable) {
          console.time(`storage.updateEmail_batch_analyze_${emailId}`);
          await storage.updateEmail(emailId, {
            categoryId: analysis.categoryId, // Use categoryId from Python analysis
            confidence: Math.round(analysis.confidence * 100),
            labels: analysis.suggestedLabels,
          });
          console.timeEnd(`storage.updateEmail_batch_analyze_${emailId}`);

          // Fetch category name for result
          const assignedCategory = await storage.getCategoryById(analysis.categoryId);
          assignedCategoryName = assignedCategory ? assignedCategory.name : "Unknown";

          results.push({
            emailId,
            success: true,
            category: assignedCategoryName,
            confidence: analysis.confidence,
            analysis
          });
        } else {
          results.push({
            emailId,
            success: false,
            reason: analysis.categoryId ? 'low_confidence' : 'no_matching_category_id_from_ai',
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
router.post("/validate", async (req, res) => {
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
router.get("/health", async (_req, res) => {
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

export default router;
