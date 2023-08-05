from call_llm import CallLLM
import json
import random

class MakeAction:
    def __init__(self):
        self.call_llm = CallLLM()
        self.prompt = """The Hypothesis in User's input is based on the Input. Please take these into account and consider utterance that can validate the Hypothesis."""
        """
        ユーザー入力の仮説は入力に基づいています。これらを考慮し、仮説を検証できる発言を考えてください。
        """

    def making_action(self, input_t, hypothesis):
        prompt = self.prompt

        random_llm = random.randint(1, 4) # 思考方法を入力として仮説を提案する脳内会議メンバーを選択
        angel_prompt = """You are an angel. You always try to be positive and tolerant. You are also sincere, ascetic and optimistic about things."""
        devil_prompt = """You are the devil. You constantly try to be critical and intolerant. You are also dishonest, hedonistic, and pessimistic about things."""
        hardboiled_prompt = """You are a hard-boiled person. You are ruthless, not driven by emotions or circumstances, but because you are ruthless, you keep your promises and are dependable."""
        emotional_prompt = """You are an emotional person. You tend to rely on passion and momentum, and you tend to be intense in your joy, anger, and sorrow."""

        if random_llm == 1: # 天使
            system_prompt = angel_prompt
        elif random_llm == 2: # 悪魔
            system_prompt = devil_prompt
        elif random_llm == 3: # ハードボイルド
            system_prompt = hardboiled_prompt
        else:                 # 悲観的
            system_prompt = emotional_prompt

        while True: # 否決された場合永遠にフィードバックをするための全体ループ
            try:
                action = action # メンバーからのフィードバック時のみフィードバック前の行動として定義
            except NameError:
                action = None

            try:
                feedback1 = feedback_count[0] # 各メンバーのフィードバックを定義
            except NameError:
                feedback1 = None
            try:
                feedback2 = feedback_count[1]
            except NameError:
                feedback2 = None
            try:
                feedback3 = feedback_count[2]
            except NameError:
                feedback3 = None
            if (feedback1 == None) and (feedback2 == None) and (feedback3 == None):
                feedback = "None"
            else:
                feedback_list = [feedback1, feedback2, feedback3]
                # Noneが格納されている変数を排除
                filtered_feedback = ["- " + one_of_feedbacks for one_of_feedbacks in feedback_list if one_of_feedbacks is not None]
                # 改行で区切った文字列を生成
                feedback = "\n".join(filtered_feedback)

            sys_prompt = system_prompt + "\n\n" + prompt + f"Also, if an Utterance and Feedback exist, please modify the Hypothesis according to the Feedback.\n\n##ExistingUtterance\n{action}\n\n##Feedback\n{feedback}" # + '\n\n##Example\n{{"action": "From this input, it may be said that the woman was lonely."}}'
            main_prompt = f"##Hypothesis\n{hypothesis}\n\n##Input\n{input_t}"
            action = self.call_llm.call_llms(sys_prompt, main_prompt) # 仮説を生成するのであってjsonで出力はしないのでループはしない

            # ユーザーの入力は仮説を検証するための発話です。この発話に対する賛否と、Examplesを参照したフィードバックを出力してください。
            vote_prompt = f'''User's input is an utterance to validate the Hypothesis. Please output your approval or disapproval of this utterance and your feedback with reference to Examples.

Please outout with JSON format.

##Hypothesis
{hypothesis}

##Examples
{{"vote": "agree", "feedback": "The utterance is appropriate and consistent with the situation."}}
{{"vote": "disagree", "feedback": "That utterance misses the point. We should consider the utterance to be taken more faithful to the hypothesis."}}'''

            if random_llm == 1:
                while True: # パース失敗に備えたループ
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response1 = self.call_llm.call_llms(dev_prompt, action)
                    
                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True: # パース失敗に備えたループ
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(hard_prompt, action)
                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True: # パース失敗に備えたループ
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, action)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[This is an Expected Error3-3] The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                vote_count = [response1["vote"], response2["vote"], response3["vote"]]
                feedback_count = [response1["feedback"], response2["feedback"], response3["feedback"]]
                agree_count = 0
                disagree_count = 0
                for item in vote_count:
                    if item == "agree":
                        agree_count += 1
                    elif item == "disagree":
                        disagree_count += 1
                
                print("Agree/Disagree: ", agree_count, "/", disagree_count) 
                if agree_count >= 2:
                    print("[Resolution] Approval")
                    break
                else:
                    print("[Resolution] Rejection")
            elif random_llm == 2:
                while True:
                    ang_prompt = angel_prompt + "\n\n" + vote_prompt
                    response1 = self.call_llm.call_llms(ang_prompt, action)
                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(hard_prompt, action)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, action)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[This is an Expected Error3-3] The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                vote_count = [response1["vote"], response2["vote"], response3["vote"]]
                feedback_count = [response1["feedback"], response2["feedback"], response3["feedback"]]
                agree_count = 0
                disagree_count = 0
                for item in vote_count:
                    if item == "agree":
                        agree_count += 1
                    elif item == "disagree":
                        disagree_count += 1
                
                print("Agree/Disagree: ", agree_count, "/", disagree_count) 
                if agree_count >= 2:
                    print("[Resolution] Approval")
                    break
                else:
                    print("[Resolution] Rejection")
            elif random_llm == 3:
                while True:
                    ang_prompt = angel_prompt + "\n\n" + vote_prompt
                    response1 = self.call_llm.call_llms(ang_prompt, action)

                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(dev_prompt, action)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, action)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                vote_count = [response1["vote"], response2["vote"], response3["vote"]]
                feedback_count = [response1["feedback"], response2["feedback"], response3["feedback"]]
                agree_count = 0
                disagree_count = 0
                for item in vote_count:
                    if item == "agree":
                        agree_count += 1
                    elif item == "disagree":
                        disagree_count += 1
                
                print("Agree/Disagree: ", agree_count, "/", disagree_count) 
                if agree_count >= 2:
                    print("[Resolution] Approval")
                    break
                else:
                    print("[Resolution] Rejection")
            elif random_llm == 4:
                while True:
                    ang_prompt = angel_prompt + "\n\n" + vote_prompt
                    response1 = self.call_llm.call_llms(ang_prompt, action)

                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(dev_prompt, action)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(hard_prompt, action)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 3-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                vote_count = [response1["vote"], response2["vote"], response3["vote"]]
                feedback_count = [response1["feedback"], response2["feedback"], response3["feedback"]]
                agree_count = 0
                disagree_count = 0
                for item in vote_count:
                    if item == "agree":
                        agree_count += 1
                    elif item == "disagree":
                        disagree_count += 1
                
                print("Agree/Disagree: ", agree_count, "/", disagree_count) 
                if agree_count >= 2:
                    print("[Resolution] Approval")
                    break
                else:
                    print("[Resolution] Rejection")
        return action