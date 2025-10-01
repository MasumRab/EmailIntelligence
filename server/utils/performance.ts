export async function measureExecutionTime<T>(fn: () => Promise<T>, label: string): Promise<T> {
  console.time(label);
  const result = await fn();
  console.timeEnd(label);
  return result;
}
