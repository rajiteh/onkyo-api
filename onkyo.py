"""
Onkyo command execution module.
Handles communication with Onkyo receivers via the eiscp protocol.
"""

import logging
import re
import subprocess
import warnings
from typing import Union, Optional, Dict, Any

# Filter out SyntaxWarnings from dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _parse_response(output: str) -> Dict[str, Any]:
    """
    Parse onkyo command response.

    Expected format: "RECEIVER-NAME: command = value"

    Args:
        output: Raw output from onkyo command

    Returns:
        Dictionary with parsed response
    """
    output = output.strip()

    # Try to parse the standard format: "RECEIVER: command = value"
    match = re.match(r"^(.+?):\s*(.+?)\s*=\s*(.+)$", output)
    if match:
        receiver_name, command, value = match.groups()
        return {
            "success": True,
            "receiver": receiver_name.strip(),
            "command": command.strip(),
            "value": value.strip(),
            "raw": output,
        }

    # If parsing fails, return raw output
    return {"success": True, "raw": output}


def runCommand(
    command: str, host: Optional[str] = None, port: Optional[int] = None
) -> Union[str, dict]:
    """
    Execute an onkyo command and return the result.

    Args:
        command: The command string to send to the Onkyo receiver
        host: Optional hostname or IP address of the receiver
        port: Optional port number (default is 60128)

    Returns:
        The command output as a string, or error dict if command fails

    Examples:
        >>> runCommand("power on")
        >>> runCommand("power on", host="192.168.1.100")
        >>> runCommand("volume 20", host="onkyo.local", port=60128)
    """
    try:
        # Check if this is a query command (expects response)
        is_query = "=query" in command.lower() or command.strip().endswith("=query")

        # Build the command array safely
        cmd = ["onkyo"]

        # Add host and port if provided (as separate arguments for safety)
        if host:
            cmd.append("--host")
            cmd.append(str(host))
        if port is not None:
            cmd.append("--port")
            cmd.append(str(port))

        # Add the actual command
        cmd.append(command)

        logger.info(f"Executing onkyo command: {' '.join(cmd)} (query={is_query})")

        # Execute with proper argument list (not shell)
        # Capture stdout and stderr separately
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10 if is_query else 5,  # Longer timeout for query commands
            shell=False,  # Explicitly disable shell for security
        )

        # Log stderr if present
        if result.stderr:
            logger.warning(f"Command stderr: {result.stderr.strip()}")

        # Check if command failed
        if result.returncode != 0:
            error_msg = f"Command failed with exit code {result.returncode}"
            error_response = {
                "success": False,
                "error": error_msg,
                "command": command,
                "exit_code": result.returncode,
            }
            # Include stdout if present
            if result.stdout:
                error_response["stdout"] = result.stdout.strip()
            # Include stderr if present
            if result.stderr:
                error_response["stderr"] = result.stderr.strip()

            logger.error(
                f"{error_msg}, stdout: {result.stdout.strip()}, stderr: {result.stderr.strip()}"
            )
            return error_response

        # For query commands, parse and return the response
        if is_query:
            logger.info(f"Query result: {result.stdout.strip()}")
            if result.stdout.strip():
                return _parse_response(result.stdout)
            else:
                return {"success": True, "raw": ""}

        # For non-query commands, just return success
        logger.info(f"Command executed successfully")
        return {"success": True}

    except subprocess.TimeoutExpired:
        error_msg = f"Command timed out: {command}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg, "command": command}
    except FileNotFoundError:
        error_msg = "onkyo command not found. Is onkyo-eiscp installed?"
        logger.error(error_msg)
        return {"success": False, "error": error_msg, "command": command}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg, "command": command}
