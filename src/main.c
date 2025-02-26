#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_INPUT_SIZE 1024
#define MIN_DIVISOR 1e-4f
#define INT_MAX_VALUE 2147483647
#define INT_MIN_VALUE -2147483648

#ifdef GTEST
extern const char *input_string;
extern bool float_mode;
#else
const char *input_string;
bool float_mode = false;
#endif

float eval_expr(void);
float eval_term(void);
float eval_factor(void);

float eval_expr() {

  float result = eval_term();

  while (1) {
    while (isspace(*input_string))
      input_string++;

    if ((*input_string == '+' || *input_string == '-' || *input_string == '*' ||
         *input_string == '/') &&
        (*(input_string + 1) == '+' || *(input_string + 1) == '-' ||
         *(input_string + 1) == '*' || *(input_string + 1) == '/')) {
      fprintf(stderr, "Ошибка: Некорректное выражение!\n");
      fflush(stderr);
      exit(EXIT_FAILURE);
    }

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

float eval_term() {
  float result = eval_factor();

  while (1) {
    while (isspace(*input_string))
      input_string++;

    if (*input_string == '*') {
      input_string++;
      result *= eval_factor();
    } else if (*input_string == '/') {
      input_string++;
      float divisor = eval_factor();
      if (float_mode && divisor < MIN_DIVISOR) {
        fprintf(stderr, "Ошибка: Деление на число меньше 10^-4!\n");
        exit(EXIT_FAILURE);
      }
      if (!float_mode && divisor == 0) {
        fprintf(stderr, "Ошибка: Деление на ноль!\n");
        exit(EXIT_FAILURE);
      }
      result = float_mode ? (result / divisor) : ((int)result / (int)divisor);
    } else {
      break;
    }

    if (!float_mode && (result > INT_MAX_VALUE || result < INT_MIN_VALUE)) {
      fprintf(stderr, "Ошибка: Переполнение целого числа!\n");
      exit(EXIT_FAILURE);
    }
  }
  return result;
}

float eval_factor() {
  while (isspace(*input_string))
    input_string++;

  if (*input_string == '(') {
    input_string++;
    float result = eval_expr();
    while (isspace(*input_string))
      input_string++;
    if (*input_string == ')')
      input_string++;
    return result;
  }

  float number = 0;
  float fraction = 0.0f;
  int fraction_div = 1;
  bool is_float = false;

  while (isdigit(*input_string) || *input_string == '.') {
    if (*input_string == '.') {
      is_float = true;
    } else {
      if (is_float) {
        fraction = fraction * 10 + (*input_string - '0');
        fraction_div *= 10;
      } else {
        number = number * 10 + (*input_string - '0');
      }
    }
    input_string++;
  }

  return float_mode ? (number + fraction / fraction_div) : number;
}

#ifndef GTEST
int main(int argc, char *argv[]) {
  if (argc > 1 && strcmp(argv[1], "--float") == 0) {
    float_mode = true;
  }

  char input[MAX_INPUT_SIZE];
  size_t len = 0;
  int ch;
  bool last_was_op = true;

  while ((ch = getchar()) != EOF && len < MAX_INPUT_SIZE - 1) {
    if (!strchr("0123456789()+-*/\\s", ch)) {
      fprintf(stderr, "Ошибка: Некорректные символы в выражении!\n");
      return 1;
    }
    if (strchr("+-*/", ch) && last_was_op) {
      fprintf(stderr, "Ошибка: Некорректное выражение!\n");
      exit(EXIT_FAILURE);
    }
    last_was_op = strchr("+-*/", ch) != NULL;
    input[len++] = (char)ch;
  }
  input[len] = '\0';

  if (len >= MAX_INPUT_SIZE - 1) {
    fprintf(stderr, "Ошибка: Ввод превышает 1024 байта!\n");
    return 1;
  }

  if (len == 0) {
    fprintf(stderr, "Ошибка: Пустой ввод!\n");
    return 1;
  }

  input_string = input;
  float result = eval_expr();

  while (isspace(*input_string))
    input_string++;
  if (*input_string != '\0' && *input_string != '\n') {
    fprintf(stderr, "Ошибка: Некорректное выражение!\n");
    return 1;
  }

  if (float_mode) {
    printf("%.6f\n", result);
  } else {
    printf("%d\n", (int)result);
  }

  return 0;
}
#endif
