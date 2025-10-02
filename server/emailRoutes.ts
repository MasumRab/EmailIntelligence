import express from "express";
import { emailService } from "./services/emailService";
import { asyncHandler } from "./utils/asyncHandler";

const router = express.Router();

// Emails
router.get("/", asyncHandler(async (req, res) => {
  const { category, search } = req.query;
  const emails = await emailService.getEmails(category as string, search as string);
  res.json(emails);
}));

router.get("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const email = await emailService.getEmailById(id);
  res.json(email);
}));

router.post("/", asyncHandler(async (req, res) => {
  const email = await emailService.createEmail(req.body);
  res.status(201).json(email);
}));

router.put("/:id", asyncHandler(async (req, res) => {
  const id = parseInt(req.params.id);
  const email = await emailService.updateEmail(id, req.body);
  res.json(email);
}));

export default router;
