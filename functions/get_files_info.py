import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    # Guardrail to make sure function only works in permitted directory
    wrkdir = os.path.abspath(working_directory)
    targetdir = os.path.normpath(os.path.join(wrkdir, directory))
    try:
        if os.path.commonpath([wrkdir, targetdir]) != wrkdir:
            raise ValueError(f'Cannot list "{directory}" as it is outside the permitted working directory')
        if not os.path.isdir(targetdir):
            raise ValueError(f'"{directory}" is not a directory')
        
        # Success, list file/directory info
        output = ""
        for item in os.listdir(targetdir):
            path = os.path.join(targetdir, item)
            output += f" - {item}: file_size= {os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}\n"
        return output

    except Exception as e:
        return f"Error: {e}"
    
    
