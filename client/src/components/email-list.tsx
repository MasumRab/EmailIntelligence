import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Brain, Star } from "lucide-react";
import type { EmailWithCategory } from "@shared/schema";

interface EmailListProps {
  emails: EmailWithCategory[];
  loading: boolean;
}

export function EmailList({ emails, loading }: EmailListProps) {
  if (loading) {
    return (
      <div className="divide-y divide-gray-200">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="p-4">
            <div className="flex items-center space-x-4">
              <Skeleton className="w-10 h-10 rounded-full" />
              <div className="flex-1 space-y-2">
                <div className="flex items-center justify-between">
                  <Skeleton className="h-4 w-24" />
                  <Skeleton className="h-3 w-16" />
                </div>
                <Skeleton className="h-4 w-64" />
                <Skeleton className="h-3 w-80" />
                <div className="flex items-center space-x-2">
                  <Skeleton className="h-5 w-20 rounded-full" />
                  <Skeleton className="h-5 w-16 rounded-full" />
                  <Skeleton className="h-3 w-24" />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const getInitials = (name: string) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };

  const getCategoryBadgeColor = (categoryName?: string) => {
    if (!categoryName) return "bg-gray-100 text-gray-800";
    
    switch (categoryName.toLowerCase()) {
      case "work & business": return "bg-green-100 text-green-800";
      case "personal & family": return "bg-blue-100 text-blue-800";
      case "finance & banking": return "bg-yellow-100 text-yellow-800";
      case "promotions & marketing": return "bg-red-100 text-red-800";
      case "travel": return "bg-purple-100 text-purple-800";
      case "healthcare": return "bg-cyan-100 text-cyan-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const handleEmailClick = (email: EmailWithCategory) => {
    // In a real app, this would open the email detail view or redirect to Gmail
    console.log("Opening email:", email.subject);
  };

  if (emails.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        <p>No emails found</p>
      </div>
    );
  }

  return (
    <>
      <div className="divide-y divide-gray-200">
        {emails.map((email) => (
          <div 
            key={email.id} 
            className="p-4 hover:bg-gray-50 transition-colors cursor-pointer"
            onClick={() => handleEmailClick(email)}
          >
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                  <span className="text-sm font-medium text-gray-600">
                    {getInitials(email.sender)}
                  </span>
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {email.sender}
                    </p>
                    {email.isStarred && (
                      <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    )}
                  </div>
                  <p className="text-xs text-gray-500">{email.time}</p>
                </div>
                <p className="text-sm text-gray-900 truncate mt-1">
                  {email.subject}
                </p>
                <p className="text-xs text-gray-600 truncate mt-1">
                  {email.preview}
                </p>
                <div className="flex items-center space-x-2 mt-2">
                  {email.category && (
                    <Badge 
                      variant="secondary" 
                      className={`text-xs ${getCategoryBadgeColor(email.category.name)}`}
                    >
                      {email.category.name}
                    </Badge>
                  )}
                  {email.labels?.map((label, index) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {label}
                    </Badge>
                  ))}
                  {email.confidence && (
                    <span className="text-xs text-gray-500 flex items-center">
                      <Brain className="h-3 w-3 mr-1" />
                      {email.confidence}% confidence
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-gray-200 text-center">
        <Button variant="ghost" className="text-blue-600 hover:text-blue-700">
          Load More Emails
        </Button>
      </div>
    </>
  );
}
