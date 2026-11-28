import asyncio
import sys

sys.path.append("backend")
from python_nlp.gmail_integration import GmailDataCollector


async def main():
    print("Starting retrieval...")
    try:
        collector = GmailDataCollector()
        print("Collector created")
        emails = await collector.collect_emails(query="test", max_emails=1)
        print(f"Retrieved {len(emails)} emails")
        if emails:
            print("First email content:")
            print(emails[0])
        else:
            print("No emails")
    except Exception as e:
        print("Error:", e)
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
