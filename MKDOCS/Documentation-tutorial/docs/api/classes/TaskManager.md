[**Task Manager API**](../README.md)

***

[Task Manager API](../README.md) / TaskManager

# Class: TaskManager

Defined in: taskManager.ts:6

Handles all task operations.

## Constructors

### Constructor

> **new TaskManager**(): `TaskManager`

#### Returns

`TaskManager`

## Methods

### addTask()

> **addTask**(`title`): `void`

Defined in: taskManager.ts:18

Adds a new task.

#### Parameters

##### title

`string`

Title of task

#### Returns

`void`

***

### completeTask()

> **completeTask**(`id`): `void`

Defined in: taskManager.ts:53

Marks a task as completed.

#### Parameters

##### id

`number`

Task ID

#### Returns

`void`

***

### deleteTask()

> **deleteTask**(`id`): `void`

Defined in: taskManager.ts:68

Deletes a task.

#### Parameters

##### id

`number`

Task ID

#### Returns

`void`

***

### viewTasks()

> **viewTasks**(): `void`

Defined in: taskManager.ts:34

Displays all tasks.

#### Returns

`void`
