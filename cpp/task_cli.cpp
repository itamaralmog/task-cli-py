#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <nlohmann/json.hpp>
#include <sstream>
#include <limits>
#include <iomanip> // <-- Add this include for `setw`
#include "task_cli.hpp"

using json = nlohmann::json;
using namespace std;
int id = 1;

void initialize_id() {
    ifstream file(file_name);
    if (!file.is_open()) {
        cout << "JSON file not found. Starting fresh with ID = 1.\n";
        id = 1;
        return;
    }
    json data;
    file >> data;
    if (!data["tasks"].empty()) {
        int max_id = 0;
        for (auto& task : data["tasks"]) {
            max_id = max(max_id, task["ID"].get<int>());
        }
        id = max_id + 1;
    } else {
        id = 1;
    }
    cout << "Initialized ID to " << id << " based on existing tasks.\n";
    file.close();
}

void add_task(const string& description, const string& mark) {
    json data = load_data();
    data["tasks"].push_back({{"ID", id}, {"description", description}, {"mark", mark}});
    save_data(data);
    cout << "Task added: ID=" << id << ", Description=\"" << description << "\", Mark=\"" << mark << "\"\n";
    ++id;
}

void update_task(int task_id, const string& new_description) {
    json data = load_data();
    bool updated = false;
    for (auto& task : data["tasks"]) {
        if (task["ID"] == task_id) {
            task["description"] = new_description;
            updated = true;
            break;
        }
    }
    if (updated) {
        save_data(data);
        cout << "Task ID " << task_id << " updated successfully.\n";
    } else {
        cout << "Task ID " << task_id << " not found.\n";
    }
}

void delete_task(int task_id) {
    json data = load_data();
    size_t original_size = data["tasks"].size();
    data["tasks"].erase(remove_if(data["tasks"].begin(), data["tasks"].end(),
                                  [task_id](const json& task) { return task["ID"] == task_id; }),
                        data["tasks"].end());
    if (data["tasks"].size() < original_size) {
        save_data(data);
        cout << "Task ID " << task_id << " deleted successfully.\n";
    } else {
        cout << "Task ID " << task_id << " not found.\n";
    }
}

void mark_task(int task_id, const string& mark) {
    json data = load_data();
    bool updated = false;
    for (auto& task : data["tasks"]) {
        if (task["ID"] == task_id) {
            task["mark"] = mark;
            updated = true;
            break;
        }
    }
    if (updated) {
        save_data(data);
        cout << "Task ID " << task_id << " marked as \"" << mark << "\" successfully.\n";
    } else {
        cout << "Task ID " << task_id << " not found.\n";
    }
}

void show_list(const string& filter) {
    json data = load_data();
    int num = 1;
    for (const auto& task : data["tasks"]) {
        if (filter == "all" || task["mark"] == filter) {
            cout << num++ << ". ID=" << task["ID"] << ", Description=\"" << task["description"]
                 << "\", Mark=\"" << task["mark"] << "\"\n";
        }
    }
    if (num == 1) cout << "No tasks found.\n";
}

json load_data() {
    ifstream file(file_name);
    json data = {{"tasks", json::array()}};
    if (file.is_open()) {
        try {
            file >> data;
        } catch (...) {
            data["tasks"] = json::array();
        }
        file.close();
    }
    return data;
}

void save_data(const json& data) {
    ofstream file(file_name);
    file << setw(4) << data;
    file.close();
}
// #ifndef DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
// int main() {
//     initialize_id();
//     string command;
//     cout << "Task CLI initialized. Available commands: add, update, delete, mark, list, exit.\n";

//     while (true) {
//         cout << "task-cli> ";
//         getline(cin, command);
//         istringstream iss(command);
//         vector<string> tokens((istream_iterator<string>(iss)), istream_iterator<string>());

//         if (tokens.empty()) continue;

//         if (tokens[0] == "add" && tokens.size() > 1) {
//             string description = command.substr(4);
//             add_task(description);
//         } else if (tokens[0] == "update" && tokens.size() > 2) {
//             int task_id = stoi(tokens[1]);
//             string new_description = command.substr(command.find(tokens[2]));
//             update_task(task_id, new_description);
//         } else if (tokens[0] == "delete" && tokens.size() > 1) {
//             delete_task(stoi(tokens[1]));
//         } else if (tokens[0] == "mark-in-progress" && tokens.size() > 1) {
//             mark_task(stoi(tokens[1]), "in-progress");
//         } else if (tokens[0] == "mark-done" && tokens.size() > 1) {
//             mark_task(stoi(tokens[1]), "done");
//         } else if (tokens[0] == "list") {
//             if (tokens.size() > 1)
//                 show_list(tokens[1]);
//             else
//                 show_list();
//         } else if (tokens[0] == "exit") {
//             cout << "Exiting task CLI.\n";
//             break;
//         } else {
//             cout << "Unknown command. Available commands: add, update, delete, mark, list, exit.\n";
//         }
//     }

//     return 0;
// }
// #endif // DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN

