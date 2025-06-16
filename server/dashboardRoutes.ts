import express from "express";
import { storage } from "./storage";

const router = express.Router();

// Dashboard stats
router.get("/stats", async (_req, res) => {
  try {
    console.time("storage.getDashboardStats");
    const stats = await storage.getDashboardStats();
    console.timeEnd("storage.getDashboardStats");
    res.json(stats);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch dashboard stats" });
  }
});

export default router;
