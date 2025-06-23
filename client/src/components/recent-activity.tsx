import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { formatDistanceToNow } from "date-fns";
import type { Activity } from "@shared/schema";

interface RecentActivityProps {
  activities: Activity[];
}

export function RecentActivity({ activities }: RecentActivityProps) {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case "label": return "🏷️";
      case "category": return "🧠";
      case "sync": return "🔄";
      case "review": return "⚠️";
      default: return "📧";
    }
  };

  const getActivityBadgeColor = (type: string) => {
    switch (type) {
      case "label": return "bg-green-50 text-green-700";
      case "category": return "bg-blue-50 text-blue-700";
      case "sync": return "bg-purple-50 text-purple-700";
      case "review": return "bg-yellow-50 text-yellow-700";
      default: return "bg-gray-50 text-gray-700";
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-lg font-medium text-gray-900">Recent AI Activity</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.slice(0, 6).map((activity) => (
            <div key={activity.id} className="flex items-start space-x-3">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${getActivityBadgeColor(activity.type)}`}>
                <span className="text-xs">{getActivityIcon(activity.type)}</span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">{activity.description}</p>
                {activity.details && (
                  <p className="text-xs text-gray-600">{activity.details}</p>
                )}
                <p className="text-xs text-gray-500 mt-1">
                  {formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })}
                </p>
              </div>
            </div>
          ))}
        </div>

        <Button variant="ghost" className="w-full mt-4 text-blue-600 hover:text-blue-700">
          View All Activity
        </Button>
      </CardContent>
    </Card>
  );
}
