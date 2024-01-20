import os
from urllib.parse import urljoin
import requests
from wmill import Windmill

from memgpt.local_llm.settings.settings import get_completions_settings
from memgpt.local_llm.utils import load_grammar_file, count_tokens

WEBUI_API_SUFFIX = "/api/v1/generate"


def compile_function_block(self, functions) -> str:
    """NOTE: modified to not include inner thoughts at all as extras"""
    prompt = ""

    prompt += " ".join(
        [
            "Please select the most suitable function and parameters from the list of available functions below, based on the ongoing conversation.",
            "Provide your response in JSON format.",
            "You must always include inner thoughts, but you do not always have to call a function.",
        ]
    )
    prompt += f"\nAvailable functions:"
    for function_dict in functions:
        prompt += f"\n{self._compile_function_description(function_dict, add_inner_thoughts=False)}"

    return prompt

def get_webui_completion(endpoint, messages, function, context_window, grammar=None):
    """See https://github.com/oobabooga/text-generation-webui for instructions on how to run the LLM web server"""
    from memgpt.utils import printd

    prompt_tokens = count_tokens(prompt)
    if prompt_tokens > context_window:
        raise Exception(f"Request exceeds maximum context length ({prompt_tokens} > {context_window} tokens)")

    # Settings for the generation, includes the prompt + stop tokens, max length, etc
    settings = get_completions_settings()
    request = settings
    request["stopping_strings"] = request["stop"]  # alias
    request["max_new_tokens"] = 3072  # random hack?
    request["messages"]["prompt"] = prompt
    request["truncation_length"] = context_window  # assuming mistral 7b
    request["model"] = "TheBloke_OpenHermes-2.5-neural-chat-v3-3-Slerp-GPTQ_gptq-4bit-32g-actorder_True"
    
    # Set grammar
    if grammar is not None:
        request["grammar_string"] = grammar

    # if 'WINDMILL_TOKEN' not in os.environ:
    #     print("Error: The WINDMILL_TOKEN environment variable is not set.")
    #     sys.exit(1)

    try:
        wmill_client = Windmill(base_url = "https://windmill.batbro.us", token= "DngylpNkfbqZeX0mkSUUb4sBSnMalO", workspace="batnetwork")
        response = wmill_client.run_script("f/system/swap_model_with_openai_call", args= {"params": request})

        printd(f"JSON API response:\n{response}")
        result = response["choices"][0]["message"]["content"]
        usage = response.get("usage", None)

    except:
        # TODO handle gracefully
        raise

    # TODO correct for legacy
    completion_tokens = None
    total_tokens = prompt_tokens + completion_tokens if completion_tokens is not None else None
    usage = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }

    return result, usage
