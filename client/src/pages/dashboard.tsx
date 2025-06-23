import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "@/components/sidebar";
// import { StatsCards } from "@/components/stats-cards"; // Removed
// import { CategoryOverview } from "@/components/category-overview"; // Removed
// import { RecentActivity } from "@/components/recent-activity"; // Removed
import { EmailList } from "@/components/email-list";
import { AIAnalysisPanel } from "@/components/ai-analysis-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
// Filtered lucide-react imports: Brain, Zap, BarChart3, Bell, Settings removed
import { Search, FolderSync } from "lucide-react";
import { useState } from "react";
import type { DashboardStats, Category, EmailWithCategory, Activity } from "@shared/schema";

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("");
  const [syncLoading, setSyncLoading] = useState(false);
  // const [batchProcessing, setBatchProcessing] = useState(false); // Removed
  const [selectedEmail, setSelectedEmail] = useState<EmailWithCategory | null>(null);
  const { toast } = useToast();

  // const { data: stats, isLoading: statsLoading } = useQuery<DashboardStats>({ // Removed
  //   queryKey: ["/api/dashboard/stats"], // Removed
  // }); // Removed

  const { data: categories = [], isLoading: categoriesLoading } = useQuery<Category[]>({
    queryKey: ["/api/categories"],
  });

  const { data: emails = [], isLoading: emailsLoading, refetch: refetchEmails } = useQuery<EmailWithCategory[]>({
    queryKey: ["/api/emails", searchQuery ? { search: searchQuery } : {}],
  });

  // const { data: activities = [] } = useQuery<Activity[]>({ // Removed
  //   queryKey: ["/api/activities"], // Removed
  // }); // Removed

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

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // The query will automatically trigger refetch due to dependency
  };

  // const handleBatchAnalysis = async () => { // Removed
  //   setBatchProcessing(true); // Removed
  //   try { // Removed
  //     const emailIds = emails.slice(0, 5).map(email => email.id); // Process first 5 emails // Removed
  //     const response = await fetch('/api/ai/batch-analyze', { // Removed
  //       method: 'POST', // Removed
  //       headers: { // Removed
  //         'Content-Type': 'application/json', // Removed
  //       }, // Removed
  //       body: JSON.stringify({ emailIds }), // Removed
  //     }); // Removed
      
  //     if (response.ok) { // Removed
  //       const result = await response.json(); // Removed
  //       toast({ // Removed
  //         title: "Batch Analysis Complete", // Removed
  //         description: `${result.summary.successful}/${result.summary.total} emails analyzed successfully`, // Removed
  //       }); // Removed
  //       refetchEmails(); // Removed
  //     } else { // Removed
  //       throw new Error('Batch analysis failed'); // Removed
  //     } // Removed
  //   } catch (error) { // Removed
  //     toast({ // Removed
  //       title: "Batch Analysis Failed", // Removed
  //       description: "Unable to perform batch analysis", // Removed
  //       variant: "destructive", // Removed
  //     }); // Removed
  //   } finally { // Removed
  //     setBatchProcessing(false); // Removed
  //   } // Removed
  // }; // Removed

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
              {/* Connection Status */}
              <Badge variant="secondary" className="bg-green-50 text-green-700 hover:bg-green-50">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Gmail Connected
              </Badge>
              
              {/* Notification */}
              {/* Removed Bell Icon Button */}

              {/* Profile */}
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span className="text-white font-medium text-sm">JD</span>
                </div>
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

          {/* Stats Cards */}
          {/* <StatsCards stats={stats} loading={statsLoading} /> */} {/* Removed */}

          {/* AI Control Panel */}
          {/* Entire AI Control Panel Card removed as its content became empty */}

          {/* Main Dashboard Grid - Placeholders for CategoryOverview and RecentActivity removed */}
          {/* This section can be repurposed or filled with other components if needed */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
            <div className="lg:col-span-2">
              {/* This space was for CategoryOverview */}
              <Card>
                <CardHeader><CardTitle>Data Overview</CardTitle></CardHeader>
                <CardContent><p>Placeholder for future data visualizations.</p></CardContent>
              </Card>
            </div>
            <div>
              {/* This space was for RecentActivity */}
              <Card>
                <CardHeader><CardTitle>Quick Links</CardTitle></CardHeader>
                <CardContent><p>Placeholder for future quick links or actions.</p></CardContent>
              </Card>
            </div>
          </div>

          {/* Recent Emails & AI Analysis Section - Two Column Layout */}
          <div className="mt-8 flex gap-6">
            {/* Left Column: Email List */}
            <div className="w-1/2 bg-white rounded-lg shadow-sm border border-gray-200 flex flex-col">
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
              <div className="flex-grow overflow-auto"> {/* Added for scrollability if list is long */}
                <EmailList
                  emails={emails}
                  loading={emailsLoading}
                  onEmailSelect={setSelectedEmail}
                />
              </div>
            </div>

            {/* Right Column: AI Analysis Panel */}
            <div className="w-1/2">
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
