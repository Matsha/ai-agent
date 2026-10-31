import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        full_working_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(full_working_path, directory))

        if os.path.commonpath([full_working_path, target_dir]) != full_working_path:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        elif not os.path.isdir(target_dir):
            return f"Error: \"{target_dir}\" is not a directory"
        else:
            record = ""
            list_of_files = os.listdir(target_dir)
            for file in list_of_files:
                filepath = target_dir + "/" + file
                is_directory = os.path.isdir(filepath)
                filesize = os.path.getsize(filepath)
                record = record + f"- {file}: file_size={filesize} bytes, is_dir={is_directory}\n"
            return record


    except Exception as e1:
        return f"Error: {e1}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
