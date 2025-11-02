# Migration Guide: Legacy Dashboard

This guide provides instructions for migrating from the legacy dashboard to the new consolidated dashboard.

## Overview

The legacy dashboard, located at `backend/python_backend/dashboard_routes.py`, is deprecated and will be removed in a future version. The new consolidated dashboard, located at `modules/dashboard/routes.py`, provides a more comprehensive and efficient implementation.

## Key Changes

- The new dashboard uses a consolidated data model, `ConsolidatedDashboardStats`, which includes all the fields from both the legacy and modular dashboards.
- The new dashboard uses efficient server-side aggregations to calculate statistics, resulting in significant performance improvements.
- The new dashboard includes a modular widget system, allowing for greater flexibility and customization.
- The new dashboard includes historical trend analysis, providing insights into email volume and categorization trends over time.

## Migration Steps

1. **Update API Endpoints:** Update your client-side code to use the new API endpoints:
    - `/api/dashboard/stats`: Get dashboard statistics.
    - `/api/dashboard/widgets`: Get the list of available widgets.
    - `/api/dashboard/widgets/{widget_type}`: Get the data for a widget.
    - `/api/dashboard/historical-data`: Get historical dashboard data.
2. **Update Data Models:** Update your client-side code to use the new `ConsolidatedDashboardStats` data model.
3. **Remove Legacy Code:** Remove any code that references the legacy dashboard.

## Timeline

The legacy dashboard will be removed in version 4.0.0. Please migrate to the new consolidated dashboard as soon as possible.
