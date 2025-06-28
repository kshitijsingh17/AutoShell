# debug_subprocess_session.py

from session.subprocess_session import SubprocessSession

def main():
    shell = SubprocessSession()
    print("✅ Subprocess shell initialized.")

    while True:
        try:
            command = input("Enter command (or 'exit' to quit): ").strip()
            if command == "exit":
                break

            # Run command and get output
            exit_code = shell.write_stdin(command)
            stdout = shell.read_stdout()
            stderr = shell.read_stderr()

            print("\n--- STDOUT ---")
            print(stdout.strip())

            print("\n--- STDERR ---")
            print(f"\033[91m{stderr.strip()}\033[0m")  # Red color

            print(f"\n[exit code] {exit_code}")

            # Flush for next command
            shell.flush_stdout()
            shell.flush_stderr()

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break

    shell.terminate()

if __name__ == "__main__":
    main()
