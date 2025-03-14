CC  ?= gcc
CXX ?= g++
AR  ?= ar

SRC_DIR   ?= src
TESTS_DIR ?= tests
BUILD_DIR ?= build

APP_BUILD_DIR=$(BUILD_DIR)/app
TEST_BUILD_DIR=$(BUILD_DIR)/test

TEST_BUILD_DIR_APP_OBJS=$(TEST_BUILD_DIR)/app
TEST_BUILD_DIR_UNIT_TESTS_OBJS=$(TEST_BUILD_DIR)/unit-tests

GTEST_DIR ?= googletest/googletest
CPPFLAGS += -isystem $(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -pthread -std=c++17
CFLAGS   += -g -Wall -Wextra -Wpedantic -Werror -std=c11

APP_SRCS := $(shell find $(SRC_DIR) -name '*.c')
TEST_SRCS := $(shell find $(TESTS_DIR) -name '*.cpp')

APP_OBJS := $(patsubst $(SRC_DIR)/%.c, $(APP_BUILD_DIR)/%.o, $(APP_SRCS))
TEST_OBJS := $(patsubst $(SRC_DIR)/%.c, $(TEST_BUILD_DIR_APP_OBJS)/%.o, $(filter-out $(SRC_DIR)/main.c, $(APP_SRCS)))
UNIT_TESTS_OBJS := $(patsubst $(TESTS_DIR)/%.cpp, $(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o, $(TEST_SRCS))

all: $(BUILD_DIR)/app.exe $(BUILD_DIR)/unit-tests.exe

clean:
	rm -rf $(BUILD_DIR)

run-int: $(BUILD_DIR)/app.exe
	@$<

run-float: $(BUILD_DIR)/app.exe
	@$< --float

run-unit-tests: $(BUILD_DIR)/unit-tests.exe
	@$<

-include $(APP_OBJS:.o=.d)
$(APP_BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(BUILD_DIR)/app.exe: $(APP_OBJS)
	$(CC) $(CFLAGS) $^ -o $@

$(TEST_BUILD_DIR_APP_OBJS)/main_test.o: $(SRC_DIR)/main.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -DGTEST -c $< -o $@

-include $(TEST_OBJS:.o=.d)
$(TEST_BUILD_DIR_APP_OBJS)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -DGTEST -c $< -o $@

-include $(UNIT_TESTS_OBJS:.o=.d)
$(TEST_BUILD_DIR_UNIT_TESTS_OBJS)/%.o: $(TESTS_DIR)/%.cpp
	@mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MMD -MP -c $< -o $@

$(BUILD_DIR)/unit-tests.exe: $(TEST_OBJS) $(UNIT_TESTS_OBJS) $(TEST_BUILD_DIR_APP_OBJS)/main_test.o $(TEST_BUILD_DIR)/gtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -lpthread $^ -o $@

$(TEST_BUILD_DIR)/gtest-all.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest-all.cc -o $@

$(TEST_BUILD_DIR)/gtest_main.o: $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c $(GTEST_DIR)/src/gtest_main.cc -o $@

$(TEST_BUILD_DIR)/gtest_main.a: $(TEST_BUILD_DIR)/gtest-all.o $(TEST_BUILD_DIR)/gtest_main.o
	$(AR) $(ARFLAGS) $@ $^

venv:
	python3 -m venv venv && source venv/bin/activate && pip install pytest

run-integration-tests: $(BUILD_DIR)/app.exe
	pytest tests/integration/

run-server:
	python3 serv.py
