import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import dashboardRoutes from './dashboardRoutes';
import { storage } from './storage';
import { type DashboardStats } from '@shared/schema';

vi.mock('./storage', () => ({
  storage: {
    getDashboardStats: vi.fn(),
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/dashboard', dashboardRoutes);

describe('Dashboard Routes', () => {
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
    vi.clearAllMocks();
  });

  describe('GET /api/dashboard/stats', () => {
    it('should get dashboard stats and return 200', async () => {
      (storage.getDashboardStats as ReturnType<typeof vi.fn>).mockResolvedValue(mockStats);

      const response = await request(app).get('/api/dashboard/stats');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockStats);
    });

    it('should return 500 if fetching stats fails', async () => {
      (storage.getDashboardStats as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('DB Error'));

      const response = await request(app).get('/api/dashboard/stats');

      expect(response.status).toBe(500);
      expect(response.body).toEqual({ message: 'Failed to fetch dashboard stats' });
    });
  });
});
