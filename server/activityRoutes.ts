import express from "express";
import { storage } from "./storage";
import { insertActivitySchema } from "@shared/schema";
import { z } from "zod";

const router = express.Router();

// Handler for GET /api/activities
export const getAllActivitiesHandler = async (req, res) => {
  try {
    const { limit } = req.query;
    console.time("storage.getRecentActivities");
    const activities = await storage.getRecentActivities(
      limit ? parseInt(limit as string) : undefined
    );
    console.timeEnd("storage.getRecentActivities");
    res.json(activities);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch activities" });
  }
};

// Handler for POST /api/activities
export const createActivityHandler = async (req, res) => {
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
};

// Activities
router.get("/", getAllActivitiesHandler);
router.post("/", createActivityHandler);

export default router;
