/**
 * Represents a single task.
 */
export interface Task {

  /**
   * Unique ID of task
   */
  id: number

  /**
   * Title of task
   */
  title: string

  /**
   * Completion status
   */
  completed: boolean
}