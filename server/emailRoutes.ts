/**
 * @file Defines the API routes for email management.
 *
 * This file creates an Express router for handling all CRUD (Create, Read, Update, Delete)
 * operations related to emails. It uses the `emailService` to interact with the
 * data layer and supports filtering by category and search terms.
 */
import express from "express";
import { emailService } from "./services/emailService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

/**
 * @route GET /api/emails/
 * @description Retrieves a list of emails, with optional filtering by category or search query.
 * @param {string} [req.query.category] - The category to filter emails by.
 * @param {string} [req.query.search] - The search term to filter emails by.
 * @returns {Array<object>} A list of email objects that match the criteria.
 */
router.get("/", asyncHandler(async (req, res) => {
  const { category, search } = req.query;
  const emails = await emailService.getEmails(category as string, search as string);
  res.json(emails);
}));

/**
 * @route GET /api/emails/:id
 * @description Retrieves a single email by its ID.
 * @param {object} req.params - The route parameters.
 * @param {string} req.params.id - The ID of the email to retrieve.
 * @returns {object} The email object if found, otherwise null.
 */
router.get("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const email = await emailService.getEmailById(id);
  res.json(email);
}));

/**
 * @route POST /api/emails/
 * @description Creates a new email.
 * @param {object} req.body - The request body containing the new email's data.
 * @returns {object} The newly created email object.
 */
router.post("/", asyncHandler(async (req, res) => {
  const email = await emailService.createEmail(req.body);
  res.status(201).json(email);
}));

/**
 * @route PUT /api/emails/:id
 * @description Updates an existing email.
 * @param {object} req.params - The route parameters.
 * @param {string} req.params.id - The ID of the email to update.
 * @param {object} req.body - The request body containing the updated email data.
 * @returns {object} The updated email object.
 */
router.put("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const email = await emailService.updateEmail(id, req.body);
  res.json(email);
}));

export default router;