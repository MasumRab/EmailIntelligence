/**
 * @file This file contains the Sidebar component, which serves as the main
 *       navigation panel for the application.
 */
import { Link, useLocation } from "wouter";
import {
  LayoutDashboard,
  Inbox,
  Star,
  Send,
  Trash2,
  Settings,
  Brain,
  Mail,
  Wrench
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { Category } from "@shared/schema";

/**
 * @interface SidebarProps
 * @description Defines the props for the Sidebar component.
 * @property {Category[]} categories - An array of category objects to be displayed.
 */
interface SidebarProps {
  categories: Category[];
}

/**
 * A React component that renders the main navigation sidebar.
 *
 * This component displays navigation links for standard email folders,
 * AI-generated categories, and application settings. It highlights the
 * active route based on the current location.
 *
 * @param {SidebarProps} props - The props for the component.
 * @returns {JSX.Element} The rendered sidebar navigation panel.
 */
export function Sidebar({ categories }: SidebarProps) {
  const [location] = useLocation();

  const navigationItems = [
    { href: "/", icon: LayoutDashboard, label: "Dashboard", active: true },
    { href: "/tools", icon: Wrench, label: "Tools" },
    { href: "/inbox", icon: Inbox, label: "Inbox", count: 23 },
    { href: "/starred", icon: Star, label: "Starred" },
    { href: "/sent", icon: Send, label: "Sent" },
    { href: "/trash", icon: Trash2, label: "Trash" },
  ];

  const settingsItems = [
    { href: "/settings", icon: Settings, label: "Settings" },
    { href: "/ai-training", icon: Brain, label: "AI Training" },
  ];

  /**
   * Returns the appropriate color class for a category badge.
   * @param {string} [color] - The hex color code for the category.
   * @returns {string} The Tailwind CSS background color class.
   */
  const getCategoryColor = (color?: string) => {
    switch (color) {
      case "#34A853": return "bg-green-500";
      case "#4285F4": return "bg-blue-500";
      case "#FBBC04": return "bg-yellow-500";
      case "#EA4335": return "bg-red-500";
      case "#9C27B0": return "bg-purple-500";
      case "#00BCD4": return "bg-cyan-500";
      default: return "bg-gray-500";
    }
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex-shrink-0">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
            <Mail className="text-white h-4 w-4" />
          </div>
          <h1 className="text-xl font-semibold text-gray-900">GmailAI</h1>
        </div>
      </div>

      {/* Navigation Menu */}
      <nav className="p-2">
        <ul className="space-y-1">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = location === item.href || (item.href === "/" && location === "/dashboard");

            return (
              <li key={item.href}>
                <Link href={item.href} className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  isActive
                    ? "bg-blue-50 text-blue-600 font-medium"
                    : "hover:bg-gray-100 text-gray-700"
                }`}>
                  <Icon className="h-5 w-5" />
                  <span>{item.label}</span>
                  {item.count && (
                    <Badge variant="secondary" className="ml-auto">
                      {item.count}
                    </Badge>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>

        {/* AI Categories Section */}
        <div className="mt-6">
          <h3 className="text-sm font-medium text-gray-500 px-3 mb-2 uppercase tracking-wider">
            AI Categories
          </h3>
          <ul className="space-y-1">
            {categories.map((category) => (
              <li key={category.id}>
                <div className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-700 cursor-pointer">
                  <div className={`w-3 h-3 rounded-full ${getCategoryColor(category.color)}`}></div>
                  <span className="text-sm">{category.name}</span>
                  <span className="ml-auto text-xs text-gray-500">{category.count}</span>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Settings */}
        <div className="mt-6 pt-4 border-t border-gray-200">
          <ul className="space-y-1">
            {settingsItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.href}>
                  <Link href={item.href}>
                    <a className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-700">
                      <Icon className="h-5 w-5" />
                      <span>{item.label}</span>
                    </a>
                  </Link>
                </li>
              );
            })}
            <li>
              <Link href="/profile">
                <a className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors text-gray-700">
                  <Settings className="h-5 w-5" />
                  <span>Profile</span>
                </a>
              </Link>
            </li>
          </ul>
        </div>
      </nav>
    </div>
  );
}