import express from "express";
import { storage } from "./storage";
import { insertCategorySchema } from "@shared/schema";
import { z } from "zod";

const router = express.Router();

// Categories
router.get("/", async (_req, res) => {
  try {
    console.time("storage.getAllCategories");
    const categories = await storage.getAllCategories();
    console.timeEnd("storage.getAllCategories");
    res.json(categories);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch categories" });
  }
});

router.post("/", async (req, res) => {
  try {
    const categoryData = insertCategorySchema.parse(req.body);
    console.time("storage.createCategory");
    const category = await storage.createCategory(categoryData);
    console.timeEnd("storage.createCategory");
    res.status(201).json(category);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ message: "Invalid category data", errors: error.errors });
    } else {
      res.status(500).json({ message: "Failed to create category" });
    }
  }
});

router.put("/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const updateData = req.body;
    console.time("storage.updateCategory");
    const category = await storage.updateCategory(id, updateData);
    console.timeEnd("storage.updateCategory");

    if (!category) {
      return res.status(404).json({ message: "Category not found" });
    }

    res.json(category);
  } catch (error) {
    res.status(500).json({ message: "Failed to update category" });
  }
});

export default router;
