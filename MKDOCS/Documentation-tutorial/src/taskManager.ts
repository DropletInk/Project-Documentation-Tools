import { Task } from "./task"

/**
 * Handles all task operations.
 */
export class TaskManager {

  /**
   * Stores all tasks.
   */
  private tasks: Task[] = []

  /**
   * Adds a new task.
   *
   * @param title Title of task
   */
  addTask(title: string): void {

    const newTask: Task = {
      id: this.tasks.length + 1,
      title,
      completed: false
    }

    this.tasks.push(newTask)

    console.log("Task Added:", newTask)
  }

  /**
   * Displays all tasks.
   */
  viewTasks(): void {

    console.log("\nTasks List:")

    this.tasks.forEach(task => {

      console.log(
        `${task.id}. ${task.title} - ${
          task.completed ? "Completed" : "Pending"
        }`
      )
    })
  }

  /**
   * Marks a task as completed.
   *
   * @param id Task ID
   */
  completeTask(id: number): void {

    const task = this.tasks.find(task => task.id === id)

    if (task) {
      task.completed = true
      console.log("Task Completed")
    }
  }

  /**
   * Deletes a task.
   *
   * @param id Task ID
   */
  deleteTask(id: number): void {

    this.tasks = this.tasks.filter(task => task.id !== id)

    console.log("Task Deleted")
  }
}