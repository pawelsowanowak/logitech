#!/usr/bin/env bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)
PROJECT_ROOT=$(cd -- "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd)
APP_PACKAGE="com.admsqa.buggycalc"
LOG_DIR="$PROJECT_ROOT/logs"
RED='\033[0;31m'
GREEN='\033[0;32m'


check_device_connection() {
    if ! command -v adb &> /dev/null; then
        echo -e "${RED}ERROR: ADB not found. Please install Android SDK platform-tools"
        exit 1
    fi

    if ! adb devices | grep -w "device"; then
        echo -e "${RED}ERROR: No Android device connected or device not authorized"
        exit 1
    fi

    echo -e "${GREEN}Android device connected"
}

check_device_connection
    pushd "$PROJECT_ROOT"
    mkdir -p "$LOG_DIR"
    mkdir -p "$LOG_DIR/device"

    echo "========= Running API Tests ========="
    pytest tests/api/test_user.py -v

    echo "========= Running Calculator E2E Tests ========="
    pytest tests/buggy_calc/test_e2e.py -v

    echo "========= Running BDD Tests ========="
    behave --format=pretty --outfile=logs/behave/bdd_calculator.txt

    echo "========= Collecting complete logcat dump ========="
    adb.exe logcat -d -v time > "$LOG_DIR/device/logcat_dump.txt" 2>&1

    echo "========= Collecting package details information ========="
    adb shell dumpsys package "$APP_PACKAGE" > "$LOG_DIR/device/package_details.txt" 2>&1
