/**
 * @file Service layer for handling category-related business logic.
 *
 * This service provides methods for creating, retrieving, and updating
 * email categories. It uses the storage layer for data persistence and Zod
 * for data validation.
 */
import { storage } from "../storage";
import { insertCategorySchema } from "@shared/schema";
import { z } from "zod";
import { measureExecutionTime } from "../utils/performance";

export const categoryService = {
  /**
   * Retrieves all categories from storage.
   * @returns {Promise<Array<object>>} A promise that resolves to a list of all categories.
   */
  async getAllCategories() {
    return await measureExecutionTime(() => storage.getAllCategories(), "storage.getAllCategories");
  },

  /**
   * Creates a new category after validating the input data.
   * @param {object} categoryData - The data for the new category.
   * @param {string} categoryData.name - The name of the category.
   * @param {string} [categoryData.color] - The color of the category.
   * @returns {Promise<object>} A promise that resolves to the newly created category object.
   */
  async createCategory(categoryData: z.infer<typeof insertCategorySchema>) {
    const validatedData = insertCategorySchema.parse(categoryData);
    return await measureExecutionTime(() => storage.createCategory(validatedData), "storage.createCategory");
  },

  /**
   * Updates an existing category.
   * @param {number} id - The ID of the category to update.
   * @param {object} updateData - An object containing the fields to update.
   * @returns {Promise<object>} A promise that resolves to the updated category object.
   */
  async updateCategory(id: number, updateData: any) {
    return await measureExecutionTime(() => storage.updateCategory(id, updateData), `storage.updateCategory:${id}`);
  },
};