import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import aiRoutes from './aiRoutes';
import { storage } from './storage';
import { pythonNLP } from './python-bridge';
import { type MappedNLPResult } from './python-bridge';

// Mock dependencies
vi.mock('./storage', () => ({
  storage: {
    getEmailById: vi.fn(),
    updateEmail: vi.fn(),
    createActivity: vi.fn(),
    getAllCategories: vi.fn(),
    getCategoryById: vi.fn(),
  },
}));

vi.mock('./python-bridge', () => ({
  pythonNLP: {
    analyzeEmail: vi.fn(),
    testConnection: vi.fn(),
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/ai', aiRoutes);

describe('AI Routes', () => {
  const mockEmail = { id: 1, subject: 'Test Email', content: 'Test content' };
  const mockNLPAnalysisResult: MappedNLPResult = {
    topic: 'Work',
    sentiment: 'neutral',
    intent: 'informational',
    urgency: 'low',
    confidence: 0.9,
    categories: ['Work & Business'],
    keywords: ['test', 'email'],
    reasoning: 'Analyzed by mock',
    suggestedLabels: ['TestLabel'],
    riskFlags: [],
    categoryId: 5,
    validation: {
      validationMethod: 'confidence_threshold',
      score: 0.9,
      reliable: true,
      feedback: 'Mock validation',
    },
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('POST /api/ai/analyze', () => {
    it('should analyze email and return analysis', async () => {
      (pythonNLP.analyzeEmail as ReturnType<typeof vi.fn>).mockResolvedValue(mockNLPAnalysisResult);

      const response = await request(app)
        .post('/api/ai/analyze')
        .send({ subject: 'Test', content: 'Content' });

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockNLPAnalysisResult);
      expect(pythonNLP.analyzeEmail).toHaveBeenCalledWith('Test', 'Content');
    });

    it('should return 400 if subject or content is missing', async () => {
      const response = await request(app)
        .post('/api/ai/analyze')
        .send({ subject: 'Test' });

      expect(response.status).toBe(400);
      expect(response.body).toEqual({ message: 'Subject and content are required' });
    });
  });

  describe('POST /api/ai/categorize', () => {
    it('should auto-categorize an email using categoryId from AI and return success', async () => {
      (storage.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as ReturnType<typeof vi.fn>).mockResolvedValue(mockNLPAnalysisResult);
      const updatedEmail = { ...mockEmail, categoryId: 5, confidence: 90 };
      (storage.updateEmail as ReturnType<typeof vi.fn>).mockResolvedValue(updatedEmail);
      (storage.getCategoryById as ReturnType<typeof vi.fn>).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });

      const response = await request(app)
        .post('/api/ai/categorize')
        .send({ emailId: 1, autoAnalyze: true });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.email).toEqual(updatedEmail);
      expect(response.body.categoryAssigned).toBe('Work');
    });

    it('should return success:false if AI does not provide categoryId', async () => {
      (storage.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmail);
      const nlpResultWithoutCategoryId = { ...mockNLPAnalysisResult, categoryId: undefined };
      (pythonNLP.analyzeEmail as ReturnType<typeof vi.fn>).mockResolvedValue(nlpResultWithoutCategoryId);

      const response = await request(app)
        .post('/api/ai/categorize')
        .send({ emailId: 1, autoAnalyze: true });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(false);
    });

    it('should handle manual categorization', async () => {
      (storage.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmail);
      const manualCategoryId = 2;
      const updatedEmail = { ...mockEmail, categoryId: manualCategoryId, confidence: 95 };
      (storage.updateEmail as ReturnType<typeof vi.fn>).mockResolvedValue(updatedEmail);

      const response = await request(app)
        .post('/api/ai/categorize')
        .send({ emailId: 1, autoAnalyze: false, categoryId: manualCategoryId, confidence: 95 });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.email).toEqual(updatedEmail);
    });
  });

  describe('POST /api/ai/batch-analyze', () => {
    it('should batch analyze emails and use categoryId from AI', async () => {
      const emailIds = [1, 2];
      const email1 = { id: 1, subject: 'S1', content: 'C1' };
      const email2 = { id: 2, subject: 'S2', content: 'C2' };
      const nlpResult1: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: 5, categories: ["Work"] };
      const nlpResult2: MappedNLPResult = { ...mockNLPAnalysisResult, categoryId: undefined, categories: ["Personal"] };

      (storage.getEmailById as ReturnType<typeof vi.fn>).mockImplementation(id => {
        if (id === 1) return Promise.resolve(email1);
        if (id === 2) return Promise.resolve(email2);
        return Promise.resolve(undefined);
      });
      (pythonNLP.analyzeEmail as ReturnType<typeof vi.fn>).mockImplementation((subject) => {
        if (subject === 'S1') return Promise.resolve(nlpResult1);
        if (subject === 'S2') return Promise.resolve(nlpResult2);
        return Promise.resolve(mockNLPAnalysisResult);
      });
      (storage.updateEmail as ReturnType<typeof vi.fn>).mockResolvedValue(email1);
      (storage.getCategoryById as ReturnType<typeof vi.fn>).mockResolvedValue({ id: 5, name: 'Work', description: '', color: '', count: 1 });

      const response = await request(app)
        .post('/api/ai/batch-analyze')
        .send({ emailIds });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
      expect(response.body.results).toHaveLength(2);
      expect(response.body.results[0].success).toBe(true);
      expect(response.body.results[1].success).toBe(false);
    });
  });

  describe('POST /api/ai/validate', () => {
    it('should validate AI analysis and return success', async () => {
      (storage.getEmailById as ReturnType<typeof vi.fn>).mockResolvedValue(mockEmail);
      (pythonNLP.analyzeEmail as ReturnType<typeof vi.fn>).mockResolvedValue(mockNLPAnalysisResult);

      const response = await request(app)
        .post('/api/ai/validate')
        .send({ emailId: 1, userFeedback: 'correct' });

      expect(response.status).toBe(200);
      expect(response.body.success).toBe(true);
    });
  });

  describe('GET /api/ai/health', () => {
    it('should return health status from pythonNLP.testConnection', async () => {
      (pythonNLP.testConnection as ReturnType<typeof vi.fn>).mockResolvedValue(true);

      const response = await request(app).get('/api/ai/health');

      expect(response.status).toBe(200);
      expect(response.body.status).toBe('healthy');
    });
  });
});
