import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import activityRoutes from './activityRoutes';
import { storage } from './storage';

jest.mock('./storage', () => ({
  storage: {
    getRecentActivities: jest.fn(),
    createActivity: jest.fn(),
  },
}));

const createApp = (): Application => {
  const app = express();
  app.use(express.json());
  app.use('/api/activities', activityRoutes);
  return app;
};

describe('Activity Routes', () => {
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
    (storage.getRecentActivities as jest.Mock).mockClear();
    (storage.createActivity as jest.Mock).mockClear();
  });

  describe('GET /api/activities', () => {
    it('should get recent activities and return 200', async () => {
      const mockActivities = [{ id: 1, description: 'Test Activity' }];
      (storage.getRecentActivities as jest.Mock).mockResolvedValue(mockActivities);
      mockRequest = { query: { limit: '5' }, method: 'GET' };

      await activityRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getRecentActivities).toHaveBeenCalledWith(5);
      expect(mockResponse.json).toHaveBeenCalledWith(mockActivities);
    });

    it('should use default limit if not provided', async () => {
        (storage.getRecentActivities as jest.Mock).mockResolvedValue([]);
        mockRequest = { query: {}, method: 'GET' };

        await activityRoutes(mockRequest as Request, mockResponse as Response, nextFunction);
        expect(storage.getRecentActivities).toHaveBeenCalledWith(undefined); // or specific default if defined in handler
    });

    it('should return 500 if fetching activities fails', async () => {
      (storage.getRecentActivities as jest.Mock).mockRejectedValue(new Error('DB Error'));
      mockRequest = { query: {}, method: 'GET' };

      await activityRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Failed to fetch activities' });
    });
  });

  describe('POST /api/activities', () => {
    it('should create an activity and return 201', async () => {
      const newActivityData = { type: 'test', description: 'New Activity', icon: 'test', iconBg: 'test', timestamp: 'test' };
      const createdActivity = { id: 2, ...newActivityData };
      (storage.createActivity as jest.Mock).mockResolvedValue(createdActivity);

      mockRequest = { body: newActivityData, method: 'POST' };
      await activityRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.createActivity).toHaveBeenCalledWith(newActivityData);
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(createdActivity);
    });

    it('should return 400 for invalid activity data (simulated ZodError)', async () => {
        // This test path is challenging to hit directly without supertest
        // if Zod parsing happens inside the route handler before the mock.
        const invalidActivityData = { type: '' };
        const zodError = new Error("Invalid activity data") as any;
        zodError.errors = [{ message: "Type cannot be empty" }];
        zodError.name = "ZodError";

        // If storage.createActivity was called and it threw an error that was then
        // identified as a ZodError equivalent by the route handler:
        (storage.createActivity as jest.Mock).mockImplementation(() => {
           throw zodError;
        });

        mockRequest = { body: invalidActivityData, method: 'POST' };
        await activityRoutes(mockRequest as Request, mockResponse as Response, nextFunction);

        expect(mockResponse.status).toHaveBeenCalledWith(400);
        expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ message: "Invalid activity data" }));
      });
  });
});
[end of server/activityRoutes.test.ts]
