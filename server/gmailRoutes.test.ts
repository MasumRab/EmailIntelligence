import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import gmailRoutes from './gmailRoutes';
import { gmailAIService } from './gmail-ai-service'; // To mock its methods

// Mock the gmailAIService module
jest.mock('./gmail-ai-service', () => ({
  gmailAIService: {
    syncGmailEmails: jest.fn(),
    executeSmartRetrieval: jest.fn(),
    getRetrievalStrategies: jest.fn(),
    syncInboxEmails: jest.fn(),
    syncImportantEmails: jest.fn(),
    syncWeeklyBatch: jest.fn(),
    trainModelsFromGmail: jest.fn(),
    applyAdaptiveOptimization: jest.fn(),
    getPerformanceMetrics: jest.fn(), // For quota-status, alerts, recommendations
  },
}));

const createApp = (): Application => {
  const app = express();
  app.use(express.json());
  app.use('/api/gmail', gmailRoutes);
  return app;
};

describe('Gmail Routes', () => {
  let app: Application;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = jest.fn();

  beforeEach(() => {
    app = createApp();
    mockRequest = {};
    mockResponse = {
      json: jest.fn().mockReturnThis(),
      status: jest.fn().mockReturnThis(),
    };
    // Reset mocks for gmailAIService methods
    Object.values(gmailAIService).forEach(mockFn => {
        if (jest.isMockFunction(mockFn)) {
            mockFn.mockClear();
        }
    });
  });

  describe('POST /api/gmail/sync', () => {
    it('should call gmailAIService.syncGmailEmails and return result', async () => {
      const mockSyncResult = { success: true, processedCount: 10 };
      (gmailAIService.syncGmailEmails as jest.Mock).mockResolvedValue(mockSyncResult);
      mockRequest = { body: { maxEmails: 100 }, method: 'POST' };

      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.syncGmailEmails).toHaveBeenCalledWith(expect.objectContaining({ maxEmails: 100 }));
      expect(mockResponse.json).toHaveBeenCalledWith(mockSyncResult);
    });

    it('should return 500 if syncGmailEmails fails', async () => {
      (gmailAIService.syncGmailEmails as jest.Mock).mockRejectedValue(new Error('Sync Error'));
      mockRequest = { body: {}, method: 'POST' };

      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ success: false }));
    });
  });

  describe('POST /api/gmail/smart-retrieval', () => {
    it('should call gmailAIService.executeSmartRetrieval and return result', async () => {
      const mockRetrievalResult = { success: true, processedCount: 5 };
      (gmailAIService.executeSmartRetrieval as jest.Mock).mockResolvedValue(mockRetrievalResult);
      mockRequest = { body: { strategies: ['test'] }, method: 'POST' };

      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.executeSmartRetrieval).toHaveBeenCalledWith(['test'], 100, 30); // Default values
      expect(mockResponse.json).toHaveBeenCalledWith(mockRetrievalResult);
    });
  });

  describe('GET /api/gmail/strategies', () => {
    it('should call gmailAIService.getRetrievalStrategies and return strategies', async () => {
      const mockStrategies = [{ name: 'strategy1' }];
      (gmailAIService.getRetrievalStrategies as jest.Mock).mockResolvedValue(mockStrategies);
      mockRequest = { method: 'GET' };

      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.getRetrievalStrategies).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ strategies: mockStrategies });
    });
  });

  // Simplified tests for other sync endpoints - they all follow a similar pattern
  describe('POST /api/gmail/sync-inbox', () => {
    it('should call gmailAIService.syncInboxEmails', async () => {
      (gmailAIService.syncInboxEmails as jest.Mock).mockResolvedValue({ success: true });
      mockRequest = { body: { maxEmails: 50 }, method: 'POST' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.syncInboxEmails).toHaveBeenCalledWith(50);
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });
  });

  describe('POST /api/gmail/train-models', () => {
    it('should call gmailAIService.trainModelsFromGmail', async () => {
      (gmailAIService.trainModelsFromGmail as jest.Mock).mockResolvedValue({ success: true });
      mockRequest = { body: { trainingQuery: "test" }, method: 'POST' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.trainModelsFromGmail).toHaveBeenCalledWith("test", 5000); // Default maxTrainingEmails
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });
  });

  describe('POST /api/gmail/optimize', () => {
    it('should call gmailAIService.applyAdaptiveOptimization if strategyName is provided', async () => {
      (gmailAIService.applyAdaptiveOptimization as jest.Mock).mockResolvedValue({ success: true });
      mockRequest = { body: { strategyName: "test_strat" }, method: 'POST' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.applyAdaptiveOptimization).toHaveBeenCalledWith("test_strat");
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });

    it('should return 400 if strategyName is missing', async () => {
        mockRequest = { body: {}, method: 'POST' }; // strategyName is missing
        await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
        expect(mockResponse.status).toHaveBeenCalledWith(400);
        expect(mockResponse.json).toHaveBeenCalledWith({ success: false, error: "Strategy name is required" });
      });
  });

  describe('GET /api/gmail/quota-status', () => {
    it('should get quota status from performance metrics', async () => {
      const mockQuotaStatus = { dailyUsage: { percentage: 50 } };
      (gmailAIService.getPerformanceMetrics as jest.Mock).mockResolvedValue({ quotaStatus: mockQuotaStatus });
      mockRequest = { method: 'GET' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(mockQuotaStatus);
    });
  });

  describe('GET /api/gmail/alerts', () => {
    it('should get alerts from performance metrics', async () => {
      const mockAlerts = [{ type: 'quota', message: 'High usage' }];
      (gmailAIService.getPerformanceMetrics as jest.Mock).mockResolvedValue({ alerts: mockAlerts });
      mockRequest = { method: 'GET' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ alerts: mockAlerts, count: mockAlerts.length });
    });
  });

  describe('GET /api/gmail/recommendations', () => {
    it('should get recommendations from performance metrics', async () => {
      const mockRecs = [{ type: 'efficiency', recommendation: 'Adjust strategy' }];
      (gmailAIService.getPerformanceMetrics as jest.Mock).mockResolvedValue({ recommendations: mockRecs });
      mockRequest = { method: 'GET' };
      await gmailRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ recommendations: mockRecs, count: mockRecs.length });
    });
  });
});
