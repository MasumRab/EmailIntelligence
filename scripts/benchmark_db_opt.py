import timeit
import time

# Mock data
email_data = {
    "id": 1,
    "subject": "This is a test subject",
    "sender": "John Doe",
    "sender_email": "john.doe@example.com",
    "message_id": "msg123",
    "content": "Some long content here" * 10
}

# Original implementation
def get_searchable_text_orig(email):
    return (
        (email.get("subject") or "") + " " +
        (email.get("sender") or "") + " " +
        (email.get("sender_email") or "")
    ).lower()

# Optimized implementation
def get_searchable_text_opt(email):
    return f"{str(email.get('subject') or '')} {str(email.get('sender') or '')} {str(email.get('sender_email') or '')}".lower()

# Redundant calls (Current state)
def add_to_index_orig(email):
    search_index = {}
    eid = email["id"]
    # First call
    search_index[eid] = get_searchable_text_orig(email)
    # Second call
    search_index[eid] = get_searchable_text_orig(email)
    return search_index

# Optimized calls (New state)
def add_to_index_opt(email):
    search_index = {}
    eid = email["id"]
    # Single call
    search_index[eid] = get_searchable_text_opt(email)
    return search_index

def run_benchmark():
    iterations = 1000000

    print(f"Running {iterations} iterations...")

    # Measure Original
    start = time.perf_counter()
    for _ in range(iterations):
        add_to_index_orig(email_data)
    end = time.perf_counter()
    orig_time = end - start

    # Measure Optimized
    start = time.perf_counter()
    for _ in range(iterations):
        add_to_index_opt(email_data)
    end = time.perf_counter()
    opt_time = end - start

    print(f"Original: {orig_time:.4f}s")
    print(f"Optimized: {opt_time:.4f}s")
    print(f"Improvement: {(orig_time - opt_time) / orig_time * 100:.2f}%")

if __name__ == "__main__":
    run_benchmark()
