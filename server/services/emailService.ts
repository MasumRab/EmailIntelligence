import { storage } from "../storage";
import { insertEmailSchema } from "@shared/schema";
import { z } from "zod";
import { measureExecutionTime } from "../utils/performance";

export const emailService = {
  async getEmails(category?: string, search?: string) {
    if (search) {
      return await measureExecutionTime(() => storage.searchEmails(search), "storage.searchEmails");
    }
    if (category) {
      const categoryId = parseInt(category);
      return await measureExecutionTime(() => storage.getEmailsByCategory(categoryId), "storage.getEmailsByCategory");
    }
    return await measureExecutionTime(() => storage.getAllEmails(), "storage.getAllEmails");
  },

  async getEmailById(id: number) {
    return await measureExecutionTime(() => storage.getEmailById(id), `storage.getEmailById:${id}`);
  },

  async createEmail(emailData: z.infer<typeof insertEmailSchema>) {
    const validatedData = insertEmailSchema.parse(emailData);
    return await measureExecutionTime(() => storage.createEmail(validatedData), "storage.createEmail");
  },

  async updateEmail(id: number, updateData: any) {
    return await measureExecutionTime(() => storage.updateEmail(id, updateData), `storage.updateEmail:${id}`);
  },
};
