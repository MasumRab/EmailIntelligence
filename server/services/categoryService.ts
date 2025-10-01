import { storage } from "../storage";
import { insertCategorySchema } from "@shared/schema";
import { z } from "zod";
import { measureExecutionTime } from "../utils/performance";

export const categoryService = {
  async getAllCategories() {
    return await measureExecutionTime(() => storage.getAllCategories(), "storage.getAllCategories");
  },

  async createCategory(categoryData: z.infer<typeof insertCategorySchema>) {
    const validatedData = insertCategorySchema.parse(categoryData);
    return await measureExecutionTime(() => storage.createCategory(validatedData), "storage.createCategory");
  },

  async updateCategory(id: number, updateData: any) {
    return await measureExecutionTime(() => storage.updateCategory(id, updateData), `storage.updateCategory:${id}`);
  },
};
