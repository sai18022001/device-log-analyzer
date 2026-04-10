#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <chrono>
#include <thread>
#include <sstream>
#include <iomanip>
#include "log_entry.h"

std::string current_timestamp() {
    auto now = std::chrono::system_clock::now();
    std::time_t t = std::chrono::system_clock::to_time_t(now);
    std::tm tm_buf;
#ifdef _WIN32
    localtime_s(&tm_buf, &t);
#else
    localtime_r(&t, &tm_buf);
#endif
    std::ostringstream oss;
    oss << std::put_time(&tm_buf, "%Y-%m-%dT%H:%M:%S");
    return oss.str();
}

std::string random_severity() {
    int r = rand() % 10;
    if (r < 6) return "INFO";
    if (r < 9) return "WARN";
    return "ERROR";
}

std::string random_device() {
    std::vector<std::string> devices = { "dev_01", "dev_02", "dev_03", "dev_04" };
    return devices[rand() % devices.size()];
}

std::string random_message(const std::string& severity) {
    std::vector<std::string> info_msgs = {
        "System boot complete",
        "Heartbeat OK",
        "Sensor reading normal",
        "Config loaded successfully",
        "Network connection stable"
    };
    std::vector<std::string> warn_msgs = {
        "CPU temperature high",
        "Memory usage above 80%",
        "Retrying network connection",
        "Disk space below threshold"
    };
    std::vector<std::string> error_msgs = {
        "Sensor read failure",
        "Network timeout",
        "Checksum mismatch detected",
        "Watchdog timer expired"
    };

    if (severity == "INFO")  return info_msgs[rand() % info_msgs.size()];
    if (severity == "WARN")  return warn_msgs[rand() % warn_msgs.size()];
    return error_msgs[rand() % error_msgs.size()];
}

std::string escape_json(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (c == '"') out += "\\\"";
        else out += c;
    }
    return out;
}

int main() {
    srand(static_cast<unsigned>(time(nullptr)));

    while (true) {
        LogEntry entry;
        entry.timestamp = current_timestamp();
        entry.device_id = random_device();
        entry.severity = random_severity();
        entry.message = random_message(entry.severity);

        // Print as JSON line — Python ingestor reads this from stdout
        std::cout << "{"
            << "\"timestamp\":\"" << escape_json(entry.timestamp) << "\","
            << "\"device_id\":\"" << escape_json(entry.device_id) << "\","
            << "\"severity\":\"" << escape_json(entry.severity) << "\","
            << "\"message\":\"" << escape_json(entry.message) << "\""
            << "}" << std::endl;

        std::this_thread::sleep_for(std::chrono::milliseconds(800));
    }

    return 0;
}