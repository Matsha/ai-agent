import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        full_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(full_working_path, file_path))

        if os.path.commonpath([full_working_path, target_file]) != full_working_path:
            return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
        elif os.path.isdir(target_file):
            return f"Error: Cannot write to \"{file_path}\" as it is a directory"

        os.makedirs(file_path, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        raise Exception(f"Error: {e}")
