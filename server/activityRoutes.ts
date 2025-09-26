import express from "express";
import { storage } from "./storage";
import { insertActivitySchema } from "@shared/schema";
import { z } from "zod";

const router = express.Router();

// Activities
router.get("/", async (req, res) => {
  try {
    const { limit } = req.query;
    console.time("storage.getRecentActivities");
    const activities = await storage.getRecentActivities(
      limit ? parseInt(limit as string) : 10
    );
    console.timeEnd("storage.getRecentActivities");
    res.json(activities);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch activities" });
  }
});

router.post("/", async (req, res) => {
  try {
    const activityData = insertActivitySchema.parse(req.body);
    console.time("storage.createActivity");
    const activity = await storage.createActivity(activityData);
    console.timeEnd("storage.createActivity");
    res.status(201).json(activity);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ message: "Invalid activity data", errors: error.errors });
    } else {
      res.status(500).json({ message: "Failed to create activity" });
    }
  }
});

export default router;
