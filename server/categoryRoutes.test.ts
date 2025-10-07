import express, { type Application, type Request, type Response, type NextFunction } from 'express';
import { vi } from 'vitest'; // Import vi
// Import the exported handlers
import {
    getAllCategoriesHandler,
    createCategoryHandler,
    updateCategoryHandler
} from './categoryRoutes';
import { storage } from './storage';

vi.mock('./storage', () => ({
  storage: {
    getAllCategories: vi.fn(),
    createCategory: vi.fn(),
    updateCategory: vi.fn(),
  },
}));

// const createApp = (): Application => { // Not needed for direct handler testing
//   const app = express();
//   app.use(express.json());
//   app.use('/api/categories', categoryRoutes); // categoryRoutes is router instance
//   return app;
// };

describe('Category Route Handlers', () => { // Updated describe
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
    (storage.getAllCategories as any).mockClear();
    (storage.createCategory as any).mockClear();
    (storage.updateCategory as any).mockClear();
    nextFunction = vi.fn(); // Reset nextFunction
  });

  describe('getAllCategoriesHandler', () => { // Updated describe
    it('should get all categories and return 200', async () => {
      const mockCategories = [{ id: 1, name: 'Work' }];
      (storage.getAllCategories as any).mockResolvedValue(mockCategories);
      mockRequest = {}; // No specific params for this handler

      await getAllCategoriesHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.getAllCategories).toHaveBeenCalledTimes(1);
      expect(mockResponse.json).toHaveBeenCalledWith(mockCategories);
    });

    it('should return 500 if fetching categories fails', async () => {
      (storage.getAllCategories as any).mockRejectedValue(new Error('DB Error'));
      mockRequest = {};

      await getAllCategoriesHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(500);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Failed to fetch categories' });
    });
  });

  describe('createCategoryHandler', () => { // Updated describe
    it('should create a category and return 201', async () => {
      const newCategoryData = { name: 'Personal', description: 'Personal tasks', color: '#ff0000' };
      const createdCategory = { id: 2, ...newCategoryData, count: 0 };
      (storage.createCategory as any).mockResolvedValue(createdCategory);

      mockRequest = { body: newCategoryData };

      await createCategoryHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.createCategory).toHaveBeenCalledWith(newCategoryData);
      expect(mockResponse.status).toHaveBeenCalledWith(201);
      expect(mockResponse.json).toHaveBeenCalledWith(createdCategory);
    });

    it('should return 400 for invalid category data (ZodError in route)', async () => {
      const invalidCategoryData = { name: '' };
      mockRequest = { body: invalidCategoryData };

      // Zod parsing is in the handler, so it should catch and respond
      await createCategoryHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(400);
      expect(mockResponse.json).toHaveBeenCalledWith(expect.objectContaining({ message: "Invalid category data" }));
    });
  });

  describe('updateCategoryHandler', () => { // Updated describe
    it('should update a category and return 200', async () => {
      const categoryId = '1';
      const updateData = { name: 'Updated Work' };
      const updatedCategory = { id: 1, name: 'Updated Work', description: '', color: '#000', count: 0 };
      (storage.updateCategory as any).mockResolvedValue(updatedCategory);

      mockRequest = { params: { id: categoryId }, body: updateData };

      await updateCategoryHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(storage.updateCategory).toHaveBeenCalledWith(parseInt(categoryId), updateData);
      expect(mockResponse.json).toHaveBeenCalledWith(updatedCategory);
    });

    it('should return 404 if category to update not found', async () => {
      const categoryId = '99';
      (storage.updateCategory as any).mockResolvedValue(undefined); // Simulate not found

      mockRequest = { params: { id: categoryId }, body: { name: 'NonExistent' } };

      await updateCategoryHandler(mockRequest as Request, mockResponse as Response, nextFunction);

      expect(mockResponse.status).toHaveBeenCalledWith(404);
      expect(mockResponse.json).toHaveBeenCalledWith({ message: 'Category not found' });
    });
  });
});
