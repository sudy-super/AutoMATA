import openai
import os

class CallLLM:
    def __init__(self):
        self.openai_api_key = "sk-replaced_me" # os.environ["OPENAI_API_KEY"]
        self.llm_kind = "gpt"

    def call_llms(self, system_prompt, prompt):
        if self.llm_kind == "gpt":
            res = self.call_gpt(system_prompt, prompt)
            print("[INFO]Requested OpenAI API")
        
        return res
    
    def call_gpt(self, system_prompt, prompt):
        openai.api_key = self.openai_api_key

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
                ],
            # temperature=1
            )
        response = response["choices"][0]["message"]["content"]

        return response
