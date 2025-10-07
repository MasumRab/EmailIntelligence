import express, { type Application, type Request, type Response, type NextFunction } from 'express';
// Import the exported handlers
import {
    analyzeEmailHandler,
    categorizeEmailHandler,
    batchAnalyzeEmailsHandler,
    validateAIAnalysisHandler,
    getAIHealthHandler
} from './aiRoutes';
import { storage } from './storage';
import { pythonNLP } from './python-bridge';
import { type MappedNLPResult } from './python-bridge';
import { vi } from 'vitest'; // Import vi

// Mock dependencies
vi.mock('./storage', () => ({
  storage: {
    getEmailById: vi.fn(),
    updateEmail: vi.fn(),
    createActivity: vi.fn(),
    getAllCategories: vi.fn(), // Though this might not be used anymore post-refactor
    getCategoryById: vi.fn(),
  },
}));

vi.mock('./python-bridge', () => ({
  pythonNLP: {
    analyzeEmail: vi.fn(),
    testConnection: vi.fn(),
  },
}));

const createApp = (): Application => {
  const app = express();
  app.use(express.json());
  // app.use('/api/ai', aiRoutes); // Not needed if testing handlers directly
  return app;
};

describe('AI Route Handlers', () => { // Updated describe
  // let app: Application; // Not needed
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = vi.fn(); // Use vi.fn()

  const mockEmail = { id: 1, subject: 'Test Email', content: 'Test content' };
  const mockNLPAnalysisResult: MappedNLPResult = {
    topic: 'Work',
    sentiment: 'neutral',
    intent: 'informational',
    urgency: 'low',
    confidence: 0.9,
    categories: ['Work & Business'], // Raw categories from NLP
    keywords: ['test', 'email'],
    reasoning: 'Analyzed by mock',
    suggestedLabels: ['TestLabel'],
    riskFlags: [],
    categoryId: 5, // Assume Python now returns a categoryId
    validation: {
      validationMethod: 'confidence_threshold',
      score: 0.9,
      reliable: true,
      feedback: 'Mock validation',
    },
  };

  beforeEach(() => {
    // app = createApp(); // Not needed for direct handler testing
    mockRequest = {};
    mockResponse = {
      json: vi.fn().mockReturnThis(), // Use vi.fn()
      status: vi.fn().mockReturnThis(), // Use vi.fn()
    };
    // Clear mocks
    (storage.getEmailById as any).mockClear();
    (storage.updateEmail as any).mockClear();
    (storage.createActivity as any).mockClear();
    (storage.getAllCategories as any).mockClear();
    (storage.getCategoryById as any).mockClear();
    (pythonNLP.analyzeEmail as any).mockClear();
    (pythonNLP.testConnection as any).mockClear();
  });

  describe('analyzeEmailHandler', () => { // Updated describe
    it('should analyze email and return analysis', async () => {
      (pythonNLP.analyzeEmail as any).mockResolvedValue(mockNLPAnalysisResult);
      mockRequest = { body: { subject: 'Test', content: 'Content' } };

      await analyzeEmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(pythonNLP.analyzeEmail).toHaveBeenCalledWith('Test', 'Content');
      expect(mockResponse.json).toHaveBeenCalledWith(mockNLPAnalysisResult);
    });

    it('should return 400 if subject or content is missing', async () => {
      mockRequest = { body: { subject: 'Test' } }; // Missing content

      await analyzeEmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Subject and content are required' });
    });
  });

  describe('categorizeEmailHandler', () => { // Updated describe
    it('should auto-categorize an email using categoryId from AI and return success', async () => {
      (storage.getEmailById as any).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as any).mockResolvedValue(mockNLPAnalysisResult); // which includes categoryId: 5
      const updatedEmail = { ...mockEmail, categoryId: 5, confidence: 90 };
      (storage.updateEmail as any).mockResolvedValue(updatedEmail);
      (storage.getCategoryById as any).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });


      mockRequest = { body: { emailId: 1, autoAnalyze: true } };
      await categorizeEmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getEmailById).toHaveBeenCalledWith(1);
      expect(pythonNLP.analyzeEmail).toHaveBeenCalledWith(mockEmail.subject, mockEmail.content);
      expect(storage.updateEmail).toHaveBeenCalledWith(1, {
        categoryId: mockNLPAnalysisResult.categoryId,
        confidence: Math.round(mockNLPAnalysisResult.confidence * 100),
        labels: mockNLPAnalysisResult.suggestedLabels,
      });
      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({
        success: true,
        email: updatedEmail,
        categoryAssigned: 'Work'
      }));
    });

    it('should return success:false if AI does not provide categoryId', async () => {
        (storage.getEmailById as any).mockResolvedValue(mockEmail);
        const nlpResultWithoutCategoryId = { ...mockNLPAnalysisResult, categoryId: undefined };
        (pythonNLP.analyzeEmail as any).mockResolvedValue(nlpResultWithoutCategoryId);

        mockRequest = { body: { emailId: 1, autoAnalyze: true } };
        await categorizeEmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

        expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({
          success: false,
          message: "No matching category found or AI analysis did not provide a category ID."
        }));
      });

    it('should handle manual categorization', async () => {
      (storage.getEmailById as any).mockResolvedValue(mockEmail);
      const manualCategoryId = 2;
      const updatedEmail = { ...mockEmail, categoryId: manualCategoryId, confidence: 95 };
      (storage.updateEmail as any).mockResolvedValue(updatedEmail);

      mockRequest = { body: { emailId: 1, autoAnalyze: false, categoryId: manualCategoryId, confidence: 95 } };
      await categorizeEmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.updateEmail).toHaveBeenCalledWith(1, { categoryId: manualCategoryId, confidence: 95 });
      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true, email: updatedEmail });
    });
  });

  describe('batchAnalyzeEmailsHandler', () => { // Updated describe
    it('should batch analyze emails and use categoryId from AI', async () => {
      const emailIds = [1, 2];
      const email1 = { id: 1, subject: 'S1', content: 'C1' };
      const email2 = { id: 2, subject: 'S2', content: 'C2' };
      const nlpResult1: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: 5, categories: ["Work"] };
      const nlpResult2: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: undefined, categories: ["Personal"] }; // No categoryId for second

      (storage.getEmailById as any).mockImplementation(id => {
        if (id === 1) return Promise.resolve(email1);
        if (id === 2) return Promise.resolve(email2);
        return Promise.resolve(undefined);
      });
      (pythonNLP.analyzeEmail as any).mockImplementation((subject) => {
        if (subject === 'S1') return Promise.resolve(nlpResult1);
        if (subject === 'S2') return Promise.resolve(nlpResult2);
        return Promise.resolve(mockNLPAnalysisResult);
      });
      (storage.updateEmail as any).mockResolvedValue(email1); // Simulate update success
      (storage.getCategoryById as any).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });


      mockRequest = { body: { emailIds } };
      await batchAnalyzeEmailsHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(pythonNLP.analyzeEmail).toHaveBeenCalledTimes(2);
      expect(storage.updateEmail).toHaveBeenCalledTimes(1); // Only for email1 with categoryId
      expect(storage.updateEmail).toHaveBeenCalledWith(1, expect.objectContaining({ categoryId: 5 }));
      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({
        success: true,
        results: expect.arrayContaining([
          expect.objectContaining({ emailId: 1, success: true, category: 'Work' }),
          expect.objectContaining({ emailId: 2, success: false, reason: 'no_matching_category_id_from_ai' })
        ])
      }));
    });
  });

  describe('validateAIAnalysisHandler', () => { // Updated describe
    it('should validate AI analysis and return success', async () => {
      (storage.getEmailById as any).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as any).mockResolvedValue(mockNLPAnalysisResult);

      mockRequest = { body: { emailId: 1, userFeedback: 'correct' } };
      await validateAIAnalysisHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ success: true }));
    });
  });

  describe('getAIHealthHandler', () => { // Updated describe
    it('should return health status from pythonNLP.testConnection', async () => {
      (pythonNLP.testConnection as any).mockResolvedValue(true);
      mockRequest = { method: 'GET' }; // method is not strictly needed for direct handler call if not used by handler

      await getAIHealthHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(pythonNLP.testConnection).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ status: 'healthy' }));
    });
  });
});
