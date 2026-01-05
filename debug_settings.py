print("Starting import...")
try:
    from src.core.config import settings

    print("Import successful")
    print(f"Settings loaded: {settings.environment}")
except Exception as e:
    print(f"Import failed: {e}")
print("Done")
