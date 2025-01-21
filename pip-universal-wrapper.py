#!/usr/bin/env python3

import subprocess
import sys
import shutil
import os


def check_python_version():
    """Ensure the script is running on Python 3."""
    if sys.version_info.major < 3:
        print("Error: This script requires Python 3. Please run it with Python 3.")
        sys.exit(1)


def show_help():
    """Displays help information for using the script."""
    help_text = """
Usage: python pip-universal-wrapper.py --exec <program> [additional arguments...]

Arguments:
  --exec             Executes the specified pip-installed program with the following arguments.
  additional args    Any additional arguments to pass to the program.
  
Examples:
  python pip_wrapper.py --exec <program>  # Executes a pip-installed program
"""
    print(help_text)


def execute_pip_program(program_name, *args):
    """Executes a pip-installed program."""
    try:
        # Detect if we are on Windows or Linux
        is_windows = os.name == 'nt'

        if is_windows:
            # On Windows, try to find the program in the PATH
            program_path = shutil.which(program_name)
            if not program_path:
                raise FileNotFoundError(f"Program '{program_name}' not found in PATH.")

            print(f"Executing pip-installed program on Windows: {program_name}")
            subprocess.check_call([program_path] + list(args), shell=True)
            print(f"Program '{program_name}' executed successfully on Windows.")

        else:
            # On Linux, check pip standard locations
            user_bin_dir = os.path.expanduser("~/.local/bin")  # User-level install location
            system_bin_dir = "/usr/local/bin"  # System-level install location (commonly used)

            # Check if the program exists in the standard pip installation directories
            pip_bin_dir = user_bin_dir if os.path.exists(user_bin_dir) else system_bin_dir
            program_path = shutil.which(program_name, path=pip_bin_dir)

            if program_path:
                print(f"Executing pip-installed program on Linux: {program_name}")
                subprocess.check_call([program_path] + list(args))
                print(f"Program '{program_name}' executed successfully on Linux.")
            else:
                raise FileNotFoundError(f"Program '{program_name}' not found in pip-installed locations.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error: Program '{program_name}' failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    # Check Python version
    check_python_version()

    # Ensure the --exec argument is provided
    if len(sys.argv) < 3 or sys.argv[1] != '--exec':
        print("Error: Missing '--exec' argument or program name.")
        show_help()
        sys.exit(1)

    try:
        # Handle --exec argument
        exec_index = sys.argv.index("--exec") + 1
        if exec_index < len(sys.argv):
            program_name = sys.argv[exec_index]
            arguments = sys.argv[exec_index + 1:]  # All arguments after the program name
            execute_pip_program(program_name, *arguments)
        else:
            print("Error: No program specified after '--exec'.")
            sys.exit(1)

    except ValueError:
        print("Error: Unexpected argument structure.")
        sys.exit(1)


if __name__ == "__main__":
    main()
