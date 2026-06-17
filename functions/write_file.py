import os
import google.genai.types as types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:

    # Guardrail to make sure function only works in permitted directory
    wrkdir = os.path.abspath(working_directory)
    targetfile = os.path.normpath(os.path.join(wrkdir, file_path))
    try:
        if os.path.commonpath([wrkdir, targetfile]) != wrkdir:
            raise ValueError(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(targetfile) and os.path.isdir(targetfile):
            raise ValueError(f'Cannot write to "{file_path}" as it is a directory')

        # Success, write content to file, creates new path if need be
        os.makedirs(os.path.dirname(targetfile), exist_ok=True)
        with open(targetfile, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"