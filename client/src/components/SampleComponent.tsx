import React from 'react';

// Define the props interface
interface SampleComponentProps {
  title: string;
  description?: string;
  count?: number;
}

// Functional component implementation
const SampleComponent: React.FC<SampleComponentProps> = ({
  title,
  description = 'Default description',
  count = 0
}) => {
  return (
    <div className="sample-component">
      <h2 className="sample-title">{title}</h2>
      <p className="sample-description">{description}</p>
      <div className="sample-count">Count: {count}</div>
    </div>
  );
};

// Default export
export default SampleComponent;