import asyncio
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.resolution.semantic_merger import SemanticMerger
from src.core.conflict_models import ConflictBlock


async def main():
    merger = SemanticMerger()

    print("Verifying SemanticMerger...")

    # Scenario 1: False Conflict (Whitespace)
    print("\nScenario 1: False Conflict (Whitespace)")
    base = "def foo():\n    return 1"
    ours = "def foo():\n    return 1  "  # Trailing space
    theirs = "def foo():\n\n    return 1"  # Extra newline

    block = ConflictBlock(
        file_path="test.py",
        start_line=1,
        end_line=2,
        current_content=ours,
        incoming_content=theirs,
        base_content=base,
    )

    result = await merger.merge_blocks(block)
    print(f"Result: {result!r}")
    if result == theirs:
        print("✅ Passed (Preferred incoming for style fix)")
    else:
        print("❌ Failed")

    # Scenario 2: Ours unchanged semantically, Theirs changed
    print("\nScenario 2: Ours unchanged, Theirs changed")
    base = "def foo():\n    return 1"
    ours = "def foo():\n    return 1  "  # Whitespace only
    theirs = "def foo():\n    return 2"  # Semantic change

    block = ConflictBlock(
        file_path="test.py",
        start_line=1,
        end_line=2,
        current_content=ours,
        incoming_content=theirs,
        base_content=base,
    )

    result = await merger.merge_blocks(block)
    print(f"Result: {result!r}")
    if result == theirs:
        print("✅ Passed (Accepted semantic change from theirs)")
    else:
        print("❌ Failed")

    # Scenario 3: Theirs unchanged semantically, Ours changed
    print("\nScenario 3: Theirs unchanged, Ours changed")
    base = "def foo():\n    return 1"
    ours = "def foo():\n    return 2"  # Semantic change
    theirs = "def foo():\n    return 1  "  # Whitespace only

    block = ConflictBlock(
        file_path="test.py",
        start_line=1,
        end_line=2,
        current_content=ours,
        incoming_content=theirs,
        base_content=base,
    )

    result = await merger.merge_blocks(block)
    print(f"Result: {result!r}")
    if result == ours:
        print("✅ Passed (Kept our semantic change)")
    else:
        print("❌ Failed")

    # Scenario 4: Both changed semantically (Equivalent)
    print("\nScenario 4: Both changed semantically (Equivalent)")
    base = "def foo():\n    return 1"
    ours = "def foo():\n    return 2"
    theirs = "def foo():\n    return 2"  # Same change

    block = ConflictBlock(
        file_path="test.py",
        start_line=1,
        end_line=2,
        current_content=ours,
        incoming_content=theirs,
        base_content=base,
    )

    result = await merger.merge_blocks(block)
    print(f"Result: {result!r}")
    if result == ours:  # or theirs, they are same
        print("✅ Passed (Resolved equivalent changes)")
    else:
        print("❌ Failed")

    # Scenario 5: Real Conflict
    print("\nScenario 5: Real Conflict")
    base = "def foo():\n    return 1"
    ours = "def foo():\n    return 2"
    theirs = "def foo():\n    return 3"

    block = ConflictBlock(
        file_path="test.py",
        start_line=1,
        end_line=2,
        current_content=ours,
        incoming_content=theirs,
        base_content=base,
    )

    result = await merger.merge_blocks(block)
    print(f"Result: {result!r}")
    if result is None:
        print("✅ Passed (Correctly identified real conflict)")
    else:
        print("❌ Failed")


if __name__ == "__main__":
    asyncio.run(main())
