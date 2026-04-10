#pragma once
#include <string>

struct LogEntry {
    std::string timestamp;
    std::string device_id;
    std::string severity;   // INFO, WARN, ERROR
    std::string message;
};