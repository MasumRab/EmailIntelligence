import { z } from "zod";

// AI Analysis Result Schema
export const aiAnalysisSchema = z.object({
  topic: z.string(),
  sentiment: z.enum(["positive", "negative", "neutral"]),
  intent: z.string(),
  urgency: z.enum(["low", "medium", "high", "critical"]),
  confidence: z.number().min(0).max(1),
  categories: z.array(z.string()),
  keywords: z.array(z.string()),
  reasoning: z.string(),
  suggestedLabels: z.array(z.string()),
  riskFlags: z.array(z.string()).optional(),
  categoryId: z.number().optional(), // Added categoryId
});

export type AIAnalysis = z.infer<typeof aiAnalysisSchema>;

// Accuracy validation schema
export const accuracyValidationSchema = z.object({
  validationMethod: z.enum(["cross_validation", "ensemble", "confidence_threshold", "human_feedback"]),
  score: z.number().min(0).max(1),
  reliable: z.boolean(),
  feedback: z.string().optional(),
});

export type AccuracyValidation = z.infer<typeof accuracyValidationSchema>;

// Free language model interface
interface FreeLanguageModel {
  name: string;
  apiUrl: string;
  analyze(text: string): Promise<Partial<AIAnalysis>>;
}

class HuggingFaceModel implements FreeLanguageModel {
  name = "HuggingFace Transformers";
  apiUrl = "https://api-inference.huggingface.co/models";

  async analyze(text: string): Promise<Partial<AIAnalysis>> {
    try {
      // Use multiple free models for different tasks
      const [sentiment, classification] = await Promise.all([
        this.analyzeSentiment(text),
        this.classifyText(text)
      ]);

      return {
        sentiment: sentiment.sentiment,
        categories: classification.categories,
        confidence: Math.min(sentiment.confidence || 0.5, classification.confidence || 0.5),
        keywords: this.extractKeywords(text),
        topic: classification.topic || "General",
        intent: this.detectIntent(text),
        urgency: this.assessUrgency(text),
        reasoning: `Analysis based on sentiment: ${sentiment}, classification: ${JSON.stringify(classification)}`
      };
    } catch (error) {
      console.error("HuggingFace analysis error:", error);
      return this.getFallbackAnalysis(text);
    }
  }

  private async analyzeSentiment(text: string): Promise<{ sentiment: "positive" | "negative" | "neutral", confidence: number }> {
    // Simulate sentiment analysis using pattern matching
    const positiveWords = ["good", "great", "excellent", "happy", "pleased", "thank", "wonderful"];
    const negativeWords = ["bad", "terrible", "awful", "angry", "disappointed", "upset", "problem", "issue"];
    
    const words = text.toLowerCase().split(/\s+/);
    const positiveCount = words.filter(word => positiveWords.some(pos => word.includes(pos))).length;
    const negativeCount = words.filter(word => negativeWords.some(neg => word.includes(neg))).length;
    
    let sentiment: "positive" | "negative" | "neutral";
    let confidence: number;

    if (positiveCount > negativeCount) {
      sentiment = "positive";
      confidence = Math.min(0.5 + (positiveCount - negativeCount) * 0.1, 0.9); // Confidence increases with more positive words
    } else if (negativeCount > positiveCount) {
      sentiment = "negative";
      confidence = Math.min(0.5 + (negativeCount - positiveCount) * 0.1, 0.9); // Confidence increases with more negative words
    } else {
      sentiment = "neutral";
      confidence = 0.6; // Neutral sentiment has a base confidence
    }
    return { sentiment, confidence };
  }

