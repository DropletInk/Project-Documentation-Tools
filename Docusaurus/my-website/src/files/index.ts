/**
 * Adds two numbers together.
 *
 * @param a - The first number
 * @param b - The second number
 * @returns The sum of `a` and `b`
 *
 * @example
 * ```ts
 * const result = add(2, 3); // 5
 * ```
 */
export function add(a: number, b: number): number {
  return a + b;
}

/**
 * Represents a user in the system.
 */
export interface User {
  /** Unique identifier */
  id: string;
  /** Display name */
  name: string;
  /** Optional email address */
  email?: string;
}