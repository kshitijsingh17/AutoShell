from session.subprocess_session import SubprocessSession

def get_current_directory(shell: SubprocessSession) -> str:
    exit_code = shell.write_stdin("pwd")
    stdout = shell.read_stdout().strip()
    stderr = shell.read_stderr().strip()

    shell.flush_stdout()
    shell.flush_stderr()

    if exit_code == 0:
        return stdout
    else:
        return f"[error] Failed to get cwd: {stderr or stdout}"
