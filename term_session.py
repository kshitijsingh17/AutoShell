import subprocess
import threading
import sys
import queue

class ShellSession:
    def __init__(self):
        self.proc = subprocess.Popen(
            ['bash'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )

        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.running = True

        # Start readers for stdout and stderr
        threading.Thread(target=self._reader, args=(self.proc.stdout, self.stdout_queue), daemon=True).start()
        threading.Thread(target=self._reader, args=(self.proc.stderr, self.stderr_queue), daemon=True).start()

    def _reader(self, stream, output_queue):
        """Reads lines from a stream and stores in a thread-safe queue."""
        for line in iter(stream.readline, ''):
            output_queue.put(line.rstrip())

    def write_command(self, cmd: str):
        """Send a command to the shell."""
        if self.proc.stdin:
            self.proc.stdin.write(cmd + '\n')
            self.proc.stdin.flush()

    def read_output(self):
        RED = '\033[91m'
        RESET = '\033[0m'
        """Read and print all lines from stdout and stderr queues."""
        while not self.stdout_queue.empty():
            print(f"{self.stdout_queue.get()}\n")

        while not self.stderr_queue.empty():
            print(f"{RED}{self.stderr_queue.get()}{RESET}\n")

    def run(self):
        print("🔧 Terminal session started. Type 'exit' to quit.\n")

        try:
            while self.running:
                user_input = input("> ")
                #print(f"> {user_input}")  # show command again as part of transcript

                if user_input.strip() == "exit":
                    self.running = False

                self.write_command(user_input)

                # Small wait to allow output to queue up
                self.proc.stdin.flush()
                self.proc.stdout.flush()
                self.proc.stderr.flush()

                # Wait for output to appear
                import time
                time.sleep(0.3)

                self.read_output()

        except KeyboardInterrupt:
            print("\n[!] Session interrupted.")
            self.running = False

        self.proc.terminate()
        print("\n🛑 Terminal session ended.")

# Run the terminal
if __name__ == '__main__':
    ShellSession().run()
