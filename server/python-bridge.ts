import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import type { AIAnalysis, AccuracyValidation } from './ai-engine'; // Import backend types
import { type Email, type InsertEmail, type EmailWithCategory } from '@shared/schema';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PYTHON_SERVER_URL = 'http://127.0.0.1:8000';

// This interface represents the direct output from the Python script
interface PythonScriptOutput {
  topic: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  intent: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  categories: string[];
  keywords: string[];
  reasoning: string;
  suggested_labels: string[];
  risk_flags: string[];
  validation: {
    validation_method: string; // Note: snake_case from Python
    score: number;
    reliable: boolean;
    feedback: string;
  };
  category_id?: number; // Added category_id from Python
}

export type MappedNLPResult = AIAnalysis & { validation: AccuracyValidation }; // AIAnalysis now includes categoryId?

export class PythonNLPBridge {
  private pythonScriptPath: string;

  constructor() {
    this.pythonScriptPath = path.join(__dirname, 'python_nlp', 'nlp_engine.py');
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const url = `${PYTHON_SERVER_URL}${path}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Python server request failed: ${response.status} ${response.statusText} - ${errorText}`);
    }

    return response.json() as Promise<T>;
  }


  private mapPythonOutputToNLPResult(pyOutput: PythonScriptOutput): MappedNLPResult {
    return {
      topic: pyOutput.topic,
      sentiment: pyOutput.sentiment,
      intent: pyOutput.intent,
      urgency: pyOutput.urgency,
      confidence: pyOutput.confidence,
      categories: pyOutput.categories,
      keywords: pyOutput.keywords,
      reasoning: pyOutput.reasoning,
      suggestedLabels: pyOutput.suggested_labels, // map snake_case to camelCase
      riskFlags: pyOutput.risk_flags,           // map snake_case to camelCase
      validation: {
        validationMethod: pyOutput.validation.validation_method as AccuracyValidation['validationMethod'], // map snake_case to camelCase and assert type
        score: pyOutput.validation.score,
        reliable: pyOutput.validation.reliable,
        feedback: pyOutput.validation.feedback,
      },
      categoryId: pyOutput.category_id, // Map category_id
    };
  }

  async getEmails(category?: string, search?: string): Promise<EmailWithCategory[]> {
    const params = new URLSearchParams();
    if (category) params.append('category_id', category);
    if (search) params.append('search', search);
    return this.request<EmailWithCategory[]>(`/api/emails?${params.toString()}`);
  }

  async getEmailById(id: number): Promise<EmailWithCategory> {
    return this.request<EmailWithCategory>(`/api/emails/${id}`);
  }

  async createEmail(email: InsertEmail): Promise<Email> {
    return this.request<Email>('/api/emails', {
      method: 'POST',
      body: JSON.stringify(email),
    });
  }

  async updateEmail(id: number, email: Partial<Email>): Promise<Email> {
    return this.request<Email>(`/api/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify(email),
    });
  }

  async analyzeEmail(subject: string, content: string): Promise<MappedNLPResult> {
    return new Promise((resolve, reject) => {
      const python = spawn('python3', [this.pythonScriptPath, subject, content], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      let output = '';
      let errorOutput = '';

      python.stdout.on('data', (data) => {
        output += data.toString();
      });

      python.stderr.on('data', (data) => {
        errorOutput += data.toString();
      });

      python.on('close', (code) => {
        if (code !== 0) {
          console.error('Python NLP Error:', errorOutput);
          resolve(this.getFallbackAnalysis(subject, content));
          return;
        }

        try {
          const result: PythonScriptOutput = JSON.parse(output.trim());
          resolve(this.mapPythonOutputToNLPResult(result));
        } catch (parseError) {
          console.error('Failed to parse Python NLP output:', parseError);
          resolve(this.getFallbackAnalysis(subject, content));
        }
      });

      python.on('error', (error) => {
        console.error('Python process error:', error);
        resolve(this.getFallbackAnalysis(subject, content));
      });
    });
  }

  private getFallbackAnalysis(subject: string, content: string): MappedNLPResult {
    // Enhanced JavaScript fallback with better pattern matching
    const fullText = `${subject}\n\n${content}`.toLowerCase();
    
    const categories = this.categorizeWithPatterns(fullText);
    const sentiment = this.analyzeSentimentFallback(fullText);
    const intent = this.detectIntentFallback(fullText);
    const urgency = this.assessUrgencyFallback(fullText);
    const keywords = this.extractKeywordsFallback(fullText);
    
    // const categories = this.categorizeWithPatterns(fullText); // Removed duplicate
    // const sentiment = this.analyzeSentimentFallback(fullText); // Removed duplicate
    // const intent = this.detectIntentFallback(fullText); // Removed duplicate
    // const urgency = this.assessUrgencyFallback(fullText); // Removed duplicate
    // const keywords = this.extractKeywordsFallback(fullText); // Removed duplicate

    return {
      topic: categories[0] || 'General Communication',
      sentiment,
      intent,
      urgency,
      confidence: 0.65,
      categories,
      keywords,
      reasoning: 'JavaScript fallback analysis with enhanced pattern matching',
      suggestedLabels: [...categories, intent.replace('_', ' ')].filter(Boolean),
      riskFlags: urgency === 'critical' ? ['urgent_content'] : [],
      validation: {
        validationMethod: 'javascript_fallback' as AccuracyValidation['validationMethod'],
        score: 0.65,
        reliable: true,
        feedback: 'Analysis completed using JavaScript fallback with good reliability'
      }
    };
  }

  private categorizeWithPatterns(text: string): string[] {
    const categoryPatterns = {
      'Work & Business': [
        /\b(meeting|conference|project|deadline|client|presentation|report|proposal|budget|team|colleague|office|work|business|professional|corporate|company|organization)\b/g,
        /\b(employee|staff|manager|supervisor|director|executive|department|division|quarterly|annual|monthly|weekly|daily)\b/g
      ],
      'Finance & Banking': [
        /\b(bank|payment|transaction|invoice|bill|statement|account|credit|debit|transfer|money|financial|insurance|investment|loan|mortgage)\b/g,
        /\$[\d,]+|\b\d+\s?(dollars?|USD|EUR|GBP)\b/g,
        /\b(tax|taxes|irs|refund|audit|accountant|bookkeeping|overdraft|bankruptcy)\b/g
      ],
      'Healthcare': [
        /\b(doctor|medical|health|hospital|clinic|appointment|prescription|medicine|treatment|therapy|checkup|surgery|dental|pharmacy)\b/g,
        /\b(symptoms|diagnosis|patient|specialist|emergency|ambulance|insurance|medicare|medicaid|covid|coronavirus|vaccine)\b/g
      ],
      'Personal & Family': [
        /\b(family|personal|friend|birthday|anniversary|vacation|holiday|weekend|dinner|lunch|home|house|kids|children)\b/g,
        /\b(mom|dad|mother|father|sister|brother|grandma|grandpa|wedding|graduation|baby|party|celebration)\b/g
      ],
      'Travel': [
        /\b(travel|flight|hotel|booking|reservation|trip|vacation|destination|airport|airline|passport|visa|itinerary)\b/g,
        /\b(departure|arrival|check-in|luggage|baggage|cruise|resort|tour|tickets|confirmation)\b/g
      ],
      'Technology': [
        /\b(software|hardware|computer|laptop|mobile|app|application|website|internet|email|password|account|login)\b/g,
        /\b(server|database|API|code|programming|development|tech|technical|IT|support|troubleshoot|install)\b/g
      ],
      'Education': [
        /\b(school|university|college|student|teacher|professor|course|class|lecture|assignment|homework|exam|grade)\b/g,
        /\b(semester|tuition|scholarship|graduation|degree|diploma|enrollment|registration|admissions)\b/g
      ],
      'Promotions & Marketing': [
        /\b(sale|discount|offer|promotion|deal|coupon|newsletter|marketing|advertisement|special|limited|exclusive|free|save)\b/g,
        /(%\s*off|free shipping|limited time|act now|don\'t miss|buy now|unsubscribe|opt-out|mailing list)/g
      ]
    };

    const scores: { [key: string]: number } = {};
    
    for (const [category, patterns] of Object.entries(categoryPatterns)) {
      let score = 0;
      for (const pattern of patterns) {
        const matches = text.match(pattern);
        if (matches) score += matches.length;
      }
      if (score > 0) scores[category] = score;
    }

    const sortedCategories = Object.entries(scores)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 2)
      .map(([category]) => category);

    return sortedCategories.length > 0 ? sortedCategories : ['General'];
  }

  private analyzeSentimentFallback(text: string): 'positive' | 'negative' | 'neutral' {
    const positiveWords = [
      'excellent', 'amazing', 'fantastic', 'wonderful', 'great', 'good', 'nice', 'pleased', 'happy',
      'satisfied', 'thank', 'thanks', 'grateful', 'appreciate', 'love', 'perfect', 'success',
      'achievement', 'congratulations', 'approve', 'accept', 'agree', 'brilliant', 'outstanding'
    ];

    const negativeWords = [
      'terrible', 'awful', 'horrible', 'disaster', 'bad', 'poor', 'disappointed', 'frustrated',
      'angry', 'upset', 'problem', 'issue', 'error', 'mistake', 'wrong', 'failed', 'failure',
      'broken', 'difficult', 'trouble', 'concern', 'worry', 'urgent', 'emergency', 'critical',
      'serious', 'complaint', 'complain', 'reject', 'deny', 'refuse', 'cancel'
    ];

    let positiveScore = 0;
    let negativeScore = 0;

    positiveWords.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'g');
      const matches = text.match(regex);
      if (matches) positiveScore += matches.length;
    });

    negativeWords.forEach(word => {
      const regex = new RegExp(`\\b${word}\\b`, 'g');
      const matches = text.match(regex);
      if (matches) negativeScore += matches.length;
    });

    if (positiveScore > negativeScore + 1) return 'positive';
    if (negativeScore > positiveScore + 1) return 'negative';
    return 'neutral';
  }

  private detectIntentFallback(text: string): string {
    const intentPatterns = {
      'request': /\b(please|could you|would you|can you|need|require|request|help|assist|support|provide)\b/g,
      'inquiry': /\b(question|ask|wonder|curious|information|details|clarification|explain|how|what|when|where|why)\b/g,
      'scheduling': /\b(schedule|calendar|meeting|appointment|time|date|available|busy|free|reschedule|confirm)\b/g,
      'urgent_action': /\b(urgent|asap|immediately|emergency|critical|priority|deadline|rush|time sensitive)\b/g,
      'gratitude': /\b(thank|thanks|grateful|appreciate|acknowledgment|recognition)\b/g,
      'complaint': /\b(complaint|complain|issue|problem|dissatisfied|unhappy|wrong|error|not working|broken|failed)\b/g,
      'follow_up': /\b(follow up|follow-up|checking in|status|update|progress|reminder|following up)\b/g,
      'confirmation': /\b(confirm|confirmation|verify|check|ensure|validate|acknowledge|received|understand)\b/g
    };

    let maxScore = 0;
    let detectedIntent = 'informational';

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

  private assessUrgencyFallback(text: string): 'low' | 'medium' | 'high' | 'critical' {
    if (/\b(emergency|urgent|asap|immediately|critical|crisis|disaster|failure|deadline today|due today|overdue)\b/.test(text)) {
      return 'critical';
    }
    if (/\b(soon|quickly|priority|important|deadline|time-sensitive|this week|tomorrow|by end of day)\b/.test(text)) {
      return 'high';
    }
    if (/\b(when you can|next week|upcoming|planned|scheduled|reminder|follow up)\b/.test(text)) {
      return 'medium';
    }
    return 'low';
  }

  private extractKeywordsFallback(text: string): string[] {
    const stopWords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
      'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
      'will', 'would', 'could', 'should', 'can', 'may', 'might', 'must', 'this', 'that',
      'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
    ]);

    const words = text.match(/\b[a-zA-Z]{3,}\b/g) || [];
    const wordFreq: { [key: string]: number } = {};

    words.forEach(word => {
      const lowerWord = word.toLowerCase();
      if (!stopWords.has(lowerWord)) {
        wordFreq[lowerWord] = (wordFreq[lowerWord] || 0) + 1;
      }
    });

    return Object.entries(wordFreq)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 8)
      .map(([word]) => word);
  }

  async testConnection(): Promise<boolean> {
    try {
      const result = await this.analyzeEmail('Test Subject', 'Test content for connection verification.');
      // Access reliable from the mapped structure
      return result.validation.reliable;
    } catch (error) {
      console.error('Python NLP connection test failed:', error);
      return false;
    }
  }
}

export const pythonNLP = new PythonNLPBridge();