  private async classifyText(text: string) {
    // Rule-based classification for demo purposes
    const categories = [];
    const lowerText = text.toLowerCase();
    
    if (lowerText.includes("meeting") || lowerText.includes("conference") || lowerText.includes("project")) {
      categories.push("Work & Business");
    }
    if (lowerText.includes("bank") || lowerText.includes("payment") || lowerText.includes("invoice")) {
      categories.push("Finance & Banking");
    }
    if (lowerText.includes("family") || lowerText.includes("personal") || lowerText.includes("friend")) {
      categories.push("Personal & Family");
    }
    if (lowerText.includes("promotion") || lowerText.includes("sale") || lowerText.includes("offer")) {
      categories.push("Promotions & Marketing");
    }
    if (lowerText.includes("doctor") || lowerText.includes("appointment") || lowerText.includes("health")) {
      categories.push("Healthcare");
    }
    if (lowerText.includes("travel") || lowerText.includes("flight") || lowerText.includes("hotel")) {
      categories.push("Travel");
    }

    return {
      categories: categories.length > 0 ? categories : ["General"],
      confidence: categories.length > 0 ? 0.8 : 0.4,
      topic: categories[0] || "General"
    };
  }

  private extractKeywords(text: string): string[] {
    // Simple keyword extraction
    const stopWords = new Set(["the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should"]);
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const keywords = words
      .filter(word => word.length > 3 && !stopWords.has(word))
      .reduce((acc: { [key: string]: number }, word) => {
        acc[word] = (acc[word] || 0) + 1;
        return acc;
      }, {});
    
    return Object.entries(keywords)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 5)
      .map(([word]) => word);
  }

  private detectIntent(text: string): string {
    const lowerText = text.toLowerCase();
    if (lowerText.includes("question") || lowerText.includes("?") || lowerText.includes("how") || lowerText.includes("what")) {
      return "inquiry";
    }
    if (lowerText.includes("thank") || lowerText.includes("appreciate")) {
      return "gratitude";
    }
    if (lowerText.includes("please") || lowerText.includes("request") || lowerText.includes("need")) {
      return "request";
    }
    if (lowerText.includes("confirm") || lowerText.includes("schedule") || lowerText.includes("meeting")) {
      return "scheduling";
    }
    if (lowerText.includes("urgent") || lowerText.includes("asap") || lowerText.includes("immediately")) {
      return "urgent_action";
    }
    return "informational";
  }

  private assessUrgency(text: string): "low" | "medium" | "high" | "critical" {
    const lowerText = text.toLowerCase();
    if (lowerText.includes("urgent") || lowerText.includes("asap") || lowerText.includes("emergency") || lowerText.includes("critical")) {
      return "critical";
    }
    if (lowerText.includes("soon") || lowerText.includes("quickly") || lowerText.includes("priority")) {
      return "high";
    }
    if (lowerText.includes("when you can") || lowerText.includes("this week") || lowerText.includes("deadline")) {
      return "medium";
    }
    return "low";
  }

  private getFallbackAnalysis(text: string): Partial<AIAnalysis> {
    return {
      sentiment: "neutral",
      categories: ["General"],
      confidence: 0.3,
      keywords: this.extractKeywords(text),
      topic: "General",
      intent: "informational",
      urgency: "low",
      reasoning: "Fallback analysis due to API limitations"
    };
  }
}

class LocalNLPModel implements FreeLanguageModel {
  name = "Local Pattern Matching";
  apiUrl = "local";

  async analyze(text: string): Promise<Partial<AIAnalysis>> {
    // Enhanced pattern-based analysis
    const analysis = {
      sentiment: this.analyzeSentiment(text),
      categories: this.categorizeEmail(text),
      confidence: this.calculateConfidence(text),
      keywords: this.extractAdvancedKeywords(text),
      topic: this.extractTopic(text),
      intent: this.detectAdvancedIntent(text),
      urgency: this.assessDetailedUrgency(text),
      suggestedLabels: this.generateLabels(text),
      reasoning: "Local pattern-based analysis with enhanced rules"
    };

    return analysis;
  }

