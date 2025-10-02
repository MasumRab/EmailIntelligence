import express from "express";
import { categoryService } from "./services/categoryService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

// Categories
router.get("/", asyncHandler(async (_req, res) => {
  const categories = await categoryService.getAllCategories();
  res.json(categories);
}));

router.post("/", asyncHandler(async (req, res) => {
  const category = await categoryService.createCategory(req.body);
  res.status(201).json(category);
}));

router.put("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const category = await categoryService.updateCategory(id, req.body);
  res.json(category);
}));

export default router;
