from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file
import json
from collections.abc import Callable

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

def call_function(tool_call, verbose: bool = False) -> dict:
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments or "{}")
    id = tool_call.id

    if verbose == True:
        print(f" - Calling function: {func_name}({func_args})")
    print(f" - Calling function: {func_name}")

    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file
    }
    if func_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": id,
            "content": f"Error: Unknown function: {func_name}",
        }

    func_args["working_directory"] = "./calculator"
    result = function_map[func_name](**func_args)
    return {
        "role": "tool",
        "tool_call_id": id,
        "content": result,
    }
