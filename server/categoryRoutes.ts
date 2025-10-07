/**
 * @file Defines the API routes for category management.
 *
 * This file creates an Express router for handling all CRUD (Create, Read, Update, Delete)
 * operations related to email categories. It uses the `categoryService` to interact
 * with the data layer.
 */
import express from "express";
import { categoryService } from "./services/categoryService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

/**
 * @route GET /api/categories/
 * @description Retrieves all email categories.
 * @returns {Array<object>} A list of all category objects.
 */
router.get("/", asyncHandler(async (_req, res) => {
  const categories = await categoryService.getAllCategories();
  res.json(categories);
}));

/**
 * @route POST /api/categories/
 * @description Creates a new email category.
 * @param {object} req.body - The request body.
 * @param {string} req.body.name - The name of the new category.
 * @param {string} [req.body.color] - The color of the new category.
 * @returns {object} The newly created category object.
 */
router.post("/", asyncHandler(async (req, res) => {
  const category = await categoryService.createCategory(req.body);
  res.status(201).json(category);
}));

/**
 * @route PUT /api/categories/:id
 * @description Updates an existing email category.
 * @param {object} req.params - The route parameters.
 * @param {string} req.params.id - The ID of the category to update.
 * @param {object} req.body - The request body containing the updated category data.
 * @returns {object} The updated category object.
 */
router.put("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const category = await categoryService.updateCategory(id, req.body);
  res.json(category);
}));

export default router;