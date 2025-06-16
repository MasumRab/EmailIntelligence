import express from "express";
import { storage } from "./storage";
import { insertEmailSchema } from "@shared/schema";
import { z } from "zod";

const router = express.Router();

// Emails
router.get("/", async (req, res) => {
  try {
    const { category, search } = req.query;

    let emails;
    if (search && typeof search === 'string') {
      console.time("storage.searchEmails");
      emails = await storage.searchEmails(search);
      console.timeEnd("storage.searchEmails");
    } else if (category && typeof category === 'string') {
      const categoryId = parseInt(category);
      console.time("storage.getEmailsByCategory");
      emails = await storage.getEmailsByCategory(categoryId);
      console.timeEnd("storage.getEmailsByCategory");
    } else {
      console.time("storage.getAllEmails");
      emails = await storage.getAllEmails();
      console.timeEnd("storage.getAllEmails");
    }

    res.json(emails);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch emails" });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    console.time("storage.getEmailById");
    const email = await storage.getEmailById(id);
    console.timeEnd("storage.getEmailById");

    if (!email) {
      return res.status(404).json({ message: "Email not found" });
    }

    res.json(email);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch email" });
  }
});

router.post("/", async (req, res) => {
  try {
    const emailData = insertEmailSchema.parse(req.body);
    console.time("storage.createEmail");
    const email = await storage.createEmail(emailData);
    console.timeEnd("storage.createEmail");
    res.status(201).json(email);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ message: "Invalid email data", errors: error.errors });
    } else {
      res.status(500).json({ message: "Failed to create email" });
    }
  }
});

router.put("/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const updateData = req.body;
    console.time("storage.updateEmail");
    const email = await storage.updateEmail(id, updateData);
    console.timeEnd("storage.updateEmail");

    if (!email) {
      return res.status(404).json({ message: "Email not found" });
    }

    res.json(email);
  } catch (error) {
    res.status(500).json({ message: "Failed to update email" });
  }
});

export default router;
