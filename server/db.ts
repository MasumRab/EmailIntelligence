import dotenv from "dotenv";
// Load environment variables from .env file
dotenv.config();

// import { Pool } from 'pg'; // Removed for SQLite
// import { drizzle } from 'drizzle-orm/node-postgres'; // Removed for SQLite
import Database from 'better-sqlite3';
import { drizzle } from 'drizzle-orm/better-sqlite3';
import * as schema from "@shared/schema";

// if (!process.env.DATABASE_URL) { // Removed, defaulting to local sqlite.db
//   throw new Error(
//     "DATABASE_URL must be set. Did you forget to provision a database?",
//   );
// }

// export const pool = new Pool({ connectionString: process.env.DATABASE_URL }); // Removed for SQLite
<<<<<<< HEAD
const sqliteDbPath = process.env.DATABASE_URL || 'sqlite.db';
const sqlite = new Database(sqliteDbPath);
=======
const sqlite = new Database('sqlite.db');
>>>>>>> 3b25c44ce8d35ed3fff3b3d8b18a6149725285f5
export const db = drizzle(sqlite, { schema });
