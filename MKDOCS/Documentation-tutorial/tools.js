"use strict";
// Function with type annotations for parameters and return type
function greetUser(user) {
    return `Hello, ${user.firstName} ${user.lastName}!`;
}
// Create a user object that matches the interface
const newUser = {
    firstName: "Jane",
    lastName: "Doe",
    age: 28
};
// Log the result of the function
console.log(greetUser(newUser));
