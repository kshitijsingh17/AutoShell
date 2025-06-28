import os
import subprocess
import threading

class SubprocessSession:
    def __init__(self):
        self.process = subprocess.Popen(
            ["bash"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,  # Detach from parent terminal session
            text=True,             # Handle strings, not bytes
            bufsize=1              # Line-buffered output
        )

        self.stdout_buffer = ""
        self.stderr_buffer = ""
        self.lock = threading.Lock()

        threading.Thread(target=self._read_stdout, daemon=True).start()
        threading.Thread(target=self._read_stderr, daemon=True).start()

    def _read_stdout(self):
        for line in self.process.stdout:
            with self.lock:
                self.stdout_buffer += line

    def _read_stderr(self):
        for line in self.process.stderr:
            with self.lock:
                self.stderr_buffer += line

    # def write_stdin(self, command: str) -> int:
    #     print('hi')
    #     marker = "__RET:$?__"
    #     full_command = f"{command}\necho {marker} $?\n"

    #     # Clear output buffers first
    #     self.flush_stdout()
    #     self.flush_stderr()

    #     if self.process.stdin:
    #         self.process.stdin.write(full_command)
    #         self.process.stdin.flush()

    #     # Wait for marker to appear
    #     import time
    #     while True:
    #         time.sleep(0.05)
    #         with self.lock:
    #             if marker in self.stdout_buffer:
    #                 break

    #     # Extract and return the exit code
    #     with self.lock:
    #         lines = self.stdout_buffer.splitlines()
    #         for line in reversed(lines):
    #             if line.startswith(marker):
    #                 try:
    #                     return int(line.replace(marker, "").strip())
    #                 except ValueError:
    #                     return -1  # Parsing failed
    #     return -1  # Fallback
    # def write_stdin(self, command: str) -> int:
    #     try:
    #         if self.process.stdin:
    #             self.process.stdin.write(command + "\n")
    #             self.process.stdin.flush()
    #         return 200  # Success code (arbitrary)
    #     except Exception as e:
    #         print(f"❌ Error writing to stdin: {e}")
    #         return -1
    def write_stdin(self, command: str) -> int:
        try:
            marker = "__CMD_DONE__"
            full_command = f"{command}\necho {marker}\n"

            # Clear output buffers before writing
            self.flush_stdout()
            self.flush_stderr()

            if self.process.stdin:
                self.process.stdin.write(full_command)
                self.process.stdin.flush()

            # Wait for the marker to appear in stdout
            import time
            timeout = 5  # seconds
            waited = 0
            while waited < timeout:
                time.sleep(0.1)
                waited += 0.1
                with self.lock:
                    if marker in self.stdout_buffer:
                        return 200  # Simulate success

            print("⚠️ Timeout: Marker not detected")
            return -1  # Timeout occurred
        except Exception as e:
            print(f"❌ Error writing to stdin: {e}")
            return -1



    def read_stdout(self) -> str:
        with self.lock:
            return self.stdout_buffer

    def flush_stdout(self):
        with self.lock:
            self.stdout_buffer = ""

    def read_stderr(self) -> str:
        with self.lock:
            return self.stderr_buffer

    def flush_stderr(self):
        with self.lock:
            self.stderr_buffer = ""

    def terminate(self):
        self.process.terminate()

    def is_alive(self):
        return self.process.poll() is None
