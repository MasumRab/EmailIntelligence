/**
 * @file Service layer for handling email-related business logic.
 *
 * This service provides methods for creating, retrieving, and updating emails.
 * It uses the storage layer for data persistence and supports fetching emails
 * with filtering and search capabilities.
 */
import { storage } from "../storage";
import { insertEmailSchema } from "@shared/schema";
import { z } from "zod";
import { measureExecutionTime } from "../utils/performance";

export const emailService = {
  /**
   * Retrieves emails, optionally filtering by category or a search term.
   * @param {string} [category] - The category ID to filter by.
   * @param {string} [search] - A search term to filter emails by.
   * @returns {Promise<Array<object>>} A promise that resolves to a list of emails.
   */
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

  /**
   * Retrieves a single email by its ID.
   * @param {number} id - The ID of the email to retrieve.
   * @returns {Promise<object|null>} A promise that resolves to the email object, or null if not found.
   */
  async getEmailById(id: number) {
    return await measureExecutionTime(() => storage.getEmailById(id), `storage.getEmailById:${id}`);
  },

  /**
   * Creates a new email after validating the input data.
   * @param {object} emailData - The data for the new email.
   * @returns {Promise<object>} A promise that resolves to the newly created email object.
   */
  async createEmail(emailData: z.infer<typeof insertEmailSchema>) {
    const validatedData = insertEmailSchema.parse(emailData);
    return await measureExecutionTime(() => storage.createEmail(validatedData), "storage.createEmail");
  },

  /**
   * Updates an existing email.
   * @param {number} id - The ID of the email to update.
   * @param {object} updateData - An object containing the fields to update.
   * @returns {Promise<object>} A promise that resolves to the updated email object.
   */
  async updateEmail(id: number, updateData: any) {
    return await measureExecutionTime(() => storage.updateEmail(id, updateData), `storage.updateEmail:${id}`);
  },
};