import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import dashboardRoutes from './dashboardRoutes';
import { storage } from './storage';
import { type DashboardStats } from '@shared/schema';

jest.mock('./storage', () => ({
  storage: {
    getDashboardStats: jest.fn(),
  },
}));

const createApp = (): Application => {
  const app = express();
  app.use(express.json());
  app.use('/api/dashboard', dashboardRoutes); // Assuming dashboardRoutes handles paths like /stats
  return app;
};

describe('Dashboard Routes', () => {
  let app: Application;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = jest.fn();

  const mockStats: DashboardStats = {
    totalEmails: 100,
    autoLabeled: 50,
    categories: 5,
    timeSaved: "10h",
    weeklyGrowth: {
      totalEmails: 10,
      autoLabeled: 5,
      categories: 1,
      timeSaved: 1,
    },
  };

  beforeEach(() => {
    app = createApp();
    mockRequest = {}; // Reset request object for each test
    mockResponse = { // Reset response object for each test
      json: jest.fn().mockReturnThis(),
      status: jest.fn().mockReturnThis(),
    };
    (storage.getDashboardStats as jest.Mock).mockClear();
  });

  describe('GET /api/dashboard/stats', () => {
    it('should get dashboard stats and return 200', async () => {
      (storage.getDashboardStats as jest.Mock).mockResolvedValue(mockStats);
      // Simulate the Express router handling by directly invoking the router function
      // For this to work correctly, the path matching (e.g., /stats) is handled internally by the Express Router instance
      // when mounted in an app. For unit testing the handler logic directly:
      mockRequest = { path: '/stats', method: 'GET' }; // Path might not be needed if not checked by handler itself

      await dashboardRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getDashboardStats).toHaveBeenCalledTimes(1);
      expect(mockResponse.json).toHaveBeenCalledWith(mockStats);
    });

    it('should return 500 if fetching stats fails', async () => {
      (storage.getDashboardStats as jest.Mock).mockRejectedValue(new Error('DB Error'));
      mockRequest = { path: '/stats', method: 'GET' };

      await dashboardRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Failed to fetch dashboard stats' });
    });
  });
});
[end of server/dashboardRoutes.test.ts]
