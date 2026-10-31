import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        full_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(full_working_path, file_path))

        if os.path.commonpath([full_working_path, target_file]) != full_working_path:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        elif not os.path.isfile(target_file):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        elif not file_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"

        command = ["python", target_file]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        elif result.stderr == "" and result.stdout == "":
            return "No output produced"
        else:
            return_string = "STDOUT:" + result.stdout + "\nSTDERR:" + result.stderr
            return return_string


    except Exception as e:
        raise Exception(f"Error:{e}")
