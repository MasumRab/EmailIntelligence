import express, { type Application } from 'express';
import { vi } from 'vitest';
import request from 'supertest';
import { z } from 'zod';
import categoryRoutes from './categoryRoutes';
import { storage } from './storage';

vi.mock('./storage', () => ({
  storage: {
    getAllCategories: vi.fn(),
    createCategory: vi.fn(),
    updateCategory: vi.fn(),
  },
}));

vi.mock('@shared/schema', () => ({
  insertCategorySchema: {
    parse: (data: any) => {
      if (!data.name) {
        throw new z.ZodError([]);
      }
      return data;
    },
  },
}));

const app: Application = express();
app.use(express.json());
app.use('/api/categories', categoryRoutes);

describe('Category Routes', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('GET /api/categories', () => {
    it('should get all categories and return 200', async () => {
      const mockCategories = [{ id: 1, name: 'Work' }];
      (storage.getAllCategories as ReturnType<typeof vi.fn>).mockResolvedValue(mockCategories);

      const response = await request(app).get('/api/categories');

      expect(response.status).toBe(200);
      expect(response.body).toEqual(mockCategories);
    });

    it('should return 500 if fetching categories fails', async () => {
      (storage.getAllCategories as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('DB Error'));

      const response = await request(app).get('/api/categories');

      expect(response.status).toBe(500);
      expect(response.body).toEqual({ message: 'Failed to fetch categories' });
    });
  });

  describe('POST /api/categories', () => {
    it('should create a category and return 201', async () => {
      const newCategoryData = { name: 'Personal', description: 'Personal tasks', color: '#ff0000' };
      const createdCategory = { id: 2, ...newCategoryData, count: 0 };
      (storage.createCategory as ReturnType<typeof vi.fn>).mockResolvedValue(createdCategory);

      const response = await request(app).post('/api/categories').send(newCategoryData);

      expect(response.status).toBe(201);
      expect(response.body).toEqual(createdCategory);
    });

    it('should return 400 for invalid category data', async () => {
      const invalidCategoryData = { name: '' };
      const response = await request(app).post('/api/categories').send(invalidCategoryData);
      expect(response.status).toBe(400);
    });
  });

  describe('PUT /api/categories/:id', () => {
    it('should update a category and return 200', async () => {
      const categoryId = '1';
      const updateData = { name: 'Updated Work' };
      const updatedCategory = { id: 1, name: 'Updated Work', description: '', color: '#000', count: 0 };
      (storage.updateCategory as ReturnType<typeof vi.fn>).mockResolvedValue(updatedCategory);

      const response = await request(app).put(`/api/categories/${categoryId}`).send(updateData);

      expect(response.status).toBe(200);
      expect(response.body).toEqual(updatedCategory);
    });

    it('should return 404 if category to update not found', async () => {
      const categoryId = '99';
      (storage.updateCategory as ReturnType<typeof vi.fn>).mockResolvedValue(undefined);

      const response = await request(app).put(`/api/categories/${categoryId}`).send({ name: 'NonExistent' });

      expect(response.status).toBe(404);
      expect(response.body).toEqual({ message: 'Category not found' });
    });
  });
});
