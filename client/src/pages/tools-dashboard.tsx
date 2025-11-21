/**
 * @file Tools Dashboard component for accessing scripts and isolated tools.
 */
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { useToast } from "@/hooks/use-toast";
import {
  Wrench,
  Play,
  CheckCircle,
  XCircle,
  AlertCircle,
  Clock,
  Activity,
  Shield,
  Code,
  Database,
  FileText,
  Settings
} from "lucide-react";
import { useState } from "react";

interface ToolStatus {
  name: string;
  category: string;
  status: string;
  description: string;
  last_run?: string;
  health_check?: string;
}

interface ToolsDashboardResponse {
  tools: ToolStatus[];
  categories: string[];
  system_health: {
    total_tools: number;
    healthy_tools: number;
    categories: string[];
    last_updated: string;
  };
}

interface ScriptExecutionRequest {
  script_name: string;
  args?: string[];
  working_directory?: string;
}

interface ScriptExecutionResponse {
  script_name: string;
  status: string;
  output?: string;
  error?: string;
  execution_time?: number;
  timestamp: string;
}

/**
 * Tools Dashboard component for accessing and managing scripts and tools.
 */
export default function ToolsDashboard() {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const [executionResults, setExecutionResults] = useState<ScriptExecutionResponse[]>([]);

  const { data: dashboardData, isLoading, error } = useQuery<ToolsDashboardResponse>({
    queryKey: ["/api/tools/dashboard"],
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  const executeScriptMutation = useMutation<
    ScriptExecutionResponse,
    Error,
    ScriptExecutionRequest
  >({
    mutationFn: async (request) => {
      const response = await fetch("/api/tools/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.json();
    },
    onSuccess: (result) => {
      setExecutionResults(prev => [result, ...prev.slice(0, 9)]); // Keep last 10 results
      queryClient.invalidateQueries({ queryKey: ["/api/tools/dashboard"] });

      if (result.status === "success") {
        toast({
          title: "Script executed successfully",
          description: `${result.script_name} completed in ${result.execution_time?.toFixed(2)}s`,
        });
      } else {
        toast({
          title: "Script execution failed",
          description: result.error || "Unknown error occurred",
          variant: "destructive",
        });
      }
    },
    onError: (error) => {
      toast({
        title: "Execution failed",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleExecuteScript = (toolName: string) => {
    executeScriptMutation.mutate({
      script_name: toolName,
    });
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy":
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case "error":
        return <XCircle className="h-4 w-4 text-red-500" />;
      case "not_found":
        return <XCircle className="h-4 w-4 text-gray-500" />;
      case "not_executable":
        return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case "import_error":
        return <XCircle className="h-4 w-4 text-orange-500" />;
      default:
        return <Clock className="h-4 w-4 text-blue-500" />;
    }
  };

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case "healthy":
        return "default";
      case "error":
      case "not_found":
      case "not_executable":
      case "import_error":
        return "destructive";
      default:
        return "secondary";
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category.toLowerCase()) {
      case "context control":
        return <Shield className="h-4 w-4" />;
      case "monitoring":
        return <Activity className="h-4 w-4" />;
      case "analysis":
        return <Code className="h-4 w-4" />;
      case "validation":
        return <CheckCircle className="h-4 w-4" />;
      case "task management":
        return <Settings className="h-4 w-4" />;
      case "maintenance":
        return <Wrench className="h-4 w-4" />;
      case "documentation":
        return <FileText className="h-4 w-4" />;
      default:
        return <Database className="h-4 w-4" />;
    }
  };

  const getToolsByCategory = (category: string) => {
    return dashboardData?.tools.filter(tool => tool.category === category) || [];
  };

  if (isLoading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
            <p className="mt-2 text-muted-foreground">Loading tools dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6">
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load tools dashboard: {error.message}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const systemHealth = dashboardData?.system_health;
  const categories = dashboardData?.categories || [];

  return (
    <div className="container mx-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">Tools Dashboard</h1>
          <p className="text-muted-foreground">
            Access and manage isolated scripts and tools
          </p>
        </div>
      </div>

      {/* System Health Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tools</CardTitle>
            <Wrench className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{systemHealth?.total_tools || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Healthy Tools</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {systemHealth?.healthy_tools || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Categories</CardTitle>
            <Settings className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{categories.length}</div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue={categories[0] || "all"} className="w-full">
        <TabsList className="grid w-full grid-cols-4 lg:grid-cols-8">
          {categories.map((category) => (
            <TabsTrigger key={category} value={category} className="text-xs">
              {category}
            </TabsTrigger>
          ))}
        </TabsList>

        {categories.map((category) => (
          <TabsContent key={category} value={category}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {getToolsByCategory(category).map((tool) => (
                <Card key={tool.name}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {getCategoryIcon(tool.category)}
                        <CardTitle className="text-sm">{tool.name}</CardTitle>
                      </div>
                      <Badge variant={getStatusBadgeVariant(tool.status)}>
                        {getStatusIcon(tool.status)}
                        <span className="ml-1">{tool.status}</span>
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4">
                      {tool.description}
                    </p>
                    <Button
                      onClick={() => handleExecuteScript(tool.name)}
                      disabled={executeScriptMutation.isPending}
                      className="w-full"
                      size="sm"
                    >
                      {executeScriptMutation.isPending ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Running...
                        </>
                      ) : (
                        <>
                          <Play className="h-4 w-4 mr-2" />
                          Execute
                        </>
                      )}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        ))}
      </Tabs>

      {/* Execution Results */}
      {executionResults.length > 0 && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Activity className="h-5 w-5 mr-2" />
              Recent Executions
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {executionResults.map((result, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      {result.status === "success" ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-500" />
                      )}
                      <span className="font-medium">{result.script_name}</span>
                    </div>
                    <div className="text-sm text-muted-foreground">
                      {result.execution_time?.toFixed(2)}s
                    </div>
                  </div>

                  {result.output && (
                    <div className="bg-green-50 dark:bg-green-950 p-2 rounded text-sm font-mono mb-2">
                      <div className="text-green-800 dark:text-green-200">
                        {result.output.split('\n').slice(0, 5).join('\n')}
                        {result.output.split('\n').length > 5 && '...'}
                      </div>
                    </div>
                  )}

                  {result.error && (
                    <div className="bg-red-50 dark:bg-red-950 p-2 rounded text-sm font-mono">
                      <div className="text-red-800 dark:text-red-200">
                        {result.error.split('\n').slice(0, 5).join('\n')}
                        {result.error.split('\n').length > 5 && '...'}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}