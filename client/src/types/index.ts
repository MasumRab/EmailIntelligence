export * from "@shared/schema";

export interface SearchFilters {
  category?: string;
  sender?: string;
  starred?: boolean;
  read?: boolean;
}

export interface SyncResult {
  synced: number;
  newEmails: any[];
  errors?: string[];
}

export interface AICategorizationResult {
  success: boolean;
  email: any;
  confidence: number;
  suggestedLabels?: string[];
}
