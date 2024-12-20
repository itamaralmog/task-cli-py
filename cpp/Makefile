# # # # # # CXX = g++
# # # # # # CXXFLAGS = -std=c++17 -Iinclude

# # # # # # all: task_cli

# # # # # # task_cli: task_cli.cpp
# # # # # # 	$(CXX) $(CXXFLAGS) task_cli.cpp -o task_cli  # <-- Use tabs here, not spaces!

# # # # # # test: task_cli_test.cpp
# # # # # # 	g++ -std=c++17 task_cli.cpp task_cli_test.cpp -lgtest -lgtest_main -pthread -o test_task_cli

# # # # # # clean:
# # # # # # 	rm -f task_cli tasks.json  # <-- Also use tabs for any command lines

# # # # # # # mkdir build
# # # # # # # cd build
# # # # # # # cmake ..
# # # # # # # make
# # # # # # # ./task_cli

CXX = g++
CXXFLAGS = -std=c++17 -Wall -I.

# Source files and output
SRC = task_cli.cpp
EXEC = task-cli
TEST_SRC = test_task_cli.cpp
TEST_EXEC = test_task-cli

# Default target (build the task CLI executable)
all: $(EXEC)

# Compile task_cli.cpp
$(EXEC): $(SRC)
	$(CXX) $(CXXFLAGS) $(SRC) -o $(EXEC)

# Compile test_task_cli.cpp
test: $(TEST_EXEC)

$(TEST_EXEC): $(TEST_SRC) $(SRC)
	$(CXX) $(CXXFLAGS) $(TEST_SRC) -o $(TEST_EXEC)

# Run tests
run_tests: $(TEST_EXEC)
	./$(TEST_EXEC)

# Clean build directory and output files
clean:
	rm -f $(EXEC) $(TEST_EXEC)

