from email import parser
import os
import argparse
from turtle import done
from dotenv import load_dotenv
from google import genai
from google.genai import types
import prompts
from call_function import available_functions, call_function

def call_agent(client, userprompt, args, messages):
    try:
        response = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=prompts.system_prompt, temperature=0))
        if not response.usage_metadata:
            raise RuntimeError("Failed API request.")
        
        # Update message history
        if response.candidates and len(response.candidates) > 0:
            messages.append(response.candidates[0].content)

        # Displays response, if verbose enabled, input and token stats as well
        if args.verbose is True:
            print(f"**User prompt: [\n{userprompt}\n]")
            print(f"**Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"**Response tokens: {response.usage_metadata.candidates_token_count}")
            if response.text:
                print(f"**Response text: [\n{response.text}\n]")

        # Handles function calls
        function_history = []
        if response.function_calls is not None:
            for function in response.function_calls:
                function_call_result = call_function(function, verbose=args.verbose)
                if function_call_result.parts is None:
                    raise Exception("Function call failed")
                elif function_call_result.parts[0].function_response is None:
                    raise Exception("Function call failed.")
                elif function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function call failed.")
                else:
                    # Success, update history and print agent response
                    function_history.append(function_call_result.parts[0])
                    if args.verbose is True:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

            # Update the messages to include all function calling history
            messages.append(types.Content(role="user", parts=function_history))
            #for i, msg in enumerate(messages):
               # print(f"Message {i}: role={msg.role}, parts={msg.parts}")
        else:
            print(response.text)
            return True
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    load_dotenv()

    # Pull key, setup client
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Missing GEMINI_API_KEY")
    
    except Exception as e:
        print(f"Error: {e}")
    
    client = genai.Client(api_key=api_key)

    # Setup argument parsing, pulls user prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    userprompt = args.user_prompt

    # Creates Message list to send to API
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    
    # Send a user prompt to API, handles response
    for _ in range(20):
        done = call_agent(client, userprompt, args, messages)
        if done:
            # Agent finished calls, exit program.
            exit(0)
    print("Error: Agent did not complete within 20 iterations.")
    exit(1)


if __name__ == "__main__":
    main()
