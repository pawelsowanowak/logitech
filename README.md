# Project Requirements & Setup

## Python Requirements
- **Python Version:** 3.12.x
- **Dependencies:** `dependency.py312.lock`
- **Virtual Environment:** Recommended (`pyenv`)

## Hardware Requirements
- **Device:** Android Device or Emulator
- **Android Version:** 7.0+ (API level 24+)

---

## Setup Instructions

```bash
git clone https://github.com/pawelsowanowak/logitech.git
cd logitech
pip install -r dependencies.py312.lock
pip install .
```

---

## Install Calculator APK & Verify

```bash
adb install buggy_calc_debug.apk
adb shell pm list packages com.admsqa.buggycalc
```

## How to Run Tests

**All tests (with logs):**
```bash
./scripts/run_all_tests.sh
```

**Mobile Application Testing (Task 1):**
```bash
pytest tests/buggy_calc/E2E/test_e2e.py -v
```

**API Testing (Task 2):**
```bash
pytest tests/api/test_user.py -v
```

**Gherkin Scenarios (Task 3):**
```bash
behave --format=pretty --outfile=logs/behave/bdd_calculator.txt
```

---

## Logs Directory Structure

```
logitech/
└── logs/
    ├── automation/
    │   ├── adb_controller.log
    │   ├── calculator.py
    │   ├── ui_parser.py
    │   └── parser.py
    ├── device/
    │   ├── logcat_dump.txt
    │   └── package_details.txt
    ├── behave/
    │   └── bdd_calculator.txt
    └── screenshots/
        └── <scenario-name>.png
```

### automation
- `adb_controller.log` – ADB command trace (install, start, tap, etc.)
- `calculator.py` – Debug logs emitted by the calculator page object
- `ui_parser.py` – UI XML dump parsing results
- `parser.py` – Helper logs (argument parsing, config loading)

### device
- `logcat_dump.txt` – Full logcat snapshot with timestamps
- `package_details.txt` – Output of `adb shell dumpsys package <com.admsqa.buggycalc>`

### behave
- Human-readable Behave reports

### screenshots
- `<scenario-name>.png` auto-captured after each BDD scenario

---

## Potential Improvements

- **Speed up test execution**
- **Prevent log overwrites:** Append `YYYYMMDD_HHMMSS` to each log file (e.g., `adb_controller_20250818_2115.log`)
- **Multi-Python-Version Support:** Broaden compatibility from 3.9 → 3.12
