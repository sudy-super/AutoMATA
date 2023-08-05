from call_llm import CallLLM

class JudgeFinish:
    def __init__(self):
        self.call_llm = CallLLM()
        self.system_prompt = "The Hypothesis in User's input is derived from the Input, the UtteredContent is the utterance made to verify the Hypothesis, and the NewInput is the reply to the UtteredContent. Now you have a loop that velifies the Hypothesis derived from the Input by uttering the UtteredContent, receives the NewInput, and modifies the Hypothesis. If there is a surprise between the Hypothesis and the NewInput, please output False because the loop must continue, and output True because the loop doesn't need to continue if it determines that there is not a surprise."
        # User's inputのHypothesisはInputから導かれ、UtteredContentはHypothesisを検証するためにした発言で、NewInputはUtteredContentの返事です。今はInputから導かれたHypothesisをUtteredContentを発話することで検証し、NewInputを受け取ってHypothesisを修正するループをしています。User's inputを考慮して、HypothesisとNewInputの間に乖離があると判断したらループを続ける必要があるのでFalse、一致していると判断したらループを続ける必要はないのでTrueと出力してください。

    def judging_finish(self, input_t, hypothesis, word, input_t_n):
        while True:
            sys_prompt = self.system_prompt
            main_prompt = f"##Input\n{input_t}\n\n##Hypothesis\n{hypothesis}\n\n##UtteredContent\n{word}\n\n##NewInput\n{input_t_n}"
            response = self.call_llm.call_llms(sys_prompt, main_prompt)
            
            if (response == "True") or (response == "False"):
                break
            print("[INFO] 5: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

        return response