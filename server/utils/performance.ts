/**
 * @file Provides performance measurement utilities.
 *
 * This module contains helper functions for measuring and logging the
 * execution time of asynchronous operations, which is useful for performance
 * monitoring and optimization.
 */

/**
 * Measures and logs the execution time of an asynchronous function.
 *
 * This higher-order function takes an async function and a label, logs the
 * execution time to the console using `console.time` and `console.timeEnd`,
 * and returns the result of the original function.
 *
 * @template T - The return type of the function to be measured.
 * @param {() => Promise<T>} fn - The asynchronous function to measure.
 * @param {string} label - A label for the performance measurement, used in the console logs.
 * @returns {Promise<T>} A promise that resolves to the result of the executed function.
 */
export async function measureExecutionTime<T>(fn: () => Promise<T>, label: string): Promise<T> {
  console.time(label);
  const result = await fn();
  console.timeEnd(label);
  return result;
}