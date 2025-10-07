import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import { vi } from 'vitest'; // Import vi for Vitest mocking
// Import the exported handlers
import { getAllActivitiesHandler, createActivityHandler } from './activityRoutes';
import { storage } from './storage';

vi.mock('./storage', () => ({
  storage: {
    getRecentActivities: vi.fn(),
    createActivity: vi.fn(),
  },
}));

// createApp might not be needed if we test handlers directly and don't use supertest
// const createApp = (): Application => {
//   const app = express();
//   app.use(express.json());
//   // app.use('/api/activities', activityRoutes); // activityRoutes is the default export (router instance)
//   return app;
// };

describe('Activity Route Handlers', () => {
  // let app: Application; // Not needed for direct handler testing
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
    (storage.getRecentActivities as any).mockClear();
    (storage.createActivity as any).mockClear();
    nextFunction = vi.fn(); // Reset nextFunction mock as well
  });

  describe('getAllActivitiesHandler', () => {
    it('should get recent activities and return 200', async () => {
      const mockActivities = [{ id: 1, description: 'Test Activity' }];
      (storage.getRecentActivities as any).mockResolvedValue(mockActivities);
      mockRequest = { query: { limit: '5' } }; // method: 'GET' is implicit in handler choice

      // Call the specific handler
      await getAllActivitiesHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getRecentActivities).toHaveBeenCalledWith(5);
      expect(mockResponse.json).toHaveBeenCalledWith(mockActivities);
    });

    it('should use default limit if not provided', async () => {
        (storage.getRecentActivities as any).mockResolvedValue([]);
        mockRequest = { query: {} };

        await getAllActivitiesHandler(mockRequest as Request, mockResponse as Response, nextFunction);
        expect(storage.getRecentActivities).toHaveBeenCalledWith(undefined);
    });

    it('should return 500 if fetching activities fails', async () => {
      (storage.getRecentActivities as any).mockRejectedValue(new Error('DB Error'));
      mockRequest = { query: {} };

      await getAllActivitiesHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Failed to fetch activities' });
    });
  });

  describe('createActivityHandler', () => {
    it('should create an activity and return 201', async () => {
      const newActivityData = { type: 'test', description: 'New Activity', icon: 'test', iconBg: 'test', timestamp: 'test' };
      const createdActivity = { id: 2, ...newActivityData };
      (storage.createActivity as any).mockResolvedValue(createdActivity);

      mockRequest = { body: newActivityData }; // method: 'POST' is implicit
      await createActivityHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.createActivity).toHaveBeenCalledWith(newActivityData);
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(createdActivity);
    });

    it('should return 400 for invalid activity data (simulated ZodError in route)', async () => {
        const invalidActivityData = { type: '' }; // Zod schema in route will fail this
        mockRequest = { body: invalidActivityData };

        // The actual Zod parsing is in the handler, so no need to mock storage.createActivity to throw
        // The handler itself should catch the ZodError and respond
        await createActivityHandler(mockRequest as Request, mockResponse as Response, nextFunction);

        expect(mockResponse.status).toHaveBeenCalledWith(400);
        expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ message: "Invalid activity data" }));
      });
  });
});
