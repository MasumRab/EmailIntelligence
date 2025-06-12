import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Progress } from "@/components/ui/progress";
import { useToast } from "@/hooks/use-toast";
import { 
  Brain, 
  CheckCircle, 
  AlertTriangle, 
  TrendingUp, 
  Zap, 
  Target,
  Eye,
  ThumbsUp,
  ThumbsDown,
  RotateCcw
} from "lucide-react";
import type { EmailWithCategory } from "@shared/schema";

interface AIAnalysis {
  topic: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  intent: string;
  urgency: 'low' | 'medium' | 'high' | 'critical';
  confidence: number;
  categories: string[];
  keywords: string[];
  reasoning: string;
  suggested_labels: string[];
  risk_flags: string[];
  validation: {
    validation_method: string;
    score: number;
    reliable: boolean;
    feedback: string;
  };
}

interface AIAnalysisPanelProps {
  email: EmailWithCategory;
  onCategoryUpdate?: (email: EmailWithCategory) => void;
}

export function AIAnalysisPanel({ email, onCategoryUpdate }: AIAnalysisPanelProps) {
  const [analysis, setAnalysis] = useState<AIAnalysis | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const { toast } = useToast();

  const analyzeEmail = async () => {
    setIsAnalyzing(true);
    try {
      const response = await fetch('/api/ai/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subject: email.subject,
          content: email.content
        }),
      });

      if (response.ok) {
        const result = await response.json();
        setAnalysis(result);
        setShowDetails(true);
        
        toast({
          title: "AI Analysis Complete",
          description: `Analysis completed with ${Math.round(result.confidence * 100)}% confidence`,
        });
      } else {
        throw new Error('Analysis failed');
      }
    } catch (error) {
      toast({
        title: "Analysis Failed",
        description: "Unable to analyze email with AI",
        variant: "destructive",
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const applyCategorization = async () => {
    if (!analysis) return;

    try {
      const response = await fetch('/api/ai/categorize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          emailId: email.id,
          autoAnalyze: true
        }),
      });

      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          toast({
            title: "Categorization Applied",
            description: `Email categorized as "${result.categoryAssigned}"`,
          });
          if (onCategoryUpdate && result.email) {
            onCategoryUpdate(result.email);
          }
        } else {
          toast({
            title: "Category Suggestion",
            description: result.message,
            variant: "default",
          });
        }
      } else {
        throw new Error('Categorization failed');
      }
    } catch (error) {
      toast({
        title: "Categorization Failed",
        description: "Unable to apply AI categorization",
        variant: "destructive",
      });
    }
  };

  const provideFeedback = async (feedback: 'correct' | 'incorrect') => {
    try {
      const response = await fetch('/api/ai/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          emailId: email.id,
          userFeedback: feedback
        }),
      });

      if (response.ok) {
        toast({
          title: "Feedback Recorded",
          description: "Thank you for helping improve AI accuracy",
        });
      }
    } catch (error) {
      toast({
        title: "Feedback Failed",
        description: "Unable to record feedback",
        variant: "destructive",
      });
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-50';
      case 'negative': return 'text-red-600 bg-red-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'critical': return 'text-red-600 bg-red-50';
      case 'high': return 'text-orange-600 bg-orange-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence > 0.8) return 'text-green-600';
    if (confidence > 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Brain className="h-5 w-5 text-blue-600" />
            AI Email Analysis
          </CardTitle>
          <div className="flex gap-2">
            <Button
              onClick={analyzeEmail}
              disabled={isAnalyzing}
              size="sm"
              variant="outline"
            >
              <Zap className={`h-4 w-4 mr-2 ${isAnalyzing ? 'animate-spin' : ''}`} />
              {isAnalyzing ? 'Analyzing...' : 'Analyze'}
            </Button>
            {analysis && (
              <Button
                onClick={() => setShowDetails(!showDetails)}
                size="sm"
                variant="ghost"
              >
                <Eye className="h-4 w-4 mr-2" />
                {showDetails ? 'Hide' : 'Show'} Details
              </Button>
            )}
          </div>
        </div>
      </CardHeader>

      {analysis && (
        <CardContent className="space-y-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Confidence</div>
              <div className={`text-lg font-semibold ${getConfidenceColor(analysis.confidence)}`}>
                {Math.round(analysis.confidence * 100)}%
              </div>
              <Progress 
                value={analysis.confidence * 100} 
                className="h-2 mt-1"
              />
            </div>

            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Sentiment</div>
              <Badge className={getSentimentColor(analysis.sentiment)}>
                {analysis.sentiment}
              </Badge>
            </div>

            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Urgency</div>
              <Badge className={getUrgencyColor(analysis.urgency)}>
                {analysis.urgency}
              </Badge>
            </div>

            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-sm text-gray-600">Reliability</div>
              <div className="flex items-center justify-center gap-1">
                {analysis.validation.reliable ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <AlertTriangle className="h-4 w-4 text-yellow-600" />
                )}
                <span className="text-sm font-medium">
                  {analysis.validation.reliable ? 'High' : 'Low'}
                </span>
              </div>
            </div>
          </div>

          {/* Categories */}
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Suggested Categories</h4>
            <div className="flex flex-wrap gap-2">
              {analysis.categories.map((category, index) => (
                <Badge key={index} variant="secondary" className="bg-blue-50 text-blue-700">
                  {category}
                </Badge>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-2">
            <Button 
              onClick={applyCategorization}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <Target className="h-4 w-4 mr-2" />
              Apply Categorization
            </Button>
            
            <div className="flex gap-1">
              <Button
                onClick={() => provideFeedback('correct')}
                size="sm"
                variant="outline"
                className="text-green-600 hover:bg-green-50"
              >
                <ThumbsUp className="h-4 w-4" />
              </Button>
              <Button
                onClick={() => provideFeedback('incorrect')}
                size="sm"
                variant="outline"
                className="text-red-600 hover:bg-red-50"
              >
                <ThumbsDown className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Detailed Analysis */}
          {showDetails && (
            <>
              <Separator />
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Topic & Intent</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="text-sm text-gray-600">Topic:</span>
                      <p className="font-medium">{analysis.topic}</p>
                    </div>
                    <div>
                      <span className="text-sm text-gray-600">Intent:</span>
                      <p className="font-medium">{analysis.intent.replace('_', ' ')}</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Keywords</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.keywords.map((keyword, index) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {keyword}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Suggested Labels</h4>
                  <div className="flex flex-wrap gap-2">
                    {analysis.suggested_labels.map((label, index) => (
                      <Badge key={index} className="bg-purple-50 text-purple-700">
                        {label}
                      </Badge>
                    ))}
                  </div>
                </div>

                {analysis.risk_flags.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2 flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 text-orange-500" />
                      Risk Flags
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {analysis.risk_flags.map((flag, index) => (
                        <Badge key={index} className="bg-orange-50 text-orange-700">
                          {flag.replace('_', ' ')}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Analysis Reasoning</h4>
                  <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg">
                    {analysis.reasoning}
                  </p>
                </div>

                <div>
                  <h4 className="font-medium text-gray-900 mb-2">Validation Details</h4>
                  <div className="bg-gray-50 p-3 rounded-lg space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Method:</span>
                      <span className="font-medium">{analysis.validation.validation_method}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Score:</span>
                      <span className="font-medium">{(analysis.validation.score * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-xs text-gray-600 mt-2">
                      {analysis.validation.feedback}
                    </p>
                  </div>
                </div>
              </div>
            </>
          )}
        </CardContent>
      )}

      {!analysis && !isAnalyzing && (
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            <Brain className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>Click "Analyze" to get AI-powered insights about this email</p>
            <div className="mt-4 text-sm space-y-1">
              <p>• Advanced sentiment and intent detection</p>
              <p>• Smart categorization with confidence scores</p>
              <p>• Accuracy validation and feedback learning</p>
            </div>
          </div>
        </CardContent>
      )}
    </Card>
  );
}