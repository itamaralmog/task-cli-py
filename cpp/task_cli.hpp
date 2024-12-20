#ifndef TASK_CLI_H
#define TASK_CLI_H

#ifndef DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
    #define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
    #include "doctest.h"
#endif

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <nlohmann/json.hpp>
#include <sstream>
#include <limits>
#include <iomanip> // <-- Add this include for `setw`

using json = nlohmann::json;
using namespace std;

const string file_name = "tasks.json";
extern int id; // Declare 'id' to be used in source file

// Task structure
struct Task {
    int ID;
    string description;
    string mark;
};

// Function declarations
void initialize_id();
void add_task(const string& description, const string& mark = "todo");
void update_task(int task_id, const string& new_description);
void delete_task(int task_id);
void mark_task(int task_id, const string& mark);
void show_list(const string& filter = "all");
json load_data();
void save_data(const json& data);

#endif // TASK_CLI_H
