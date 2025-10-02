/**
 * @file Service layer for handling AI-related business logic.
 *
 * This service orchestrates interactions between the API routes, the Python
 * NLP bridge, and the database storage for all AI-powered features, including
 * email analysis, categorization, and validation.
 */
import { storage } from "../storage";
import { pythonNLP, type MappedNLPResult } from "../python-bridge";
import { measureExecutionTime } from "../utils/performance";

export const aiService = {
  /**
   * Analyzes the subject and content of an email.
   * @param {string} subject - The subject of the email.
   * @param {string} content - The content of the email.
   * @returns {Promise<MappedNLPResult>} The analysis result from the Python NLP bridge.
   * @throws {Error} If subject or content are missing.
   */
  async analyzeEmail(subject: string, content: string) {
    if (!subject || !content) {
      throw new Error("Subject and content are required");
    }
    return await measureExecutionTime(() => pythonNLP.analyzeEmail(subject, content), "pythonNLP.analyzeEmail");
  },

  /**
   * Categorizes an email, either automatically using AI or manually.
   * @param {number} emailId - The ID of the email to categorize.
   * @param {boolean} autoAnalyze - If true, use AI to determine the category.
   * @param {number} [categoryId] - The category ID for manual categorization.
   * @param {number} [confidence] - The confidence score for manual categorization.
   * @returns {Promise<object>} An object containing the result of the operation.
   * @throws {Error} If the email is not found.
   */
  async categorizeEmail(emailId: number, autoAnalyze: boolean, categoryId?: number, confidence?: number) {
    const email = await measureExecutionTime(() => storage.getEmailById(emailId), `storage.getEmailById:${emailId}`);
    if (!email) {
      throw new Error("Email not found");
    }

    if (autoAnalyze) {
      const analysis: MappedNLPResult | undefined = await measureExecutionTime(() => pythonNLP.analyzeEmail(email.subject, email.content), `pythonNLP.analyzeEmail:${emailId}`);

      if (analysis && analysis.categoryId) {
        const updatedEmail = await measureExecutionTime(() => storage.updateEmail(emailId, {
          categoryId: analysis.categoryId,
          confidence: Math.round(analysis.confidence * 100),
          labels: analysis.suggestedLabels,
        }), `storage.updateEmail:${emailId}`);

        const assignedCategory = await measureExecutionTime(() => storage.getCategoryById(analysis.categoryId), `storage.getCategoryById:${analysis.categoryId}`);

        await measureExecutionTime(() => storage.createActivity({
          type: "label",
          description: "Advanced AI analysis completed",
          details: `${analysis.categories.join(", ")} | Confidence: ${Math.round(analysis.confidence * 100)}% | ${analysis.validation.reliable ? 'High' : 'Low'} reliability`,
          timestamp: new Date().toISOString(),
          icon: "fas fa-brain",
          iconBg: analysis.validation.reliable ? "bg-green-50 text-green-600" : "bg-yellow-50 text-yellow-600",
        }), "storage.createActivity");

        return {
          success: true,
          email: updatedEmail,
          analysis,
          categoryAssigned: assignedCategory ? assignedCategory.name : "Unknown"
        };
      } else {
        return {
          success: false,
          analysis,
          suggestion: analysis && analysis.categories.length > 0 ? "create_category" : "no_suggestion",
          suggestedCategory: analysis && analysis.categories.length > 0 ? analysis.categories[0] : undefined,
          message: "No matching category found or AI analysis did not provide a category ID."
        };
      }
    } else {
      const updatedEmail = await measureExecutionTime(() => storage.updateEmail(emailId, {
        categoryId: categoryId,
        confidence: confidence || 95,
      }), `storage.updateEmail:${emailId}`);

      await measureExecutionTime(() => storage.createActivity({
        type: "label",
        description: "Manual email categorization",
        details: `Email "${email.subject}" manually categorized`,
        timestamp: new Date().toISOString(),
        icon: "fas fa-user",
        iconBg: "bg-blue-50 text-blue-600",
      }), "storage.createActivity");

      return { success: true, email: updatedEmail };
    }
  },

  /**
   * Performs AI analysis on a batch of emails.
   * @param {number[]} emailIds - An array of email IDs to analyze.
   * @returns {Promise<object>} An object containing the results and a summary of the batch operation.
   * @throws {Error} If the email IDs array is not provided.
   */
  async batchAnalyzeEmails(emailIds: number[]) {
    if (!emailIds || !Array.isArray(emailIds)) {
      throw new Error("Email IDs array is required");
    }

    const results = [];
    for (const emailId of emailIds.slice(0, 10)) {
      try {
        const email = await measureExecutionTime(() => storage.getEmailById(emailId), `storage.getEmailById:${emailId}`);
        if (!email) continue;

        const analysis: MappedNLPResult = await measureExecutionTime(() => pythonNLP.analyzeEmail(email.subject, email.content), `pythonNLP.analyzeEmail:${emailId}`);

        let assignedCategoryName: string | undefined = undefined;
        if (analysis.categoryId && analysis.validation.reliable) {
          await measureExecutionTime(() => storage.updateEmail(emailId, {
            categoryId: analysis.categoryId,
            confidence: Math.round(analysis.confidence * 100),
            labels: analysis.suggestedLabels,
          }), `storage.updateEmail:${emailId}`);

          const assignedCategory = await measureExecutionTime(() => storage.getCategoryById(analysis.categoryId), `storage.getCategoryById:${analysis.categoryId}`);
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
      } catch (error) {
        results.push({
          emailId,
          success: false,
          reason: 'analysis_error',
          error: error instanceof Error ? error.message : String(error)
        });
      }
    }

    const successCount = results.filter(r => r.success).length;
    await measureExecutionTime(() => storage.createActivity({
      type: "label",
      description: "Batch AI analysis completed",
      details: `${successCount}/${emailIds.length} emails successfully analyzed and categorized`,
      timestamp: new Date().toISOString(),
      icon: "fas fa-layer-group",
      iconBg: "bg-purple-50 text-purple-600",
    }), "storage.createActivity");

    return {
      success: true,
      results,
      summary: {
        total: emailIds.length,
        processed: results.length,
        successful: successCount,
        failed: results.length - successCount
      }
    };
  },

  /**
   * Validates an AI analysis based on user feedback.
   * @param {number} emailId - The ID of the email being validated.
   * @param {string} userFeedback - The feedback from the user (e.g., 'correct', 'incorrect').
   * @param {string} [correctCategory] - The correct category, if provided by the user.
   * @returns {Promise<object>} An object containing the validation result.
   * @throws {Error} If the email is not found.
   */
  async validateAnalysis(emailId: number, userFeedback: string, correctCategory?: string) {
    const email = await measureExecutionTime(() => storage.getEmailById(emailId), `storage.getEmailById:${emailId}`);
    if (!email) {
      throw new Error("Email not found");
    }

    const analysis = await measureExecutionTime(() => pythonNLP.analyzeEmail(email.subject, email.content), `pythonNLP.analyzeEmail:${emailId}`);
    const isCorrect = userFeedback === 'correct';
    const accuracyScore = isCorrect ? 1.0 : 0.0;

    if (correctCategory && !isCorrect) {
      const categories = await measureExecutionTime(() => storage.getAllCategories(), "storage.getAllCategories");
      const category = categories.find(c => c.name === correctCategory);

      if (category) {
        await measureExecutionTime(() => storage.updateEmail(emailId, {
          categoryId: category.id,
          confidence: 90,
        }), `storage.updateEmail:${emailId}`);
      }
    }

    await measureExecutionTime(() => storage.createActivity({
      type: "review",
      description: "AI accuracy validation",
      details: `User feedback: ${userFeedback}${correctCategory ? ` | Corrected to: ${correctCategory}` : ''}`,
      timestamp: new Date().toISOString(),
      icon: "fas fa-check-circle",
      iconBg: isCorrect ? "bg-green-50 text-green-600" : "bg-orange-50 text-orange-600",
    }), "storage.createActivity");

    return {
      success: true,
      validation: {
        original_analysis: analysis,
        user_feedback: userFeedback,
        accuracy_score: accuracyScore,
        corrected_category: correctCategory
      }
    };
  },

  /**
   * Checks the health of the AI service and its connection to the Python NLP bridge.
   * @returns {Promise<object>} An object containing the health status of the service.
   */
  async getHealth() {
    try {
      const isHealthy = await measureExecutionTime(() => pythonNLP.testConnection(), "pythonNLP.testConnection");
      return {
        status: isHealthy ? 'healthy' : 'degraded',
        python_nlp: isHealthy,
        fallback_available: true,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return {
        status: 'error',
        python_nlp: false,
        fallback_available: true,
        error: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      };
    }
  }
};