import type { Express } from "express";
import { createServer, type Server } from "http";
import emailRoutes from "./emailRoutes";
import categoryRoutes from "./categoryRoutes";
import aiRoutes from "./aiRoutes";
import gmailRoutes from "./gmailRoutes";
import performanceRoutes from "./performanceRoutes";
import activityRoutes from "./activityRoutes";
import dashboardRoutes from "./dashboardRoutes";

/**
 * Registers all HTTP API routes for dashboard statistics, categories, emails, activities, AI analysis and categorization, Gmail synchronization, performance monitoring, AI training, optimization, and utility endpoints on the provided Express app, and returns an HTTP server instance.
 *
 * @param app - The Express application instance to register routes on.
 * @returns The created HTTP server with all routes registered.
 *
 * @remark
 * The registered routes include endpoints for CRUD operations on categories, emails, and activities; advanced AI-powered email analysis and categorization (including batch and validation workflows); Gmail synchronization and smart retrieval; performance and quota monitoring; AI model training and optimization; and utility endpoints for alerts and recommendations. Most endpoints handle errors by returning appropriate HTTP status codes and JSON error messages.
 */

export async function registerRoutes(app: Express): Promise<Server> {
  app.use("/api/emails", emailRoutes);
  app.use("/api/categories", categoryRoutes);
  app.use("/api/ai", aiRoutes);
  app.use("/api/gmail", gmailRoutes);
  app.use("/api/performance", performanceRoutes);
  app.use("/api/activities", activityRoutes);
  app.use("/api/dashboard", dashboardRoutes);

  const httpServer = createServer(app);
  return httpServer;
}
