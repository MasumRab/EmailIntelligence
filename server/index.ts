/**
 * @file The main entry point for the Express server.
 *
 * This file is responsible for initializing the Express application, setting up
 * middleware, registering API routes, and starting the server. It also handles
 * database initialization and environment-specific configurations for development
 * and production.
 */
import dotenv from "dotenv";
// Load environment variables from .env file
dotenv.config();

import express, { type Request, Response, NextFunction } from "express";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { initializeDatabase } from "./init-db";

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Initialize database on startup
initializeDatabase().catch(console.error);

/**
 * Middleware for logging API requests.
 *
 * This middleware captures the start time of a request and logs the method,
 * path, status code, and duration upon completion. It also captures and logs
 * the JSON response body for API endpoints.
 *
 * @param {Request} req - The Express request object.
 * @param {Response} res - The Express response object.
 * @param {NextFunction} next - The next middleware function.
 */
app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  let capturedJsonResponse: Record<string, any> | undefined = undefined;

  const originalResJson = res.json;
  res.json = function (bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };

  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path.startsWith("/api")) {
      let logLine = `${req.method} ${path} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }

      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "…";
      }

      log(logLine);
    }
  });

  next();
});

import { errorHandler } from "./utils/errorHandler";

/**
 * Main server setup and startup function.
 *
 * This async IIFE (Immediately Invoked Function Expression) orchestrates the
 * server startup process. It registers all API routes, sets up the global
 * error handler, configures Vite for development or serves static files for
 * production, and finally starts the server on the specified port.
 */
(async () => {
  const server = await registerRoutes(app);

  app.use(errorHandler);

  // importantly only setup vite in development and after
  // setting up all the other routes so the catch-all route
  // doesn't interfere with the other routes
  if (app.get("env") === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  // ALWAYS serve the app on port 5000
  // this serves both the API and the client.
  // It is the only port that is not firewalled.
  const port = parseInt(process.env.NODE_PORT || "5000", 10);
  server.listen(port, "127.0.0.1", () => {
    log(`serving on port ${port}`);
  });
})();