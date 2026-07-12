import { useState } from "react";
import { Button } from "@components/ui/button";
import { Input } from "@components/ui/input";
import { Label } from "@components/ui/label";
import { Checkbox } from "@components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@components/ui/card";
import { Badge } from "@components/ui/badge";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@components/ui/popover";
import { Calendar } from "@components/ui/calendar";
import { CalendarIcon, Plus, Trash2, Filter } from "lucide-react";
import type { Category } from "@shared/schema";

interface AdvancedFilterPanelProps {
  categories: Category[];
  onApplyFilters: (filters: any) => void;
}

interface FilterCondition {
  id: string;
  field: string;
  operator: string;
  value: string;
}

export function AdvancedFilterPanel({
  categories,
  onApplyFilters,
}: AdvancedFilterPanelProps) {
  const [requiredKeywords, setRequiredKeywords] = useState<string>("");
  const [excludedKeywords, setExcludedKeywords] = useState<string>("");
  const [requiredSenders, setRequiredSenders] = useState<string>("");
  const [excludedSenders, setExcludedSenders] = useState<string>("");
  const [requiredRecipients, setRequiredRecipients] = useState<string>("");
  const [excludedRecipients, setExcludedRecipients] = useState<string>("");
  const [afterDate, setAfterDate] = useState<string>("");
  const [beforeDate, setBeforeDate] = useState<string>("");
  const [minSize, setMinSize] = useState<string>("");
  const [maxSize, setMaxSize] = useState<string>("");
  const [requiredCategory, setRequiredCategory] = useState<string>("");
  const [excludedCategory, setExcludedCategory] = useState<string>("");
  const [isCaseSensitive, setIsCaseSensitive] = useState<boolean>(false);

  const [customConditions, setCustomConditions] = useState<FilterCondition[]>([
    { id: "1", field: "subject", operator: "contains", value: "" },
  ]);

  const operators = [
    { value: "contains", label: "contains" },
    { value: "not_contains", label: "does not contain" },
    { value: "equals", label: "equals" },
    { value: "not_equals", label: "does not equal" },
    { value: "starts_with", label: "starts with" },
    { value: "ends_with", label: "ends with" },
  ];

  const addCondition = () => {
    const newCondition: FilterCondition = {
      id: Date.now().toString(),
      field: "subject",
      operator: "contains",
      value: "",
    };
    setCustomConditions([...customConditions, newCondition]);
  };

  const removeCondition = (id: string) => {
    if (customConditions.length > 1) {
      setCustomConditions(
        customConditions.filter((condition) => condition.id !== id),
      );
    }
  };

  const updateCondition = (id: string, field: string, value: any) => {
    setCustomConditions(
      customConditions.map((condition) =>
        condition.id === id ? { ...condition, [field]: value } : condition,
      ),
    );
  };

  const applyFilters = () => {
    const filters: any = {};

    // Keyword-based filters
    if (requiredKeywords.trim()) {
      filters.required_keywords = requiredKeywords
        .split(",")
        .map((k) => k.trim())
        .filter((k) => k);
    }
    if (excludedKeywords.trim()) {
      filters.excluded_keywords = excludedKeywords
        .split(",")
        .map((k) => k.trim())
        .filter((k) => k);
    }

    // Sender-based filters
    if (requiredSenders.trim()) {
      filters.required_senders = requiredSenders
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s);
    }
    if (excludedSenders.trim()) {
      filters.excluded_senders = excludedSenders
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s);
    }

    // Recipient-based filters
    if (requiredRecipients.trim()) {
      filters.required_recipients = requiredRecipients
        .split(",")
        .map((r) => r.trim())
        .filter((r) => r);
    }
    if (excludedRecipients.trim()) {
      filters.excluded_recipients = excludedRecipients
        .split(",")
        .map((r) => r.trim())
        .filter((r) => r);
    }

    // Date-based filters
    if (afterDate || beforeDate) {
      filters.date_criteria = {};
      if (afterDate) filters.date_criteria.after = afterDate;
      if (beforeDate) filters.date_criteria.before = beforeDate;
    }

    // Size-based filters
    if (minSize || maxSize) {
      filters.size_criteria = {};
      if (minSize) filters.size_criteria.min_size = parseInt(minSize);
      if (maxSize) filters.size_criteria.max_size = parseInt(maxSize);
    }

    // Category-based filters
    if (requiredCategory) filters.required_categories = [requiredCategory];
    if (excludedCategory) filters.excluded_categories = [excludedCategory];

    // Case sensitivity
    if (isCaseSensitive) filters.case_sensitive = true;

    // Custom conditions
    if (customConditions.length > 0) {
      filters.custom_conditions = customConditions;
    }

    onApplyFilters(filters);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Filter className="h-5 w-5" />
          Advanced Email Filters
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Keyword Filters */}
        <div className="space-y-2">
          <Label>Keywords</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">
                Required Keywords
              </Label>
              <Input
                value={requiredKeywords}
                onChange={(e) => setRequiredKeywords(e.target.value)}
                placeholder="e.g., urgent, important"
              />
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">
                Excluded Keywords
              </Label>
              <Input
                value={excludedKeywords}
                onChange={(e) => setExcludedKeywords(e.target.value)}
                placeholder="e.g., spam, advertisement"
              />
            </div>
          </div>
        </div>

        {/* Sender Filters */}
        <div className="space-y-2">
          <Label>Senders</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">
                Required Senders
              </Label>
              <Input
                value={requiredSenders}
                onChange={(e) => setRequiredSenders(e.target.value)}
                placeholder="e.g., boss@company.com"
              />
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">
                Excluded Senders
              </Label>
              <Input
                value={excludedSenders}
                onChange={(e) => setExcludedSenders(e.target.value)}
                placeholder="e.g., marketing@company.com"
              />
            </div>
          </div>
        </div>

        {/* Recipient Filters */}
        <div className="space-y-2">
          <Label>Recipients</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">
                Required Recipients
              </Label>
              <Input
                value={requiredRecipients}
                onChange={(e) => setRequiredRecipients(e.target.value)}
                placeholder="e.g., team@company.com"
              />
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">
                Excluded Recipients
              </Label>
              <Input
                value={excludedRecipients}
                onChange={(e) => setExcludedRecipients(e.target.value)}
                placeholder="e.g., alumni@university.edu"
              />
            </div>
          </div>
        </div>

        {/* Date Filters */}
        <div className="space-y-2">
          <Label>Date Range</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">
                After Date
              </Label>
              <Input
                type="date"
                value={afterDate}
                onChange={(e) => setAfterDate(e.target.value)}
              />
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">
                Before Date
              </Label>
              <Input
                type="date"
                value={beforeDate}
                onChange={(e) => setBeforeDate(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Size Filters */}
        <div className="space-y-2">
          <Label>Content Size (characters)</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">Min Size</Label>
              <Input
                type="number"
                value={minSize}
                onChange={(e) => setMinSize(e.target.value)}
                placeholder="e.g., 100"
              />
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">Max Size</Label>
              <Input
                type="number"
                value={maxSize}
                onChange={(e) => setMaxSize(e.target.value)}
                placeholder="e.g., 5000"
              />
            </div>
          </div>
        </div>

        {/* Category Filters */}
        <div className="space-y-2">
          <Label>Category</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <Label className="text-xs text-muted-foreground">
                Required Category
              </Label>
              <Select
                value={requiredCategory}
                onValueChange={setRequiredCategory}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.id} value={category.name}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label className="text-xs text-muted-foreground">
                Excluded Category
              </Label>
              <Select
                value={excludedCategory}
                onValueChange={setExcludedCategory}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((category) => (
                    <SelectItem key={category.id} value={category.name}>
                      {category.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>

        {/* Case Sensitivity */}
        <div className="flex items-center space-x-2">
          <Checkbox
            id="case-sensitive"
            checked={isCaseSensitive}
            onCheckedChange={(checked) => setIsCaseSensitive(!!checked)}
          />
          <Label htmlFor="case-sensitive">Case sensitive matching</Label>
        </div>

        {/* Custom Conditions */}
        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <Label>Custom Conditions</Label>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addCondition}
            >
              <Plus className="h-4 w-4 mr-1" />
              Add Condition
            </Button>
          </div>

          <div className="space-y-2">
            {customConditions.map((condition) => (
              <div
                key={condition.id}
                className="flex items-center space-x-2 p-2 border rounded"
              >
                <Select
                  value={condition.field}
                  onValueChange={(value) =>
                    updateCondition(condition.id, "field", value)
                  }
                >
                  <SelectTrigger className="w-[120px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="subject">Subject</SelectItem>
                    <SelectItem value="content">Content</SelectItem>
                    <SelectItem value="sender">Sender</SelectItem>
                    <SelectItem value="category">Category</SelectItem>
                  </SelectContent>
                </Select>

                <Select
                  value={condition.operator}
                  onValueChange={(value) =>
                    updateCondition(condition.id, "operator", value)
                  }
                >
                  <SelectTrigger className="w-[120px]">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {operators.map((op) => (
                      <SelectItem key={op.value} value={op.value}>
                        {op.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                <Input
                  value={condition.value}
                  onChange={(e) =>
                    updateCondition(condition.id, "value", e.target.value)
                  }
                  placeholder="Value"
                />

                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => removeCondition(condition.id)}
                  disabled={customConditions.length <= 1}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>

        {/* Apply Filters Button */}
        <Button className="w-full" onClick={applyFilters}>
          Apply Filters
        </Button>
      </CardContent>
    </Card>
  );
}
