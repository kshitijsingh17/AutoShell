from mcp.server.fastmcp import FastMCP
from session.subprocess_session import SubprocessSession 
from tools.run_command import run_command
from tools.get_cwd import get_current_directory

# Start the subprocess shell session
print(13)
shell = SubprocessSession()
print("🔧 Subprocess shell session started. Type 'exit' to quit.\n")

# Initialize FastMCP
mcp = FastMCP("shell")


@mcp.tool()
def execute_command(cmd: str):
    """
    Executes a command in the shell and returns its output, error, and exit code.
    All buffers are flushed after execution.

    Args:
        command: The shell command to execute

    Returns:
        A dictionary with stdout, stderr, and exit_code
    """
    return run_command(shell, cmd)


@mcp.tool()
def get_cwd():
    """
    Returns the current working directory.

    Args:
        None

    Returns:
        The current working directory as a string, or an error message.
    """
    return get_current_directory(shell)


if __name__ == "__main__":
    mcp.run(transport="stdio")
