import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import { z } from 'zod';
import activityRoutes from './activityRoutes';
import { storage } from './storage';
import { insertActivitySchema } from '@shared/schema';

vi.mock('./storage', () => ({
  storage: {
    getRecentActivities: vi.fn(),
    createActivity: vi.fn(),
  },
}));

vi.mock('@shared/schema', () => ({
  insertActivitySchema: {
    parse: (data: any) => {
      if (!data.type) {
        throw new z.ZodError([]);
      }
      return data;
    },
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/activities', activityRoutes);

describe('Activity Routes', () => {
  beforeEach(() => {
    (storage.getRecentActivities as ReturnType<typeof vi.fn>).mockClear();
    (storage.createActivity as ReturnType<typeof vi.fn>).mockClear();
  });

  describe('GET /api/activities', () => {
    it('should get recent activities and return 200', async () => {
      const mockActivities = [{ id: 1, description: 'Test Activity' }];
      (storage.getRecentActivities as ReturnType<typeof vi.fn>).mockResolvedValue(mockActivities);

      const response = await request(app).get('/api/activities?limit=5');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockActivities);
      expect(storage.getRecentActivities).toHaveBeenCalledWith(5);
    });

    it('should use default limit if not provided', async () => {
        (storage.getRecentActivities as ReturnType<typeof vi.fn>).mockResolvedValue([]);
        await request(app).get('/api/activities');
        expect(storage.getRecentActivities).toHaveBeenCalledWith(10);
    });

    it('should return 500 if fetching activities fails', async () => {
      (storage.getRecentActivities as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('DB Error'));
      const response = await request(app).get('/api/activities');
      expect(response.status).toBe(500);
      expect(response.body).toEqual({ message: 'Failed to fetch activities' });
    });
  });

  describe('POST /api/activities', () => {
    it('should create an activity and return 201', async () => {
      const newActivityData = { type: 'test', description: 'New Activity', icon: 'test', iconBg: 'test', timestamp: 'test' };
      const createdActivity = { id: 2, ...newActivityData };
      (storage.createActivity as ReturnType<typeof vi.fn>).mockResolvedValue(createdActivity);

      const response = await request(app).post('/api/activities').send(newActivityData);

      expect(response.status).toBe(201);
      expect(response.body).toEqual(createdActivity);
      expect(storage.createActivity).toHaveBeenCalledWith(newActivityData);
    });

    it('should return 400 for invalid activity data', async () => {
        const invalidActivityData = { type: '' };
        const response = await request(app).post('/api/activities').send(invalidActivityData);
        expect(response.status).toBe(400);
        expect(response.body).toHaveProperty('message', 'Invalid activity data');
      });
  });
});
