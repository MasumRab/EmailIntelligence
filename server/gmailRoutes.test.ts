import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import { vi } from 'vitest'; // Import vi
// Import the exported handlers
import {
    syncGmailHandler,
    smartRetrievalHandler,
    getStrategiesHandler,
    syncInboxHandler,
    syncImportantHandler,
    syncWeeklyBatchHandler,
    trainModelsHandler,
    optimizeStrategyHandler,
    getQuotaStatusHandler,
    getAlertsHandler,
    getRecommendationsHandler
} from './gmailRoutes';
import { gmailAIService } from './gmail-ai-service'; // To mock its methods

// Mock the gmailAIService module
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
    getPerformanceMetrics: vi.fn(), // For quota-status, alerts, recommendations
  },
}));

// const createApp = (): Application => { // Not needed for direct handler testing
//   const app = express();
//   app.use(express.json());
//   app.use('/api/gmail', gmailRoutes);
//   return app;
// };

describe('Gmail Route Handlers', () => { // Updated describe
  // let app: Application; // Not needed
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = vi.fn();

  beforeEach(() => {
    // app = createApp(); // Not needed
    mockRequest = {};
    mockResponse = {
      json: vi.fn().mockReturnThis(),
      status: vi.fn().mockReturnThis(),
    };
    // Reset mocks for gmailAIService methods
    Object.values(gmailAIService).forEach(mockFn => {
        if (vi.isMockFunction(mockFn)) {
            (mockFn as any).mockClear();
        }
    });
    nextFunction = vi.fn(); // Reset nextFunction
  });

  describe('syncGmailHandler', () => { // Updated describe
    it('should call gmailAIService.syncGmailEmails and return result', async () => {
      const mockSyncResult = { success: true, processedCount: 10 };
      (gmailAIService.syncGmailEmails as any).mockResolvedValue(mockSyncResult);
      mockRequest = { body: { maxEmails: 100 } };

      await syncGmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.syncGmailEmails).toHaveBeenCalledWith(expect.objectContaining({ maxEmails: 100 }));
      expect(mockResponse.json).toHaveBeenCalledWith(mockSyncResult);
    });

    it('should return 500 if syncGmailEmails fails', async () => {
      (gmailAIService.syncGmailEmails as any).mockRejectedValue(new Error('Sync Error'));
      mockRequest = { body: {} };

      await syncGmailHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ success: false }));
    });
  });

  describe('smartRetrievalHandler', () => { // Updated describe
    it('should call gmailAIService.executeSmartRetrieval and return result', async () => {
      const mockRetrievalResult = { success: true, processedCount: 5 };
      (gmailAIService.executeSmartRetrieval as any).mockResolvedValue(mockRetrievalResult);
      mockRequest = { body: { strategies: ['test'] } };

      await smartRetrievalHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.executeSmartRetrieval).toHaveBeenCalledWith(['test'], 100, 30); // Default values
      expect(mockResponse.json).toHaveBeenCalledWith(mockRetrievalResult);
    });
  });

  describe('getStrategiesHandler', () => { // Updated describe
    it('should call gmailAIService.getRetrievalStrategies and return strategies', async () => {
      const mockStrategies = [{ name: 'strategy1' }];
      (gmailAIService.getRetrievalStrategies as any).mockResolvedValue(mockStrategies);
      mockRequest = {}; // No specific params

      await getStrategiesHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(gmailAIService.getRetrievalStrategies).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ strategies: mockStrategies });
    });
  });

  describe('syncInboxHandler', () => { // Updated describe
    it('should call gmailAIService.syncInboxEmails', async () => {
      (gmailAIService.syncInboxEmails as any).mockResolvedValue({ success: true });
      mockRequest = { body: { maxEmails: 50 } };
      await syncInboxHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.syncInboxEmails).toHaveBeenCalledWith(50);
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });
  });

  describe('trainModelsHandler', () => { // Updated describe
    it('should call gmailAIService.trainModelsFromGmail', async () => {
      (gmailAIService.trainModelsFromGmail as any).mockResolvedValue({ success: true });
      mockRequest = { body: { trainingQuery: "test" } };
      await trainModelsHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.trainModelsFromGmail).toHaveBeenCalledWith("test", 5000); // Default maxTrainingEmails
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });
  });

  describe('optimizeStrategyHandler', () => { // Updated describe
    it('should call gmailAIService.applyAdaptiveOptimization if strategyName is provided', async () => {
      (gmailAIService.applyAdaptiveOptimization as any).mockResolvedValue({ success: true });
      mockRequest = { body: { strategyName: "test_strat" } };
      await optimizeStrategyHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.applyAdaptiveOptimization).toHaveBeenCalledWith("test_strat");
      expect(mockResponse.json).toHaveBeenCalledWith({ success: true });
    });

    it('should return 400 if strategyName is missing', async () => {
        mockRequest = { body: {} }; // strategyName is missing
        await optimizeStrategyHandler(mockRequest as Request, mockResponse as Response, nextFunction);
        expect(mockResponse.status).toHaveBeenCalledWith(400);
        expect(mockResponse.json).toHaveBeenCalledWith({ success: false, error: "Strategy name is required" });
      });
  });

  describe('getQuotaStatusHandler', () => { // Updated describe
    it('should get quota status from performance metrics', async () => {
      const mockQuotaStatus = { dailyUsage: { percentage: 50 } };
      (gmailAIService.getPerformanceMetrics as any).mockResolvedValue({ quotaStatus: mockQuotaStatus });
      mockRequest = {};
      await getQuotaStatusHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith(mockQuotaStatus);
    });
  });

  describe('getAlertsHandler', () => { // Updated describe
    it('should get alerts from performance metrics', async () => {
      const mockAlerts = [{ type: 'quota', message: 'High usage' }];
      (gmailAIService.getPerformanceMetrics as any).mockResolvedValue({ alerts: mockAlerts });
      mockRequest = {};
      await getAlertsHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ alerts: mockAlerts, count: mockAlerts.length });
    });
  });

  describe('getRecommendationsHandler', () => { // Updated describe
    it('should get recommendations from performance metrics', async () => {
      const mockRecs = [{ type: 'efficiency', recommendation: 'Adjust strategy' }];
      (gmailAIService.getPerformanceMetrics as any).mockResolvedValue({ recommendations: mockRecs });
      mockRequest = {};
      await getRecommendationsHandler(mockRequest as Request, mockResponse as Response, nextFunction);
      expect(gmailAIService.getPerformanceMetrics).toHaveBeenCalled();
      expect(mockResponse.json).toHaveBeenCalledWith({ recommendations: mockRecs, count: mockRecs.length });
    });
  });
});
