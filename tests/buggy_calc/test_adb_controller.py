import subprocess

import pytest

from logitech.buggy_calc.helpers.adb_controller import ADBController


class TestADBController:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.adb_controller = ADBController()

    def test_execute_command__returns_result(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_process = mocker.Mock()
        mock_run.return_value = mock_process

        result = self.adb_controller.execute_command(["adb", "devices"])
        mock_run.assert_called_once_with(
            ["adb", "devices"], capture_output=True, text=True, check=True, timeout=30
        )
        assert result == mock_process

    def test_execute_command__raises_TimeoutExpired(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="adb devices", timeout=30)

        with pytest.raises(RuntimeError):
            self.adb_controller.execute_command(["adb", "devices"])

    def test_execute_command__raises_CalledProcessError(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="adb devices"
        )

        with pytest.raises(RuntimeError):
            self.adb_controller.execute_command(["adb", "devices"])

    def test_get_ui_dump__returns_result(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_process = mocker.Mock()
        mock_process.stdout = mocker.Mock()
        mock_run.return_value = mock_process

        result = self.adb_controller.get_ui_dump()
        mock_run.assert_called_once_with(
            ["adb", "exec-out", "uiautomator", "dump", "/dev/tty"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        assert result == mock_process.stdout

    def test_tap_coordinates(self, mocker):
        mock_run = mocker.patch("subprocess.run")
        mock_process = mocker.Mock()
        mock_process.stdout = mocker.Mock()
        mock_run.return_value = mock_process
        X, Y = 1, 1

        self.adb_controller.tap_coordinates(X, Y)
        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "tap", str(X), str(Y)],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_launch_app(self, mocker):
        mock_app_name = "TEST"
        mock_activity = ".TestActivity"
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.launch_app(
            app_name=mock_app_name, activity_name=mock_activity
        )

        mock_run.assert_called_once_with(
            ["adb", "shell", "am", "start", "-n", f"{mock_app_name}/{mock_activity}"],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_close_app(self, mocker):
        mock_app_name = "TEST"
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.close_app(app_name=mock_app_name)

        mock_run.assert_called_once_with(
            ["adb", "shell", "am", "force-stop", mock_app_name],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    @pytest.mark.parametrize("input_value, expected_value", [("1", "1"), (1.0, "1.0")])
    def test_input_value(self, input_value, expected_value, mocker):
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.input_value(input_value)

        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "text", expected_value],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_del_value(self, mocker):
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.del_value()

        mock_run.assert_called_once_with(
            ["adb", "shell", "input", "keyevent", "67"],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_take_screenshot(self, mocker):
        mock_screenshot_name = "test"
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.take_screenshot(mock_screenshot_name)

        mock_run.assert_called_once_with(
            ["adb", "shell", "screencap", "-p", f"/sdcard/{mock_screenshot_name}.png"],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_pull_screenshot(self, mocker):
        mock_screenshot_name = "test"
        mock_log_dir = "test"
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.pull_screenshot(mock_screenshot_name, mock_log_dir)

        mock_run.assert_called_once_with(
            [
                "adb",
                "pull",
                f"/sdcard/{mock_screenshot_name}.png",
                f"{mock_log_dir}/{mock_screenshot_name}.png",
            ],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )

    def test_del_screenshot_from_device(self, mocker):
        mock_screenshot_name = "test"
        mock_run = mocker.patch("subprocess.run")

        self.adb_controller.del_screenshot_from_device(mock_screenshot_name)

        mock_run.assert_called_once_with(
            ["adb", "shell", "rm", f"/sdcard/{mock_screenshot_name}.png"],
            capture_output=False,
            text=True,
            check=True,
            timeout=30,
        )
