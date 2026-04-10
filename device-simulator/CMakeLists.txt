cmake_minimum_required(VERSION 3.20)
project(DeviceSimulator)

set(CMAKE_CXX_STANDARD 17)

add_executable(device_simulator
    src/log_generator.cpp
)

target_include_directories(device_simulator PRIVATE include)