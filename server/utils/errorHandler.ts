import { NextFunction, Request, Response } from "express";
import { z } from "zod";

export function errorHandler(err: Error, _req: Request, res: Response, _next: NextFunction) {
  console.error(err);

  if (err instanceof z.ZodError) {
    return res.status(400).json({
      message: "Invalid data",
      errors: err.errors,
    });
  }

  if (err.message === "Email not found" || err.message === "Category not found") {
    return res.status(404).json({ message: err.message });
  }

  if (err.message === "Subject and content are required" || err.message === "Email IDs array is required") {
    return res.status(400).json({ message: err.message });
  }

  return res.status(500).json({ message: "Internal Server Error" });
}
