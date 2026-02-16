# Advanced Email Filtering System Documentation

## Overview
The Email Intelligence Platform now includes an enhanced filtering system with sophisticated criteria and a user-friendly interface. This system allows users to create complex filtering rules combining multiple criteria types, making email organization and management significantly more powerful and efficient.

## Enhanced FilterNode Capabilities

The core of the advanced filtering system is the enhanced `FilterNode` in `backend/node_engine/email_nodes.py`, which now supports:

### 1. Keyword-Based Filtering
- **Required Keywords**: Emails must contain any of these keywords in subject or content
- **Excluded Keywords**: Emails containing these keywords are filtered out

### 2. Sender-Based Filtering
- **Required Senders**: Only emails from these senders pass through
- **Excluded Senders**: Emails from these senders are filtered out

### 3. Recipient-Based Filtering
- **Required Recipients**: Only emails sent to these recipients pass through
- **Excluded Recipients**: Emails sent to these recipients are filtered out

### 4. Category-Based Filtering
- **Required Categories**: Only emails in these categories pass through
- **Excluded Categories**: Emails in these categories are filtered out

### 5. Date/Time-Based Filtering
- **After Date**: Only emails received after this date pass through
- **Before Date**: Only emails received before this date pass through

### 6. Size-Based Filtering
- **Minimum Size**: Only emails with content larger than this size pass through
- **Maximum Size**: Only emails with content smaller than this size pass through

### 7. Priority-Based Filtering
- Filter emails based on their priority level (low, normal, high)

### 8. Complex Boolean Logic
- **AND Conditions**: All conditions must be true
- **OR Conditions**: At least one condition must be true
- **NOT Conditions**: All conditions must be false

## UI Component: AdvancedFilterPanel

The `client/src/components/advanced-filter-panel.tsx` provides a user-friendly interface for creating complex filters:

### Features:
- Keyword filtering inputs (required and excluded)
- Sender and recipient filtering inputs
- Date range pickers
- Size-based filtering options
- Category selection dropdowns
- Custom condition builder with multiple operators
- Case sensitivity toggle

### Integration:
- Integrated into the dashboard UI as a collapsible panel
- Accessible via an "Advanced Filters" toggle button
- Allows users to apply complex filtering rules without code knowledge

## Usage Examples

### Example 1: Basic Keyword Filtering
```json
{
  "required_keywords": ["urgent", "report"],
  "excluded_keywords": ["marketing", "advertisement"]
}
```

### Example 2: Multi-Criteria Filtering
```json
{
  "required_categories": ["work"],
  "excluded_categories": ["promotions"],
  "required_senders": ["boss@company.com"],
  "date_criteria": {
    "after": "2023-01-01T00:00:00Z"
  }
}
```

### Example 3: Complex Boolean Filtering
```json
{
  "and": [
    {"type": "contains_keyword", "value": "report"}
  ],
  "or": [
    {"type": "from_sender", "value": "boss@company.com"},
    {"type": "has_category", "value": "work"}
  ]
}
```

## API Integration

The filtering system integrates with the existing workflow engine architecture and can be used in various parts of the application. The filter criteria can be passed through the workflow system to process emails according to user-defined rules.

## Testing

A comprehensive test suite is available in `test_enhanced_filtering.py` that verifies all filtering capabilities work as expected. The tests cover:
- Each individual filtering type
- Combinations of different filter types
- Edge cases and error conditions
- Complex boolean logic

## Performance Considerations

- The filtering system was designed to be efficient with large email volumes
- Caching mechanisms can be implemented for frequently used filters
- The system maintains the existing workflow engine's performance monitoring capabilities

## Security & Validation

- All inputs to the filtering system are validated to prevent injection attacks
- The system integrates with the existing security framework
- User-defined filters are sanitized before execution