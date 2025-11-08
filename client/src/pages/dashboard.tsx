/**
 * @file This file contains the main Dashboard component, which serves as the
 *       primary user interface for the email client application.
 */
import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "@/components/sidebar";
import { EmailList } from "@/components/email-list";
import { AIAnalysisPanel } from "@/components/ai-analysis-panel";
import { AdvancedFilterPanel } from "@/components/advanced-filter-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Search, FolderSync, Filter } from "lucide-react";
import { useState } from "react";
import type { Category, EmailWithCategory } from "@shared/schema";

/**
 * The main dashboard component for the application.
 *
 * This component orchestrates the entire user interface, including the sidebar,
 * email list, and AI analysis panel. It manages state for the search query,
 * synchronization status, and the currently selected email. It also handles
 * data fetching for emails and categories using React Query.
 *
 * @returns {JSX.Element} The rendered dashboard page.
 */
export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("");
  const [syncLoading, setSyncLoading] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState<EmailWithCategory | null>(null);
  const { toast } = useToast();

  const { data: categories = [] } = useQuery<Category[]>({
    queryKey: ["/api/categories"],
  });

  const { data: emails = [], isLoading: emailsLoading, refetch: refetchEmails } = useQuery<EmailWithCategory[]>({
    queryKey: ["/api/emails", searchQuery ? { search: searchQuery } : {}],
  });

  /**
   * Handles the synchronization of emails with the Gmail server.
   * @async
   */
  const handleSync = async () => {
    setSyncLoading(true);
    try {
      const response = await fetch("/api/gmail/sync", {
        method: "POST",
        credentials: "include",
      });

      if (response.ok) {
        const result = await response.json();
        toast({
          title: "FolderSync Complete",
          description: `${result.synced} new emails processed`,
        });
        refetchEmails();
      } else {
        throw new Error("FolderSync failed");
      }
    } catch (error) {
      toast({
        title: "FolderSync Failed",
        description: "Unable to sync with Gmail",
        variant: "destructive",
      });
    } finally {
      setSyncLoading(false);
    }
  };

  /**
   * Handles the form submission for searching emails.
   * @param {React.FormEvent} e - The form event.
   */
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // The query will automatically trigger refetch due to dependency in useQuery
  };

  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [activeFilters, setActiveFilters] = useState<any>(null);

  const handleApplyFilters = (filters: any) => {
    setActiveFilters(filters);
    // In a real implementation, you would apply these filters to your email query
    console.log("Applying filters:", filters);
    setShowAdvancedFilters(false); // Close the filter panel after applying
  };

  return (
    <div className="flex h-screen overflow-hidden bg-gmail-bg">
      <Sidebar categories={categories} />

      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Search Bar */}
            <div className="flex-1 max-w-2xl">
              <form onSubmit={handleSearch} className="relative">
                <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                <Input
                  type="search"
                  placeholder="Search emails..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </form>
            </div>

            {/* User Actions */}
            <div className="flex items-center space-x-4">
              {/* Advanced Filters Button */}
              <Button
                variant="outline"
                onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                className="flex items-center"
              >
                <Filter className="h-4 w-4 mr-2" />
                Advanced Filters
              </Button>

              {/* Connection Status */}
              <Badge variant="secondary" className="bg-green-50 text-green-700 hover:bg-green-50">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Gmail Connected
              </Badge>

              {/* Profile */}
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-medium text-sm">JD</span>
                </div>
                <span className="text-gray-700">John Doe</span>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-auto p-6">
          {/* Dashboard Header */}
          <div className="mb-8">
            <h1 className="text-2xl font-semibold text-gray-900 mb-2">
              AI Email Analytics Dashboard
            </h1>
            <p className="text-gray-600">
              Intelligent email organization powered by advanced NLP analysis
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
            <div className="lg:col-span-2">
              <Card>
                <CardHeader><CardTitle>Data Overview</CardTitle></CardHeader>
                <CardContent><p>Placeholder for future data visualizations.</p></CardContent>
              </Card>
            </div>
            <div>
              <Card>
                <CardHeader><CardTitle>Quick Links</CardTitle></CardHeader>
                <CardContent><p>Placeholder for future quick links or actions.</p></CardContent>
              </Card>
            </div>
          </div>

          {/* Filter Panel and Email List Section */}
          <div className="mt-8 flex gap-6">
            {/* Left Column: Advanced Filter Panel and Email List */}
            <div className="w-2/3 flex flex-col gap-6">
              {showAdvancedFilters && (
                <AdvancedFilterPanel
                  categories={categories}
                  onApplyFilters={handleApplyFilters}
                />
              )}

              <div className="bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col">
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-medium text-gray-900">
                      Recently Categorized Emails
                    </h3>
                    <div className="flex items-center space-x-2">
                      <Button
                        onClick={handleSync}
                        disabled={syncLoading}
                        className="bg-blue-500 text-white hover:bg-blue-600"
                      >
                        <FolderSync className={`mr-2 h-4 w-4 ${syncLoading ? 'animate-spin' : ''}`} />
                        {syncLoading ? 'Syncing...' : 'FolderSync Now'}
                      </Button>
                      <Button variant="outline">
                        View Inbox
                      </Button>
                    </div>
                  </div>
                </div>
                <div className="flex-grow overflow-auto">
                  <EmailList
                    emails={emails}
                    loading={emailsLoading}
                    onEmailSelect={setSelectedEmail}
                  />
                </div>
              </div>
            </div>

            {/* Right Column: AI Analysis Panel */}
            <div className="w-1/3">
              {selectedEmail ? (
                <AIAnalysisPanel email={selectedEmail} />
              ) : (
                <Card className="h-full flex items-center justify-center">
                  <CardContent>
                    <p className="text-center text-gray-500">
                      Select an email to see AI analysis.
                    </p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}