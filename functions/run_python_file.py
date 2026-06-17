import os
import subprocess
from sys import stderr
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
        },
    ),
)

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    # Guardrail to make sure function only works in permitted directory
    wrkdir = os.path.abspath(working_directory)
    targetfile = os.path.normpath(os.path.join(wrkdir, file_path))
    try:
        if os.path.commonpath([wrkdir, targetfile]) != wrkdir:
            raise ValueError(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(targetfile):
            raise ValueError(f'Cannot execute "{file_path}" does not exist or is not a regular file')
        if not targetfile.endswith(".py"):
            raise ValueError(f'Cannot execute "{file_path}" is not a Python file')
        
        # Success, now build the command
        command = ["python", targetfile]
        # add args if exist
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return result.stdout + f" Process exited with code {result.returncode}"
        elif result.stdout and stderr == "":
            return "No output produced."
        else:
            return f"STDOUT: {result.stdout} STDERR: {result.stderr} \n"

    except Exception as e:
        return f"Error: executing Python file: {e}"