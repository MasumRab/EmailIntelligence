import express from "express";
import { storage } from "./storage";

const router = express.Router();

// Handler for GET /api/dashboard/stats
export const getDashboardStatsHandler = async (_req, res) => {
  try {
    console.time("storage.getDashboardStats");
    const stats = await storage.getDashboardStats();
    console.timeEnd("storage.getDashboardStats");
    res.json(stats);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch dashboard stats" });
  }
};

// Dashboard stats
router.get("/stats", getDashboardStatsHandler);

export default router;
