# calculator-kirmasov-am

## Description
This is a simple C program that reads an arithmetic expression from standard input, parses it, and prints the result. The program supports the following operators on integers: `+`, `-`, `*`, `/`, `(`, and `)`. It also handles whitespace characters in the input.

## Features
### Supported Operators
- `+` (Addition)  
- `-` (Subtraction)  
- `*` (Multiplication)  
- `/` (Division)  
- `(` and `)` (Parentheses for grouping expressions)  

### Additional Functionality
- **Whitespace Handling:** The program ignores spaces in the input.  
- **Input Size:** The input must be shorter than **1 KiB**.  
- **Output:** The result of the evaluated expression is printed as an integer.  
- **No External Dependencies:** The program uses only the standard C library (`libc`).  

## Compilation
To compile the program, run the following command:

```sh
gcc main.c -o calculator.exe
```

## Execution To run the program, execute: 

```
sh ./calculator.exe
```

## Input and Output
- The program will prompt you to enter an **arithmetic expression**.  
- After entering the expression, press **Enter**, then **Ctrl+D** (to finish input).  
- The computed result will be **displayed on the screen**.  

## Code Formatting
The code follows the **WebKit** style guide. To ensure proper formatting, use:

```sh
clang-format -i main.c
```
This command will format `main.c` according to **WebKit coding standards**.

## Testing
This project includes **automated tests** using **GoogleTest**.

### Running Unit Tests
To compile and run tests, execute:

```sh
make run-unit-tests
```

This will build the project and run the tests to verify **basic calculations and error handling**.

## Sources

- **DeepSeek**
- **GPT-4o**
