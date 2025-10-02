/**
 * @file Defines the global error handling middleware for the Express application.
 *
 * This module provides a centralized error handler that catches errors from
 * the application, logs them, and sends a formatted JSON response to the client
 * with an appropriate HTTP status code.
 */
import { NextFunction, Request, Response } from "express";
import { z } from "zod";

/**
 * Global error handling middleware for the Express application.
 *
 * This function catches and processes errors that occur in the route handlers.
 * It specifically handles Zod validation errors by returning a 400 status
 * with detailed error messages. Other custom errors are handled with their
 * respective status codes, and all other errors result in a generic 500
 * Internal Server Error response.
 *
 * @param {Error} err - The error object.
 * @param {Request} _req - The Express request object (unused).
 * @param {Response} res - The Express response object.
 * @param {NextFunction} _next - The next middleware function (unused).
 * @returns A JSON response with an error message and appropriate status code.
 */
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