import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import { vi } from 'vitest'; // Import vi
// Import the exported handler
import { getDashboardStatsHandler } from './dashboardRoutes';
import { storage } from './storage';
import { type DashboardStats } from '@shared/schema';

vi.mock('./storage', () => ({
  storage: {
    getDashboardStats: vi.fn(),
  },
}));

// const createApp = (): Application => { // Not needed for direct handler testing
//   const app = express();
//   app.use(express.json());
//   app.use('/api/dashboard', dashboardRoutes);
//   return app;
// };

describe('Dashboard Route Handlers', () => { // Updated describe
  // let app: Application; // Not needed
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let nextFunction: NextFunction = vi.fn(); // Use vi.fn()

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
    // app = createApp(); // Not needed
    mockRequest = {};
    mockResponse = {
      json: vi.fn().mockReturnThis(),
      status: vi.fn().mockReturnThis(),
    };
    (storage.getDashboardStats as any).mockClear();
    nextFunction = vi.fn(); // Reset nextFunction as well
  });

  describe('getDashboardStatsHandler', () => { // Updated describe
    it('should get dashboard stats and return 200', async () => {
      (storage.getDashboardStats as any).mockResolvedValue(mockStats);
      mockRequest = {}; // No specific path or method needed for direct handler call

      await getDashboardStatsHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getDashboardStats).toHaveBeenCalledTimes(1);
      expect(mockResponse.json).toHaveBeenCalledWith(mockStats);
    });

    it('should return 500 if fetching stats fails', async () => {
      (storage.getDashboardStats as any).mockRejectedValue(new Error('DB Error'));
      mockRequest = {};

      await getDashboardStatsHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Failed to fetch dashboard stats' });
    });
  });
});
