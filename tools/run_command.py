from session.subprocess_session import SubprocessSession

def run_command(shell: SubprocessSession, command: str) -> dict:
    print(f"[DEBUG] ➜ Executing command: {command}")
    exit_code = shell.write_stdin(command)
    print(f"[DEBUG] ↩ Exit code: {exit_code}")
    stdout = shell.read_stdout().strip()
    stderr = shell.read_stderr().strip()
    print(f"[DEBUG] STDOUT:\n{stdout}")
    print(f"[DEBUG] STDERR:\n{stderr}")
    shell.flush_stdout()
    shell.flush_stderr()

    return {
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr
    }
