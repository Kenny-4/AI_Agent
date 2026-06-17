import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to retrieve content from, relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:

    # Guardrail to make sure function only works in permitted directory
    wrkdir = os.path.abspath(working_directory)
    targetfile = os.path.normpath(os.path.join(wrkdir, file_path))
    try:
        if os.path.commonpath([wrkdir, targetfile]) != wrkdir:
            raise ValueError(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(targetfile):
            raise ValueError(f'File not found or is not a regular file: "{file_path}"')

        # Success, read file content (up to 10000 chars)
        with open(targetfile, 'r') as f:
            content = f.read(10000)
            if f.read(1) != "":
                content += f'[...File "{file_path}" truncated at 10000 characters]'
        return content
    
    except Exception as e:
        return f"Error: {e}"
