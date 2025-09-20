import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import gmailRoutes from './gmailRoutes';
import { gmailAIService } from './gmail-ai-service';

vi.mock('./gmail-ai-service', () => ({
  gmailAIService: {
    syncGmailEmails: vi.fn(),
    executeSmartRetrieval: vi.fn(),
    getRetrievalStrategies: vi.fn(),
    syncInboxEmails: vi.fn(),
    syncImportantEmails: vi.fn(),
    syncWeeklyBatch: vi.fn(),
    trainModelsFromGmail: vi.fn(),
    applyAdaptiveOptimization: vi.fn(),
    getPerformanceMetrics: vi.fn(),
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/gmail', gmailRoutes);

describe('Gmail Routes', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('POST /api/gmail/sync', () => {
    it('should call gmailAIService.syncGmailEmails and return result', async () => {
      const mockSyncResult = { success: true, processedCount: 10 };
      (gmailAIService.syncGmailEmails as ReturnType<typeof vi.fn>).mockResolvedValue(mockSyncResult);

      const response = await request(app)
        .post('/api/gmail/sync')
        .send({ maxEmails: 100 });

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockSyncResult);
    });

    it('should return 500 if syncGmailEmails fails', async () => {
      (gmailAIService.syncGmailEmails as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('Sync Error'));

      const response = await request(app).post('/api/gmail/sync').send({});

      expect(response.status).toBe(500);
      expect(response.body).toHaveProperty('success', false);
    });
  });

  describe('POST /api/gmail/smart-retrieval', () => {
    it('should call gmailAIService.executeSmartRetrieval and return result', async () => {
      const mockRetrievalResult = { success: true, processedCount: 5 };
      (gmailAIService.executeSmartRetrieval as ReturnType<typeof vi.fn>).mockResolvedValue(mockRetrievalResult);

      const response = await request(app)
        .post('/api/gmail/smart-retrieval')
        .send({ strategies: ['test'] });

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockRetrievalResult);
    });
  });

  describe('GET /api/gmail/strategies', () => {
    it('should call gmailAIService.getRetrievalStrategies and return strategies', async () => {
      const mockStrategies = [{ name: 'strategy1' }];
      (gmailAIService.getRetrievalStrategies as ReturnType<typeof vi.fn>).mockResolvedValue(mockStrategies);

      const response = await request(app).get('/api/gmail/strategies');

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ strategies: mockStrategies });
    });
  });

  describe('POST /api/gmail/sync-inbox', () => {
    it('should call gmailAIService.syncInboxEmails', async () => {
      (gmailAIService.syncInboxEmails as ReturnType<typeof vi.fn>).mockResolvedValue({ success: true });

      const response = await request(app)
        .post('/api/gmail/sync-inbox')
        .send({ maxEmails: 50 });

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ success: true });
    });
  });

  describe('POST /api/gmail/train-models', () => {
    it('should call gmailAIService.trainModelsFromGmail', async () => {
      (gmailAIService.trainModelsFromGmail as ReturnType<typeof vi.fn>).mockResolvedValue({ success: true });

      const response = await request(app)
        .post('/api/gmail/train-models')
        .send({ trainingQuery: "test" });

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ success: true });
    });
  });

  describe('POST /api/gmail/optimize', () => {
    it('should call gmailAIService.applyAdaptiveOptimization if strategyName is provided', async () => {
      (gmailAIService.applyAdaptiveOptimization as ReturnType<typeof vi.fn>).mockResolvedValue({ success: true });

      const response = await request(app)
        .post('/api/gmail/optimize')
        .send({ strategyName: "test_strat" });

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ success: true });
    });

    it('should return 400 if strategyName is missing', async () => {
      const response = await request(app).post('/api/gmail/optimize').send({});
      expect(response.status).toBe(400);
    });
  });

  describe('GET /api/gmail/quota-status', () => {
    it('should get quota status from performance metrics', async () => {
      const mockQuotaStatus = { dailyUsage: { percentage: 50 } };
      (gmailAIService.getPerformanceMetrics as ReturnType<typeof vi.fn>).mockResolvedValue({ quotaStatus: mockQuotaStatus });

      const response = await request(app).get('/api/gmail/quota-status');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockQuotaStatus);
    });
  });

  describe('GET /api/gmail/alerts', () => {
    it('should get alerts from performance metrics', async () => {
      const mockAlerts = [{ type: 'quota', message: 'High usage' }];
      (gmailAIService.getPerformanceMetrics as ReturnType<typeof vi.fn>).mockResolvedValue({ alerts: mockAlerts });

      const response = await request(app).get('/api/gmail/alerts');

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ alerts: mockAlerts, count: mockAlerts.length });
    });
  });

  describe('GET /api/gmail/recommendations', () => {
    it('should get recommendations from performance metrics', async () => {
      const mockRecs = [{ type: 'efficiency', recommendation: 'Adjust strategy' }];
      (gmailAIService.getPerformanceMetrics as ReturnType<typeof vi.fn>).mockResolvedValue({ recommendations: mockRecs });

      const response = await request(app).get('/api/gmail/recommendations');

      expect(response.status).toBe(200);
      expect(response.body).toEqual({ recommendations: mockRecs, count: mockRecs.length });
    });
  });
});
