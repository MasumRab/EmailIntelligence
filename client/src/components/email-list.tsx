/**
 * @file This file contains the EmailList component, which is responsible for
 *       rendering a list of emails, including their loading and empty states.
 */
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { Brain, Star } from "lucide-react";
import type { EmailWithCategory } from "@shared/schema";
import { memo } from "react";

/**
 * @interface EmailListProps
 * @description Defines the props for the EmailList component.
 * @property {EmailWithCategory[]} emails - An array of email objects to display.
 * @property {boolean} loading - A flag to indicate if the component is in a loading state.
 * @property {(email: EmailWithCategory) => void} onEmailSelect - A callback function to handle email selection.
 */
interface EmailListProps {
  emails: EmailWithCategory[];
  loading: boolean;
  onEmailSelect: (email: EmailWithCategory) => void;
}

/**
 * Generates initials from a given name.
 * @param {string} name - The full name of the sender.
 * @returns {string} The initials of the sender.
 */
const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase();
};

/**
 * Determines the badge color based on the category name.
 * @param {string} [categoryName] - The name of the category.
 * @returns {string} The Tailwind CSS classes for the badge color.
 */
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

/**
 * Renders a list of emails with sender details, subject, preview, and associated badges.
 *
 * This component handles the display of emails, providing visual feedback for loading
 * states and a message for when no emails are available. Each email is interactive,
 * triggering a callback on selection.
 *
 * @param {EmailListProps} props - The props for the component.
 * @returns {JSX.Element} The rendered list of emails, or a loading/empty state.
 *
 * Bolt Optimization: Wrapped in React.memo to prevent unnecessary re-renders
 * when parent state changes (e.g. search input typing) but email list data hasn't updated.
 */
export const EmailList = memo(function EmailList({ emails, loading, onEmailSelect }: EmailListProps) {
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
            onClick={() => onEmailSelect(email)}
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
                  {email.categoryData && (
                    <Badge 
                      variant="secondary" 
                      className={`text-xs ${getCategoryBadgeColor(email.categoryData.name)}`}
                    >
                      {email.categoryData.name}
                    </Badge>
                  )}
                  {email.labels?.map((label: string, index: number) => (
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
});
