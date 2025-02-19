#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAX_INPUT_SIZE 1024

const char *input_string;

int eval_expr(void);
int eval_term(void);
int eval_factor(void);


int eval_expr() {
    int result = eval_term();
    
    while (1) {
        while (isspace(*input_string)) input_string++; 
        
        if (*input_string == '+') {
            input_string++;
            result += eval_term();
        } else if (*input_string == '-') {
            input_string++;
            result -= eval_term();
        } else {
            break;
        }
    }
    return result;
}


int eval_term() {
    int result = eval_factor();
    
    while (1) {
        while (isspace(*input_string)) input_string++; 
        
        if (*input_string == '*') {
            input_string++;
            result *= eval_factor();
        } else if (*input_string == '/') {
            input_string++;
            int divisor = eval_factor();
            if (divisor == 0) {
                fprintf(stderr, "Ошибка: Деление на ноль!\n");
                exit(EXIT_FAILURE);
            }
            result /= divisor;
        } else {
            break;
        }
    }
    return result;
}

int eval_factor() {
    while (isspace(*input_string)) input_string++; 
    
    if (*input_string == '(') {
        input_string++; // Пропустить '('
        int result = eval_expr();
        while (isspace(*input_string)) input_string++; 
        if (*input_string == ')') input_string++; 
        return result;
    }
    
    int number = 0;
    while (isdigit(*input_string)) {
        number = number * 10 + (*input_string - '0');
        input_string++;
    }
    return number;
}

int main() {
    char input[MAX_INPUT_SIZE];
    if (!fgets(input, MAX_INPUT_SIZE, stdin)) {
        return 1;
    }
    
    input_string = input;
    int result = eval_expr();


    while (isspace(*input_string)) input_string++; 
    if (*input_string != '\0' && *input_string != '\n') {
        fprintf(stderr, "Ошибка: Некорректное выражение!\n");
        return 1;
    }

    printf("%d\n", result);
    return 0;
}