  private analyzeSentiment(text: string): "positive" | "negative" | "neutral" {
    const sentimentPatterns = {
      positive: [
        /\b(thank|thanks|grateful|appreciate|excellent|great|wonderful|amazing|perfect|love|happy|pleased|delighted|fantastic|awesome|brilliant)\b/gi,
        /\b(well done|good job|congratulations|success|achievement|accomplishment)\b/gi,
        /[😊😄🙂👍✅💯🎉]/g
      ],
      negative: [
        /\b(sorry|apologize|problem|issue|error|mistake|trouble|difficult|frustrated|disappointed|upset|angry|terrible|awful|horrible|disaster)\b/gi,
        /\b(can't|won't|unable|impossible|failed|failure|broken|urgent|asap|emergency)\b/gi,
        /[😔😞😢😠💔❌🚨]/g
      ]
    };

    let positiveScore = 0;
    let negativeScore = 0;

    sentimentPatterns.positive.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) positiveScore += matches.length;
    });

    sentimentPatterns.negative.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) negativeScore += matches.length;
    });

    if (positiveScore > negativeScore + 1) return "positive";
    if (negativeScore > positiveScore + 1) return "negative";
    return "neutral";
  }

  private categorizeEmail(text: string): string[] {
    const categoryPatterns = {
      "Work & Business": [
        /\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|colleague|office|work|business|professional|corporate|company|organization)\b/gi,
        /\b(schedule|calendar|appointment|discussion|review|analysis|strategy|planning|development|implementation)\b/gi
      ],
      "Finance & Banking": [
        /\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|money|financial|insurance|investment|loan|mortgage)\b/gi,
        /\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b/gi
      ],
      "Personal & Family": [
        /\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend|dinner|lunch|home|house|kids|children|spouse|partner|relative)\b/gi,
        /\b(mom|dad|mother|father|sister|brother|grandma|grandpa|aunt|uncle|cousin)\b/gi
      ],
      "Healthcare": [
        /\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine|treatment|therapy|checkup|surgery|dental|pharmacy)\b/gi,
        /\b(symptoms|diagnosis|patient|nurse|physician|specialist|emergency|ambulance)\b/gi
      ],
      "Travel": [
        /\b(travel|flight|hotel|booking|reservation|trip|vacation|destination|airport|airline|passport|visa|itinerary|accommodation)\b/gi,
        /\b(departure|arrival|boarding|check-in|luggage|baggage)\b/gi
      ],
      "Promotions & Marketing": [
        /\b(sale|discount|offer|promotion|deal|coupon|newsletter|marketing|advertisement|special|limited|exclusive|free|save|percent off)\b/gi,
        /%\s*off|free shipping|limited time|act now|don't miss/gi
      ],
      "Education": [
        /\b(school|university|college|student|teacher|professor|course|class|lecture|assignment|homework|exam|grade|study|education|academic)\b/gi,
        /\b(semester|tuition|scholarship|graduation|degree|diploma)\b/gi
      ],
      "Technology": [
        /\b(software|hardware|computer|laptop|mobile|app|application|website|internet|email|password|account|login|update|upgrade|bug|feature)\b/gi,
        /\b(server|database|API|code|programming|development|tech|technical|IT|support)\b/gi
      ]
    };

    const categories: string[] = [];
    for (const [category, patterns] of Object.entries(categoryPatterns)) {
      const score = patterns.reduce((sum, pattern) => {
        const matches = text.match(pattern);
        return sum + (matches ? matches.length : 0);
      }, 0);
      
      if (score > 0) {
        categories.push(category);
      }
    }

    return categories.length > 0 ? categories : ["General"];
  }

  private calculateConfidence(text: string): number {
    // Calculate confidence based on text length, keyword density, and pattern matches
    const baseConfidence = 0.6;
    const textLength = text.length;
    const wordCount = text.split(/\s+/).length;
    
    let confidence = baseConfidence;
    
    // Longer, more detailed emails get higher confidence
    if (textLength > 500) confidence += 0.2;
    else if (textLength > 200) confidence += 0.1;
    
    // Emails with more keywords get higher confidence
    if (wordCount > 50) confidence += 0.1;
    
    // Cap at 0.95 for local analysis
    return Math.min(confidence, 0.95);
  }

  private extractAdvancedKeywords(text: string): string[] {
    const stopWords = new Set([
      "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by",
      "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did",
      "will", "would", "could", "should", "can", "may", "might", "must", "shall", "this", "that",
      "these", "those", "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them"
    ]);

    // Extract named entities and important terms
    const entityPatterns = [
      /\b[A-Z][a-z]+ [A-Z][a-z]+\b/g, // Names
      /\b[A-Z]{2,}\b/g, // Acronyms
      /\b\w+@\w+\.\w+\b/g, // Emails
      /\b\d{1,2}\/\d{1,2}\/\d{4}\b/g, // Dates
      /\$[\d,]+/g, // Money
    ];

    const entities: string[] = [];
    entityPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) entities.push(...matches);
    });

    // Extract regular keywords
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const keywordFreq: { [key: string]: number } = {};
    
    words.forEach(word => {
      if (word.length > 3 && !stopWords.has(word)) {
        keywordFreq[word] = (keywordFreq[word] || 0) + 1;
      }
    });

    const topKeywords = Object.entries(keywordFreq)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 8)
      .map(([word]) => word);

    return [...new Set([...entities.slice(0, 3), ...topKeywords])].slice(0, 10);
  }

  private extractTopic(text: string): string {
    const categories = this.categorizeEmail(text);
    return categories[0] || "General Discussion";
  }

  private detectAdvancedIntent(text: string): string {
    const intentPatterns = {
      "request": /\b(please|could you|would you|can you|need|require|request|ask|help|assist)\b/gi,
      "inquiry": /\b(question|ask|wonder|curious|information|details|clarification|explain|how|what|when|where|why|which)\b/gi,
      "scheduling": /\b(schedule|calendar|meeting|appointment|time|date|available|busy|free|reschedule)\b/gi,
      "confirmation": /\b(confirm|confirmation|verify|check|ensure|validate|acknowledge)\b/gi,
      "complaint": /\b(complaint|complain|issue|problem|dissatisfied|unhappy|wrong|error|mistake)\b/gi,
      "gratitude": /\b(thank|thanks|grateful|appreciate|acknowledgment|recognition)\b/gi,
      "urgent_action": /\b(urgent|asap|immediately|emergency|critical|priority|deadline|rush)\b/gi,
      "follow_up": /\b(follow up|follow-up|checking in|status|update|progress|reminder)\b/gi,
      "notification": /\b(notify|notification|alert|inform|update|announcement|notice)\b/gi,
      "approval": /\b(approve|approval|authorize|permission|consent|agree|accept)\b/gi
    };

    let maxScore = 0;
    let detectedIntent = "informational";

    for (const [intent, pattern] of Object.entries(intentPatterns)) {
      const matches = text.match(pattern);
      const score = matches ? matches.length : 0;
      if (score > maxScore) {
        maxScore = score;
        detectedIntent = intent;
      }
    }

    return detectedIntent;
  }

  private assessDetailedUrgency(text: string): "low" | "medium" | "high" | "critical" {
    const urgencyIndicators = {
      critical: [
        /\b(emergency|urgent|asap|immediately|critical|crisis|disaster|failure|down|broken|not working)\b/gi,
        /\b(deadline today|due today|overdue|expired|final notice)\b/gi,
        /[🚨🔥⚠️]/g
      ],
      high: [
        /\b(soon|quickly|priority|important|deadline|due date|time-sensitive|prompt)\b/gi,
        /\b(this week|tomorrow|by end of day|eod|before|until)\b/gi,
        /[❗⏰]/g
      ],
      medium: [
        /\b(when you can|at your convenience|next week|upcoming|planned|scheduled)\b/gi,
        /\b(reminder|follow up|checking in|status update)\b/gi
      ]
    };

    for (const [level, patterns] of Object.entries(urgencyIndicators)) {
      const score = patterns.reduce((sum, pattern) => {
        const matches = text.match(pattern);
        return sum + (matches ? matches.length : 0);
      }, 0);
      
      if (score > 0) {
        return level as "low" | "medium" | "high" | "critical";
      }
    }

    return "low";
  }

  private generateLabels(text: string): string[] {
    const labels: string[] = [];
    const categories = this.categorizeEmail(text);
    const intent = this.detectAdvancedIntent(text);
    const urgency = this.assessDetailedUrgency(text);

    // Add category-based labels
    labels.push(...categories);

    // Add intent-based labels
    if (intent !== "informational") {
      labels.push(intent.replace("_", " ").replace(/\b\w/g, l => l.toUpperCase()));
    }

    // Add urgency labels
    if (urgency !== "low") {
      labels.push(urgency.charAt(0).toUpperCase() + urgency.slice(1) + " Priority");
    }

    // Add content-based labels
    const lowerText = text.toLowerCase();
    if (lowerText.includes("attachment") || lowerText.includes("attached")) {
      labels.push("Has Attachment");
    }
    if (lowerText.includes("cc:") || lowerText.includes("bcc:")) {
      labels.push("Multiple Recipients");
    }
    if (lowerText.match(/\b\d{1,2}\/\d{1,2}\/\d{4}\b/)) {
      labels.push("Contains Date");
    }

    return [...new Set(labels)].slice(0, 6);
  }
}

