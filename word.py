from call_llm import CallLLM

class MakeWord:
    def __init__(self):
        self.call_llm = CallLLM()
        self.system_prompt = "User's input is an utterance you should make. Please generate the utterance based on it in Japanese."
        """
        User's inputはあなたがするべき発言です。それに基づいて発言を日本語で生成してください。
        """
    
    def making_word(self, action):
        sys_prompt = self.system_prompt
        response = self.call_llm.call_llms(sys_prompt, action)

        return response