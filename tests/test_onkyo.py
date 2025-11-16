"""Tests for the onkyo module."""

from unittest.mock import patch, MagicMock
import subprocess
import onkyo


def test_parse_response():
    """Test response parsing."""
    # Test standard format
    result = onkyo._parse_response("TX-NR7100: master-volume = 125")
    assert result["success"] is True
    assert result["receiver"] == "TX-NR7100"
    assert result["command"] == "master-volume"
    assert result["value"] == "125"
    assert result["raw"] == "TX-NR7100: master-volume = 125"

    # Test with different spacing
    result = onkyo._parse_response("MY-RECEIVER:   power   =   on")
    assert result["success"] is True
    assert result["receiver"] == "MY-RECEIVER"
    assert result["command"] == "power"
    assert result["value"] == "on"

    # Test unparseable format
    result = onkyo._parse_response("some random output")
    assert result["success"] is True
    assert result == {"success": True, "raw": "some random output"}


def test_runCommand_non_query():
    """Test non-query command execution."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on")
        assert result == {"success": True}


def test_runCommand_query():
    """Test query command execution."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "TX-NR7100: master-volume = 125\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("master-volume=query")
        assert isinstance(result, dict)
        assert result["success"] is True
        assert result["receiver"] == "TX-NR7100"
        assert result["command"] == "master-volume"
        assert result["value"] == "125"


def test_runCommand_query_empty_response():
    """Test query command with empty response."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power=query")
        assert result["success"] is True
        assert result == {"success": True, "raw": ""}


def test_runCommand_with_host():
    """Test command execution with host parameter."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on", host="192.168.1.100")
        assert result == {"success": True}
        # Verify host was added to command as separate arguments
        args = mock_run.call_args[0][0]
        assert args == ["onkyo", "--host", "192.168.1.100", "power on"]


def test_runCommand_with_host_and_port():
    """Test command execution with host and port parameters."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("volume 20", host="onkyo.local", port=60128)
        assert result == {"success": True}
        # Verify host and port were added to command as separate arguments
        args = mock_run.call_args[0][0]
        assert args == ["onkyo", "--host", "onkyo.local", "--port", "60128", "volume 20"]


def test_runCommand_with_only_port():
    """Test command execution with only port parameter."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on", port=60128)
        assert result == {"success": True}
        # Verify port was added to command
        args = mock_run.call_args[0][0]
        assert args == ["onkyo", "--port", "60128", "power on"]


def test_runCommand_with_stderr():
    """Test command execution with stderr output."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = "some warning\n"
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on")
        # Should still return success
        assert result == {"success": True}


def test_runCommand_timeout():
    """Test command timeout handling."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.TimeoutExpired("onkyo", 10)
        result = onkyo.runCommand("power on")
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result
        assert "timed out" in result["error"]


def test_runCommand_not_found():
    """Test handling when onkyo command is not found."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError()
        result = onkyo.runCommand("power on")
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result
        assert "not found" in result["error"]


def test_runCommand_failed():
    """Test handling when command fails."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "some output"
        mock_result.stderr = "error message"
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on")
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result
        assert "exit code 1" in result["error"]
        assert result["exit_code"] == 1
        assert result["stdout"] == "some output"
        assert result["stderr"] == "error message"


def test_runCommand_failed_no_output():
    """Test handling when command fails with no output."""
    with patch("subprocess.run") as mock_run:
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        result = onkyo.runCommand("power on")
        assert isinstance(result, dict)
        assert result["success"] is False
        assert "error" in result
        assert "exit code 1" in result["error"]
        assert result["exit_code"] == 1
        # stdout and stderr keys should not be present if empty
        assert "stdout" not in result or result.get("stdout") == ""
        assert "stderr" not in result or result.get("stderr") == ""
