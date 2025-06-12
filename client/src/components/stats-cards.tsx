import { Card, CardContent } from "@/components/ui/card";
import { Mail, Tag, Brain, Clock } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import type { DashboardStats } from "@shared/schema";

interface StatsCardsProps {
  stats?: DashboardStats;
  loading: boolean;
}

export function StatsCards({ stats, loading }: StatsCardsProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[...Array(4)].map((_, i) => (
          <Card key={i}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <Skeleton className="h-4 w-24" />
                  <Skeleton className="h-8 w-16" />
                </div>
                <Skeleton className="w-12 h-12 rounded-full" />
              </div>
              <div className="mt-4">
                <Skeleton className="h-4 w-20" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!stats) return null;

  const statsData = [
    {
      title: "Total Emails Analyzed",
      value: stats.totalEmails.toLocaleString(),
      icon: Mail,
      iconBg: "bg-blue-50",
      iconColor: "text-blue-600",
      change: `↑ ${stats.weeklyGrowth.totalEmails}%`,
      changeText: "from last week",
      changeColor: "text-green-600",
    },
    {
      title: "Auto-Labeled",
      value: stats.autoLabeled.toLocaleString(),
      icon: Tag,
      iconBg: "bg-green-50",
      iconColor: "text-green-600",
      change: `↑ ${stats.weeklyGrowth.autoLabeled}%`,
      changeText: "accuracy rate",
      changeColor: "text-green-600",
    },
    {
      title: "Categories Created",
      value: stats.categories.toString(),
      icon: Brain,
      iconBg: "bg-purple-50",
      iconColor: "text-purple-600",
      change: `+${stats.weeklyGrowth.categories}`,
      changeText: "this week",
      changeColor: "text-green-600",
    },
    {
      title: "Time Saved",
      value: stats.timeSaved,
      icon: Clock,
      iconBg: "bg-yellow-50",
      iconColor: "text-yellow-600",
      change: `↑ ${stats.weeklyGrowth.timeSaved}%`,
      changeText: "this month",
      changeColor: "text-green-600",
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {statsData.map((stat, index) => {
        const Icon = stat.icon;
        return (
          <Card key={index} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 text-sm font-medium">{stat.title}</p>
                  <p className="text-2xl font-semibold text-gray-900 mt-1">{stat.value}</p>
                </div>
                <div className={`w-12 h-12 ${stat.iconBg} rounded-full flex items-center justify-center`}>
                  <Icon className={`h-6 w-6 ${stat.iconColor}`} />
                </div>
              </div>
              <div className="mt-4 flex items-center text-sm">
                <span className={stat.changeColor}>{stat.change}</span>
                <span className="text-gray-600 ml-1">{stat.changeText}</span>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
