# EmailIntelligence Frontend

This directory contains the frontend application for EmailIntelligence. The frontend is built with React, TypeScript, and various modern web technologies to provide a responsive and intuitive user interface.

## Directory Structure

- **index.html**: Main HTML entry point
- **src/**: Source code directory
  - **App.tsx**: Main application component
  - **main.tsx**: Application entry point
  - **index.css**: Global CSS styles
  - **components/**: Reusable UI components
    - **ui/**: Basic UI components (buttons, inputs, etc.)
    - **ai-analysis-panel.tsx**: AI analysis panel component
    - **category-overview.tsx**: Email category overview component
    - **email-list.tsx**: Email list component
    - **recent-activity.tsx**: Recent activity component
    - **sidebar.tsx**: Sidebar navigation component
    - **stats-cards.tsx**: Statistics cards component
  - **hooks/**: Custom React hooks
    - **use-mobile.tsx**: Hook for responsive design
    - **use-toast.ts**: Hook for toast notifications
  - **lib/**: Utility functions and libraries
    - **api.ts**: API client for backend communication
    - **queryClient.ts**: React Query client configuration
    - **utils.ts**: General utility functions
  - **pages/**: Application pages
    - **dashboard.tsx**: Main dashboard page
    - **not-found.tsx**: 404 page
  - **types/**: TypeScript type definitions
    - **index.ts**: Common type definitions

## Development

### Running the Frontend

You can run the frontend in development mode using:

```bash
# From the project root
npm run dev
```

Or using the unified launcher:

```bash
# From the project root
python launch.py --frontend-only
```

### Building for Production

To build the frontend for production:

```bash
# From the project root
npm run build
```

This will create optimized production files in the `dist` directory.

### Adding New Components

When adding new components:

1. Create a new file in the appropriate directory (e.g., `components/`)
2. Export the component as the default export
3. Import and use the component where needed

Example:

```tsx
// components/my-component.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
}

export default function MyComponent({ title }: MyComponentProps) {
  return <div>{title}</div>;
}
```

### Styling

The project uses a combination of:

- Tailwind CSS for utility-based styling
- CSS modules for component-specific styling
- Global styles in `index.css`

### API Communication

Use the API client in `lib/api.ts` for communicating with the backend:

```tsx
import { api } from '../lib/api';

// Example usage
const fetchEmails = async () => {
  const response = await api.get('/emails');
  return response.data;
};
```

## UI Components

The application includes various UI components:

- **AI Analysis Panel**: Displays AI analysis of emails
- **Category Overview**: Shows email categories and statistics
- **Email List**: Displays a list of emails with filtering and sorting
- **Recent Activity**: Shows recent email activity
- **Sidebar**: Provides navigation and filtering options
- **Stats Cards**: Displays key statistics and metrics

## Pages

The application includes the following pages:

- **Dashboard**: Main application dashboard with email management
- **Not Found**: 404 page for handling invalid routes