export class AIEngine {
  private models: FreeLanguageModel[];
  private accuracyThreshold = 0.7;

  constructor() {
    this.models = [
      new LocalNLPModel(),
      new HuggingFaceModel()
    ];
  }

  async analyzeEmail(emailContent: string, subject: string): Promise<AIAnalysis & { validation: AccuracyValidation }> {
    const fullText = `${subject}\n\n${emailContent}`;
    
    // Run analysis with multiple models
    const analyses = await Promise.all(
      this.models.map(model => model.analyze(fullText))
    );

    // Ensemble the results
    const ensembledResult = this.ensembleResults(analyses);
    
    // Validate accuracy
    const validation = await this.validateAccuracy(ensembledResult, analyses);

    return {
      ...ensembledResult,
      validation
    };
  }

  private ensembleResults(analyses: Partial<AIAnalysis>[]): AIAnalysis {
    // Combine results from multiple models
    const validAnalyses = analyses.filter(a => a.confidence && a.confidence > 0.3);
    
    if (validAnalyses.length === 0) {
      return this.getDefaultAnalysis();
    }

    // Weighted voting based on confidence scores
    const weights = validAnalyses.map(a => a.confidence || 0.5);
    const totalWeight = weights.reduce((sum, w) => sum + w, 0);

    // Ensemble categories
    const categoryVotes: { [key: string]: number } = {};
    validAnalyses.forEach((analysis, i) => {
      analysis.categories?.forEach(category => {
        categoryVotes[category] = (categoryVotes[category] || 0) + weights[i];
      });
    });

    const topCategories = Object.entries(categoryVotes)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([category]) => category);

