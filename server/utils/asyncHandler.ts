/**
 * @file Provides an async middleware wrapper for Express routes.
 *
 * This utility function wraps asynchronous route handlers to ensure that any
 * promise rejections are caught and passed to the Express error handling
 * middleware, avoiding unhandled promise rejections.
 */
import { NextFunction, Request, Response } from "express";

/**
 * Wraps an asynchronous Express route handler to catch errors.
 *
 * This higher-order function takes an async function and returns a new
 * function that can be used as Express middleware. The returned function
 * executes the original async function and catches any promise rejections,
 * passing them to the `next` function for centralized error handling.
 *
 * @param fn - The asynchronous route handler function to wrap.
 * @returns An Express route handler that handles async errors.
 */
export const asyncHandler = (fn: (req: Request, res: Response, next: NextFunction) => Promise<any>) =>
  (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };