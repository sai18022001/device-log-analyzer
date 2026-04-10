#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "log_entry.h"

TEST_CASE("LogEntry fields are set correctly") {
    LogEntry e;
    e.timestamp = "2024-01-01T00:00:00";
    e.device_id = "dev_01";
    e.severity = "ERROR";
    e.message = "Sensor read failure";

    CHECK(e.severity == "ERROR");
    CHECK(e.device_id == "dev_01");
}