    // Ensemble sentiment
    const sentimentVotes: { [key: string]: number } = {};
    validAnalyses.forEach((analysis, i) => {
      if (analysis.sentiment) {
        sentimentVotes[analysis.sentiment] = (sentimentVotes[analysis.sentiment] || 0) + weights[i];
      }
    });
    const topSentiment = Object.entries(sentimentVotes)
      .sort(([,a], [,b]) => b - a)[0]?.[0] as "positive" | "negative" | "neutral" || "neutral";

    // Weighted average confidence
    const avgConfidence = weights.reduce((sum, weight, i) => {
      return sum + (validAnalyses[i].confidence || 0.5) * weight;
    }, 0) / totalWeight;

    // Combine other fields
    const allKeywords = validAnalyses.flatMap(a => a.keywords || []);
    const uniqueKeywords = [...new Set(allKeywords)].slice(0, 10);

    const allLabels = validAnalyses.flatMap(a => a.suggestedLabels || []);
    const uniqueLabels = [...new Set(allLabels)].slice(0, 8);

    return {
      topic: validAnalyses[0]?.topic || "General",
      sentiment: topSentiment,
      intent: validAnalyses[0]?.intent || "informational",
      urgency: validAnalyses[0]?.urgency || "low",
      confidence: Math.min(avgConfidence, 0.95),
      categories: topCategories.length > 0 ? topCategories : ["General"],
      keywords: uniqueKeywords,
      reasoning: `Ensemble analysis from ${validAnalyses.length} models with weighted voting`,
      suggestedLabels: uniqueLabels,
      riskFlags: this.detectRiskFlags(validAnalyses)
    };
  }

  private async validateAccuracy(result: AIAnalysis, analyses: Partial<AIAnalysis>[]): Promise<AccuracyValidation> {
    // Cross-validation between models
    const agreements = this.calculateAgreements(analyses);
    
    // Confidence-based validation
    const confidenceValid = result.confidence >= this.accuracyThreshold;
    
    // Ensemble consistency
    const ensembleScore = agreements / analyses.length;
    
    const overallScore = (result.confidence * 0.6) + (ensembleScore * 0.4);
    const reliable = overallScore >= this.accuracyThreshold && confidenceValid;

    return {
      validationMethod: "ensemble",
      score: overallScore,
      reliable,
      feedback: reliable 
        ? "High confidence analysis with model agreement"
        : "Low confidence - may need human review"
    };
  }

  private calculateAgreements(analyses: Partial<AIAnalysis>[]): number {
    if (analyses.length < 2) return 1;
    
    let agreements = 0;
    let totalComparisons = 0;

    // Compare categories
    for (let i = 0; i < analyses.length - 1; i++) {
      for (let j = i + 1; j < analyses.length; j++) {
        const cats1 = analyses[i].categories || [];
        const cats2 = analyses[j].categories || [];
        const intersection = cats1.filter(c => cats2.includes(c));
        if (intersection.length > 0) agreements++;
        totalComparisons++;
      }
    }

    return totalComparisons > 0 ? agreements / totalComparisons : 0;
  }

  private detectRiskFlags(analyses: Partial<AIAnalysis>[]): string[] {
    const flags: string[] = [];
    
    // Check for low confidence
    const avgConfidence = analyses.reduce((sum, a) => sum + (a.confidence || 0), 0) / analyses.length;
    if (avgConfidence < 0.5) {
      flags.push("low_confidence");
    }

    // Check for conflicting analyses
    const categories = analyses.flatMap(a => a.categories || []);
    const uniqueCategories = new Set(categories);
    if (uniqueCategories.size > categories.length * 0.7) {
      flags.push("conflicting_categorization");
    }

    // Check for urgent content
    const hasUrgent = analyses.some(a => a.urgency === "critical" || a.urgency === "high");
    if (hasUrgent) {
      flags.push("urgent_content");
    }

    return flags;
  }

  private getDefaultAnalysis(): AIAnalysis {
    return {
      topic: "General",
      sentiment: "neutral",
      intent: "informational",
      urgency: "low",
      confidence: 0.3,
      categories: ["General"],
      keywords: [],
      reasoning: "Default analysis - insufficient data for classification",
      suggestedLabels: ["Needs Review"],
      riskFlags: ["low_confidence"]
    };
  }

  // Public method to update accuracy threshold
  setAccuracyThreshold(threshold: number): void {
    this.accuracyThreshold = Math.max(0.1, Math.min(0.95, threshold));
  }

  // Method to get analysis statistics
  async getAnalysisStats(): Promise<{ modelsActive: number; averageConfidence: number; accuracyThreshold: number }> {
    return {
      modelsActive: this.models.length,
      averageConfidence: 0.75, // This would be calculated from historical data
      accuracyThreshold: this.accuracyThreshold
    };
  }
}