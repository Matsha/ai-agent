import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        full_working_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(full_working_path, file_path))

        if os.path.commonpath([full_working_path, target_file]) != full_working_path:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        elif not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
        else:
            f = open(target_file)
            content = f.read(10_000)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at 10,000 characters]'
            print(content)
            return content

    except Exception as err:
        raise Exception(f"Error: {err}")
