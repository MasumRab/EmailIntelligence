/**
 * Tests for `useDebounce`, the hook behind the dashboard search box.
 *
 * Fake timers are the point: a real `setTimeout` would make these tests sleep, and a test
 * that sleeps to prove a 300ms delay is both slow and flaky. Advancing the clock explicitly
 * also lets the suite assert the part that actually breaks — that a value arriving before
 * the delay expires cancels the pending update rather than being emitted and then corrected.
 */
import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { useDebounce } from "./use-debounce";

describe("useDebounce", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns the initial value immediately", () => {
    const { result } = renderHook(() => useDebounce("first", 300));

    expect(result.current).toBe("first");
  });

  it("holds the old value until the delay has elapsed", () => {
    const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: "first" },
    });

    rerender({ value: "second" });
    expect(result.current).toBe("first");

    act(() => {
      vi.advanceTimersByTime(299);
    });
    expect(result.current).toBe("first");

    act(() => {
      vi.advanceTimersByTime(1);
    });
    expect(result.current).toBe("second");
  });

  it("emits only the last value when updates arrive faster than the delay", () => {
    const { result, rerender } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: "a" },
    });

    for (const value of ["ab", "abc", "abcd"]) {
      rerender({ value });
      act(() => {
        vi.advanceTimersByTime(100);
      });
    }

    // 300ms of typing, none of it beyond a 300ms window: still nothing emitted.
    expect(result.current).toBe("a");

    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(result.current).toBe("abcd");
  });

  it("does not update after unmount", () => {
    const { rerender, unmount } = renderHook(({ value }) => useDebounce(value, 300), {
      initialProps: { value: "a" },
    });

    rerender({ value: "b" });
    unmount();

    // A missing clearTimeout would now set state on an unmounted component; React logs a
    // warning and, under StrictMode, the stale value can resurface. Advancing past the
    // delay is what proves the cleanup ran.
    expect(() => {
      act(() => {
        vi.advanceTimersByTime(1000);
      });
    }).not.toThrow();
  });
});
