#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"  // Include doctest header
// #include "task_cli.hpp" for makefile
#include "task_cli.cpp"  // Include your task CLI implementation
#include <fstream>
#include <nlohmann/json.hpp>
#include <string>

using json = nlohmann::json;
using namespace std;

// const string file_name = "tasks.json";
void print_json_file(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Could not open the file " << filename << std::endl;
        return;
    }

    try {
        nlohmann::json j;
        file >> j;
        std::cout << "Contents of " << filename << ":\n" << j.dump(4) << std::endl;  // Pretty print with indentation
    } catch (const std::exception& e) {
        std::cerr << "Error parsing JSON from " << filename << ": " << e.what() << std::endl;
    }
}
// Helper functions for setup and teardown
void setup_file() {
    ifstream file(file_name);
    if (!file.is_open()) {
        json data = {{"tasks", json::array()}};
        ofstream out_file(file_name);
        out_file << setw(4) << data;
        out_file.close();
    }
}

void teardown_file() {
    if (remove(file_name.c_str()) != 0) {
        perror("Error deleting file");
    }
}

json load_tasks() {
    ifstream file(file_name);
    json data;
    file >> data;
    return data["tasks"];
}

// Test cases
TEST_CASE("Initialize ID starts at 1") {
    teardown_file();
    initialize_id();
    CHECK(id == 1);
}

TEST_CASE("Add a task successfully") {
    setup_file();
    initialize_id();
    add_task("First Task", "todo");
    json tasks = load_tasks();
    CHECK(tasks.size() == 1);
    CHECK(tasks[0]["description"] == "First Task");
    CHECK(tasks[0]["mark"] == "todo");
}

TEST_CASE("Update a task description") {
    setup_file();
    initialize_id();
    add_task("Task to Update", "todo");
    update_task(1, "Updated Task");
    json tasks = load_tasks();
    CHECK(tasks[0]["description"] == "Updated Task");
}

TEST_CASE("Delete a task") {
    setup_file();
    initialize_id();
    add_task("Task to Delete", "todo");
    delete_task(3);
    json tasks = load_tasks();
    CHECK(tasks.size() == 2);
}

TEST_CASE("Mark a task as in-progress") {
    setup_file();
    initialize_id();
    add_task("Task to Mark", "todo");
    mark_task(1, "in-progress");
    json tasks = load_tasks();
    CHECK(tasks[0]["mark"] == "in-progress");
}

TEST_CASE("Mark a task as done") {
    setup_file();
    initialize_id();
    add_task("Task to Complete", "todo");
    mark_task(1, "done");
    json tasks = load_tasks();
    CHECK(tasks[0]["mark"] == "done");
}

TEST_CASE("Show all tasks") {
    setup_file();
    initialize_id();
    add_task("Task 1", "todo");
    add_task("Task 2", "in-progress");

    stringstream buffer;
    streambuf* old = cout.rdbuf(buffer.rdbuf());
    show_list("all");
    cout.rdbuf(old);

    string output = buffer.str();
    CHECK(output.find("Task 1") != string::npos);
    CHECK(output.find("Task 2") != string::npos);
}

TEST_CASE("Show filtered tasks") {
    setup_file();
    initialize_id();
    add_task("Task 1", "todo");
    add_task("Task 2", "in-progress");

    stringstream buffer;
    streambuf* old = cout.rdbuf(buffer.rdbuf());
    show_list("todo");
    cout.rdbuf(old);

    string output = buffer.str();
    CHECK(output.find("Task 1") != string::npos);
    CHECK(output.find("Task 2") == string::npos);
}

TEST_CASE("Handle update of a nonexistent task") {
    setup_file();
    initialize_id();
    update_task(99, "Nonexistent Task");
    json tasks = load_tasks();
    // print_json_file(file_name);
    CHECK(tasks.size() == 8);
}

TEST_CASE("Handle deletion of a nonexistent task") {
    setup_file();
    initialize_id();
    delete_task(99);
    json tasks = load_tasks();
    // print_json_file(file_name);
    CHECK(tasks.size() == 8);
}

TEST_CASE("Handle marking a nonexistent task") {
    setup_file();
    initialize_id();
    mark_task(99, "done");
    json tasks = load_tasks();
    // print_json_file(file_name);
    CHECK(tasks.size() == 8);
}

TEST_CASE("Add multiple tasks") {
    setup_file();
    initialize_id();
    add_task("Task 1", "todo");
    add_task("Task 2", "todo");
    json tasks = load_tasks();
    // print_json_file(file_name);
    CHECK(tasks.size() == 10);
    CHECK(tasks[8]["description"] == "Task 1");
    CHECK(tasks[9]["description"] == "Task 2");
}

TEST_CASE("Update a marked task") {
    setup_file();
    initialize_id();
    add_task("Task to Update and Mark", "todo");
    mark_task(11, "in-progress");
    update_task(11, "Updated Task");
    json tasks = load_tasks();
    // print_json_file(file_name);
    CHECK(tasks[10]["description"] == "Updated Task");
    CHECK(tasks[10]["mark"] == "in-progress");
}
