# EmailIntelligence Extensions

This directory contains extensions for the EmailIntelligence application. Extensions provide a way to add custom functionality to the application without modifying the core codebase.

## Available Extensions

- [Example Extension](../extensions/example/README.md) - Demonstrates the extension system by adding emojis and detailed metrics to sentiment analysis

## Extension Structure

Each extension should have the following structure:

- **Main Module**: Contains the extension code (e.g., `example.py`)
- **Metadata File**: Contains information about the extension (`metadata.json`)
- **README File**: Contains documentation for the extension (`README.md`)
- **Requirements File**: Contains dependencies for the extension (`requirements.txt`)

## Creating Extensions

You can create a new extension template using the launcher script:

```bash
python launch.py --create-extension my_extension
```

This will create a new extension template in the `extensions/my_extension` directory with the necessary files.

## Extension Lifecycle

Extensions go through the following lifecycle:

1. **Discovery**: Extensions are discovered in the extensions directory
2. **Loading**: Extension modules are loaded into memory
3. **Initialization**: Extensions are initialized with configuration
4. **Execution**: Extensions provide functionality during application execution
5. **Shutdown**: Extensions are properly shut down when the application exits

## Managing Extensions

You can manage extensions using the launcher script:

```bash
# List all installed extensions
python launch.py --list-extensions

# Install an extension from a Git repository
python launch.py --install-extension https://github.com/username/extension.git

# Update an extension
python launch.py --update-extension example

# Uninstall an extension
python launch.py --uninstall-extension example
```

## Extension API

Extensions can interact with the core application through the Extension API. This API provides access to various components of the application, such as:

- **AI Engine**: Access to the AI and NLP capabilities
- **Data Store**: Access to the application's data store
- **User Interface**: Ability to add UI components
- **Event System**: Subscribe to and publish events

For more information about the Extension API, see the [Environment Management](env_management.md#extension-system) documentation.

## Best Practices

When creating extensions, follow these best practices:

1. **Isolation**: Keep your extension isolated from other extensions
2. **Error Handling**: Handle errors gracefully to avoid affecting the core application
3. **Documentation**: Document your extension thoroughly
4. **Testing**: Test your extension thoroughly before distributing it
5. **Dependencies**: Minimize dependencies and specify them in `requirements.txt`