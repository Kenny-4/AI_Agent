#AI Agent

This is a simple AI agent using Google Gemini's API to perform standard filesystem functions.

##HOW TO USE
 uv run main.py "Ask the model to do something here"
(Don't forget to activate the python environment beforehand)

You will see the functions that the AI model calls, and the AI's text response afterwards.

##Functionality
THe AI is set to work in the PLAYGROUND folder. It can utilize four commands:

- get_file_contents.py: Reads a file up to 10,000 characters.

- get_files_info.py: Feeds information of a directory/file displaying name, size (in bytes), and if it is a directory.

- run_python_file.py: Runs a python file, returns the output to model.

- write_file.py: Modifies a given file or creates a new one.

Other things to note:

- PLAYGROUND: This is the directory the agent will work in. For security, this agent is hardcoded to access this folder exclusively.

- prompts.py: This is the initial prompt that explains the AI what it's role is. Change it as you see fit.

If you want to add more functionality, you can add a python file in the "functions" folder. Make sure to implement a schema that works with the API, and add the function and it's schema in call_function.py. Don't forget to update prompts.py as well to let the model know it exists.'


Credit to [Boot.dev](https://www.boot.dev) for this guided project.

