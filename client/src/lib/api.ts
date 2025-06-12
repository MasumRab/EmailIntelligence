import { apiRequest } from "./queryClient";

export const api = {
  // Dashboard
  getDashboardStats: () => fetch("/api/dashboard/stats").then(res => res.json()),
  
  // Categories
  getCategories: () => fetch("/api/categories").then(res => res.json()),
  createCategory: (data: any) => apiRequest("POST", "/api/categories", data),
  updateCategory: (id: number, data: any) => apiRequest("PUT", `/api/categories/${id}`, data),
  
  // Emails
  getEmails: (params?: { search?: string; category?: string }) => {
    const url = new URL("/api/emails", window.location.origin);
    if (params?.search) url.searchParams.set("search", params.search);
    if (params?.category) url.searchParams.set("category", params.category);
    return fetch(url.toString()).then(res => res.json());
  },
  getEmail: (id: number) => fetch(`/api/emails/${id}`).then(res => res.json()),
  createEmail: (data: any) => apiRequest("POST", "/api/emails", data),
  updateEmail: (id: number, data: any) => apiRequest("PUT", `/api/emails/${id}`, data),
  
  // Activities
  getActivities: (limit?: number) => {
    const url = new URL("/api/activities", window.location.origin);
    if (limit) url.searchParams.set("limit", limit.toString());
    return fetch(url.toString()).then(res => res.json());
  },
  
  // Gmail sync
  syncGmail: () => apiRequest("POST", "/api/gmail/sync"),
  
  // AI categorization
  categorizeEmail: (emailId: number, categoryId: number, confidence?: number) => 
    apiRequest("POST", "/api/ai/categorize", { emailId, categoryId, confidence }),
};
