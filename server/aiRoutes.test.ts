import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import aiRoutes from './aiRoutes';
import { storage } from './storage';
import { pythonNLP } from './python-bridge';
import { type MappedNLPResult } from './python-bridge';

// Mock dependencies
jest.mock('./storage', () => ({
  storage: {
    getEmailById: jest.fn(),
    updateEmail: jest.fn(),
    createActivity: jest.fn(),
    getAllCategories: jest.fn(), // Though this might not be used anymore post-refactor
    getCategoryById: jest.fn(),
  },
}));

jest.mock('./python-bridge', () => ({
  pythonNLP: {
    analyzeEmail: jest.fn(),
    testConnection: jest.fn(),
  },
}));

const createApp = (): Application => {
  const app = express();
  app.use(express.json());
  app.use('/api/ai', aiRoutes);
  return app;
};

describe('AI Routes', () => {
  let app: Application;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = jest.fn();

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
    app = createApp();
    mockRequest = {};
    mockResponse = {
      json: jest.fn().mockReturnThis(),
      status: jest.fn().mockReturnThis(),
    };
    // Clear mocks
    (storage.getEmailById as jest.Mock).mockClear();
    (storage.updateEmail as jest.Mock).mockClear();
    (storage.createActivity as jest.Mock).mockClear();
    (storage.getAllCategories as jest.Mock).mockClear();
    (storage.getCategoryById as jest.Mock).mockClear();
    (pythonNLP.analyzeEmail as jest.Mock).mockClear();
    (pythonNLP.testConnection as jest.Mock).mockClear();
  });

  describe('POST /api/ai/analyze', () => {
    it('should analyze email and return analysis', async () => {
      (pythonNLP.analyzeEmail as jest.Mock).mockResolvedValue(mockNLPAnalysisResult);
      mockRequest = { body: { subject: 'Test', content: 'Content' } , method: 'POST'};

      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(pythonNLP.analyzeEmail).toHaveBeenCalledWith('Test', 'Content');
      expect(mockResponse.json).toHaveBeenCalledWith(mockNLPAnalysisResult);
    });

    it('should return 400 if subject or content is missing', async () => {
      mockRequest = { body: { subject: 'Test' }, method: 'POST' }; // Missing content

      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Subject and content are required' });
    });
  });

  describe('POST /api/ai/categorize', () => {
    it('should auto-categorize an email using categoryId from AI and return success', async () => {
      (storage.getEmailById as jest.Mock).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as jest.Mock).mockResolvedValue(mockNLPAnalysisResult); // which includes categoryId: 5
      const updatedEmail = { ...mockEmail, categoryId: 5, confidence: 90 };
      (storage.updateEmail as jest.Mock).mockResolvedValue(updatedEmail);
      (storage.getCategoryById as jest.Mock).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });


      mockRequest = { body: { emailId: 1, autoAnalyze: true }, method: 'POST' };
      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

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
        (storage.getEmailById as jest.Mock).mockResolvedValue(mockEmail);
        const nlpResultWithoutCategoryId = { ...mockNLPAnalysisResult, categoryId: undefined };
        (pythonNLP.analyzeEmail as jest.Mock).mockResolvedValue(nlpResultWithoutCategoryId);

        mockRequest = { body: { emailId: 1, autoAnalyze: true }, method: 'POST' };
        await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

        expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({
          success: false,
          message: "No matching category found or AI analysis did not provide a category ID."
        }));
      });

    it('should handle manual categorization', async () => {
      (storage.getEmailById as jest.Mock).mockResolvedValue(mockEmail);
      const manualCategoryId = 2;
      const updatedEmail = { ...mockEmail, categoryId: manualCategoryId, confidence: 95 };
      (storage.updateEmail as jest.Mock).mockResolvedValue(updatedEmail);

      mockRequest = { body: { emailId: 1, autoAnalyze: false, categoryId: manualCategoryId, confidence: 95 }, method: 'POST' };
      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.updateEmail).toHaveBeenCalledWith(1, { categoryId: manualCategoryId, confidence: 95 });
      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true, email: updatedEmail });
    });
  });

  describe('POST /api/ai/batch-analyze', () => {
    it('should batch analyze emails and use categoryId from AI', async () => {
      const emailIds = [1, 2];
      const email1 = { id: 1, subject: 'S1', content: 'C1' };
      const email2 = { id: 2, subject: 'S2', content: 'C2' };
      const nlpResult1: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: 5, categories: ["Work"] };
      const nlpResult2: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: undefined, categories: ["Personal"] }; // No categoryId for second

      (storage.getEmailById as jest.Mock).mockImplementation(id => {
        if (id === 1) return Promise.resolve(email1);
        if (id === 2) return Promise.resolve(email2);
        return Promise.resolve(undefined);
      });
      (pythonNLP.analyzeEmail as jest.Mock).mockImplementation((subject) => {
        if (subject === 'S1') return Promise.resolve(nlpResult1);
        if (subject === 'S2') return Promise.resolve(nlpResult2);
        return Promise.resolve(mockNLPAnalysisResult);
      });
      (storage.updateEmail as jest.Mock).mockResolvedValue(email1); // Simulate update success
      (storage.getCategoryById as jest.Mock).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });


      mockRequest = { body: { emailIds }, method: 'POST' };
      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

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

  describe('POST /api/ai/validate', () => {
    it('should validate AI analysis and return success', async () => {
      (storage.getEmailById as jest.Mock).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as jest.Mock).mockResolvedValue(mockNLPAnalysisResult);

      mockRequest = { body: { emailId: 1, userFeedback: 'correct' }, method: 'POST' };
      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.createActivity).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ success: true }));
    });
  });

  describe('GET /api/ai/health', () => {
    it('should return health status from pythonNLP.testConnection', async () => {
      (pythonNLP.testConnection as jest.Mock).mockResolvedValue(true);
      mockRequest = { method: 'GET' };

      await aiRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(pythonNLP.testConnection).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ status: 'healthy' }));
    });
  });
});
[end of server/aiRoutes.test.ts]
