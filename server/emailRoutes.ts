import express from "express";
import { pythonNLP } from "./python-bridge";
import { insertEmailSchema } from "@shared/schema";
import { z } from "zod";

const router = express.Router();

// Emails
router.get("/", async (req, res) => {
  try {
    const { category, search } = req.query;

    const emails = await pythonNLP.getEmails(
      category as string,
      search as string
    );
    res.json(emails);
  } catch (error) {
    res.status(500).json({ message: "Failed to fetch emails" });
  }
});

router.get("/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const email = await pythonNLP.getEmailById(id);

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
    const email = await pythonNLP.createEmail(emailData);
    res.status(201).json(email);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res
        .status(400)
        .json({ message: "Invalid email data", errors: error.errors });
    } else {
      res.status(500).json({ message: "Failed to create email" });
    }
  }
});

router.put("/:id", async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const updateData = req.body;
    const email = await pythonNLP.updateEmail(id, updateData);

    if (!email) {
      return res.status(404).json({ message: "Email not found" });
    }

    res.json(email);
  } catch (error) {
    res.status(500).json({ message: "Failed to update email" });
  }
});

export default router;
