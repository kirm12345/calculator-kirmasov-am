#include <climits>
#include <gtest/gtest.h>

extern "C" {
    extern float eval_expr();
    extern float eval_term();
    extern float eval_factor();
}

const char *input_string = nullptr;
bool float_mode = false;

TEST(CalculatorTest, Addition) {
    input_string = "3 + 5";
    EXPECT_EQ(eval_expr(), 8);
}

TEST(CalculatorTest, Subtraction) {
    input_string = "10 - 7";
    EXPECT_EQ(eval_expr(), 3);
}

TEST(CalculatorTest, Multiplication) {
    input_string = "4 * 3";
    EXPECT_EQ(eval_expr(), 12);
}

TEST(CalculatorTest, Division) {
    input_string = "20 / 5";
    EXPECT_EQ(eval_expr(), 4);
}

TEST(CalculatorTest, Parentheses) {
    input_string = "(2 + 3) * 4";
    EXPECT_EQ(eval_expr(), 20);
}

TEST(CalculatorTest, DivisionByZero) {
    input_string = "5 / 0";
    ASSERT_EXIT(eval_expr(), ::testing::ExitedWithCode(1), ".*Ошибка: Деление на ноль.*");
}

TEST(CalculatorTest, InvalidOperators) {
    input_string = "5 ++ 3";
    ASSERT_EXIT(eval_expr(), ::testing::ExitedWithCode(1), ".*Ошибка: Некорректное выражение.*");
}

TEST(CalculatorTest, IntMax) {
    char expr[50];
    snprintf(expr, sizeof(expr), "%d + 0", INT_MAX);
    input_string = expr;
    float_mode = false;
    EXPECT_NEAR(eval_expr(), INT_MAX, 256); 
}

TEST(CalculatorTest, IntMin) {
    char expr[50];
    snprintf(expr, sizeof(expr), "%d + 0", INT_MIN);
    input_string = expr;
    float_mode = false;
    EXPECT_NEAR(eval_expr(), INT_MIN, 256); 
}

TEST(CalculatorTest, FloatModeAddition) {
    float_mode = true;
    input_string = "2.5 + 3.5";
    EXPECT_FLOAT_EQ(eval_expr(), 6.0f);
}

TEST(CalculatorTest, FloatModeDivision) {
    float_mode = true;
    input_string = "10 / 4";
    EXPECT_FLOAT_EQ(eval_expr(), 2.5f);
}

TEST(CalculatorTest, FloatModeSmallDivisor) {
    float_mode = true;
    input_string = "1 / 0.00001";
    ASSERT_EXIT(eval_expr(), ::testing::ExitedWithCode(1), ".*Ошибка: Деление на число меньше 10\\^-4.*");
}

TEST(CalculatorTest, NegativeNumbers) {
    input_string = "-(-5)";
    EXPECT_EQ(eval_expr(), 5);
}

TEST(CalculatorTest, OperatorPrecedence) {
    input_string = "2 + 3 * 4";
    EXPECT_EQ(eval_expr(), 14);
}
