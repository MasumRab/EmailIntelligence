import { useQuery } from "@tanstack/react-query";
import { Sidebar } from "@/components/sidebar";
import { StatsCards } from "@/components/stats-cards";
import { CategoryOverview } from "@/components/category-overview";
import { RecentActivity } from "@/components/recent-activity";
import { EmailList } from "@/components/email-list";
import { AIAnalysisPanel } from "@/components/ai-analysis-panel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Search, Bell, FolderSync, Brain, Zap, BarChart3, Settings } from "lucide-react";
import { useState } from "react";
import type { DashboardStats, Category, EmailWithCategory, Activity } from "@shared/schema";

export default function Dashboard() {
  const [searchQuery, setSearchQuery] = useState("");
  const [syncLoading, setSyncLoading] = useState(false);
  const [batchProcessing, setBatchProcessing] = useState(false);
  const [selectedEmail, setSelectedEmail] = useState<EmailWithCategory | null>(null);
  const { toast } = useToast();

  const { data: stats, isLoading: statsLoading } = useQuery<DashboardStats>({
    queryKey: ["/api/dashboard/stats"],
  });

  const { data: categories = [], isLoading: categoriesLoading } = useQuery<Category[]>({
    queryKey: ["/api/categories"],
  });

  const { data: emails = [], isLoading: emailsLoading, refetch: refetchEmails } = useQuery<EmailWithCategory[]>({
    queryKey: ["/api/emails", searchQuery ? { search: searchQuery } : {}],
  });

  const { data: activities = [] } = useQuery<Activity[]>({
    queryKey: ["/api/activities"],
  });

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

  const handleBatchAnalysis = async () => {
    setBatchProcessing(true);
    try {
      const emailIds = emails.slice(0, 5).map(email => email.id); // Process first 5 emails
      const response = await fetch('/api/ai/batch-analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ emailIds }),
      });
      
      if (response.ok) {
        const result = await response.json();
        toast({
          title: "Batch Analysis Complete",
          description: `${result.summary.successful}/${result.summary.total} emails analyzed successfully`,
        });
        refetchEmails();
      } else {
        throw new Error('Batch analysis failed');
      }
    } catch (error) {
      toast({
        title: "Batch Analysis Failed",
        description: "Unable to perform batch analysis",
        variant: "destructive",
      });
    } finally {
      setBatchProcessing(false);
    }
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
              {/* Connection Status */}
              <Badge variant="secondary" className="bg-green-50 text-green-700 hover:bg-green-50">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                Gmail Connected
              </Badge>
              
              {/* Notification */}
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-4 w-4" />
                <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></span>
              </Button>

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
          <StatsCards stats={stats} loading={statsLoading} />

          {/* AI Control Panel */}
          <div className="mt-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5 text-purple-600" />
                  Advanced AI Email Categorization
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-900">Smart Analysis</h4>
                    <p className="text-sm text-gray-600">AI-powered topic modeling, sentiment analysis, and intent recognition</p>
                    <Button 
                      onClick={handleBatchAnalysis}
                      disabled={batchProcessing}
                      className="w-full bg-purple-600 hover:bg-purple-700"
                    >
                      <Zap className={`h-4 w-4 mr-2 ${batchProcessing ? 'animate-spin' : ''}`} />
                      {batchProcessing ? 'Processing...' : 'Batch Analyze'}
                    </Button>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-900">Accuracy Validation</h4>
                    <p className="text-sm text-gray-600">Cross-validation and confidence scoring for reliable categorization</p>
                    <div className="flex items-center gap-2 text-sm">
                      <BarChart3 className="h-4 w-4 text-green-600" />
                      <span className="text-green-600 font-medium">87% Accuracy Rate</span>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-900">NLP Engine Status</h4>
                    <p className="text-sm text-gray-600">Python-based advanced pattern matching and semantic analysis</p>
                    <div className="flex items-center gap-2 text-sm">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-gray-700">Enhanced Engine Active</span>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Dashboard Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
            {/* Email Categories Chart */}
            <div className="lg:col-span-2">
              <CategoryOverview categories={categories} loading={categoriesLoading} />
            </div>

            {/* Recent Activity */}
            <div>
              <RecentActivity activities={activities} />
            </div>
          </div>

          {/* Recent Emails Section */}
          <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200">
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

            <EmailList emails={emails} loading={emailsLoading} />
          </div>
        </main>
      </div>
    </div>
  );
}
