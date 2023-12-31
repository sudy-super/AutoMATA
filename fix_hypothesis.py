from call_llm import CallLLM
import json
import random

class FixHypothesis:
    def __init__(self):
        self.call_llm = CallLLM()

    def fixing_hypothesis(self, input_t, tool, hypothesis, input_t_n):
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
        

        if tool == "Random Idea method":
            prompt = """From the User input, please select a thing at random (or look up a dictionary and select a noun at random) and expand your ideas and a hypothesis in relation to your area of interest."""
        elif tool == "Stimulating Ideas":
            prompt = """From the User input, please make a list of what you would like it to be like, what would happen if you exaggerated certain parts, reversed it, eliminated it, put it together with something, etc., and choose the most outlandish of these to modify the ExistingHypothesis."""
        elif tool == "Challenging Ideas":
            prompt = """Please think about why it exists or what it is for and formulate the ExistingHypothesis for the User's input."""
        elif tool == "Conceptual Diffusion Ideation":
            prompt = """For the User's input, please consider whether this concept can be applied broadly to other things and modify the ExistingHypothesis."""
        elif tool == "Rebuttal Ideation":
            prompt = """For User input, please modify the ExistingHypothesis by debunking widely held beliefs, questioning obvious and obvious assumptions, and attempting to convincingly disprove them."""
        elif tool == "Linear thinking":
            prompt = """For the User's input, please focus on one thing and modify the ExistingHypothesis by inferring a causal relationship."""
        elif tool == "Critical thinking":
            prompt = """Please do not uncritically accept things and information in response to User's input, but rather consider them from various angles, understand them logically and objectively, and modify the ExistingHypothesis by meta-analyzing them from a single higher standpoint."""
        elif tool == "Integrated thinking":
            prompt = """Please modify the ExistingHypothesis by looking at things from a short, medium, and long term perspective for the User's input."""

        while True: # 否決された場合永遠にフィードバックをするための全体ループ
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

            while True:
                sys_prompt = system_prompt + "\n\n" + prompt + f"Also, if a Hypothesis and Feedback exist, please modify the Hypothesis according to the Feedback.\n\nPlease output in JSON format referring to Example.\n\n##ExistingHypothesis\n{hypothesis}\n\n##Feedback\n{feedback}" + '\n\n##Example\n{{"hypothesis": "From this feedback, it may be said that the woman was lonely."}}'
                hypothesis = self.call_llm.call_llms(sys_prompt, input_t)

                try:
                    hypothesis = json.loads(hypothesis)
                    hypothesis = hypothesis["hypothesis"]
                    break
                except Exception as e:
                    # print(e)
                    print("[INFO] 2-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

            vote_prompt = f'''User's input is the hypothesis for the Proposition. Please output your approval or disapproval of the hypothesis and feedback with reference to Examples.

Please outout with JSON format.

##Proposition
{input_t}

##Examples
{{"vote": "agree", "feedback": "The hypothesis is appropriate and consistent with the situation."}}
{{"vote": "disagree", "feedback": "That hypothesis misses the point. The likelihood of that phenomenon occurring in general is infinitesimally small, so it can be ignored."}}'''

            if random_llm == 1:
                while True: # パース失敗に備えたループ
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response1 = self.call_llm.call_llms(dev_prompt, hypothesis)
                    
                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True: # パース失敗に備えたループ
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(hard_prompt, hypothesis)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True: # パース失敗に備えたループ
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, hypothesis)
                    
                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
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
                    response1 = self.call_llm.call_llms(ang_prompt, hypothesis)
                    
                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(hard_prompt, hypothesis)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, hypothesis)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
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
                    response1 = self.call_llm.call_llms(ang_prompt, hypothesis)

                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(dev_prompt, hypothesis)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    emo_prompt = emotional_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(emo_prompt, hypothesis)

                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
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
                    response1 = self.call_llm.call_llms(ang_prompt, hypothesis)

                    try:
                        response1 = json.loads(response1)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    dev_prompt = devil_prompt + "\n\n" + vote_prompt
                    response2 = self.call_llm.call_llms(dev_prompt, hypothesis)

                    try:
                        response2 = json.loads(response2)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-2: The response from OpenAI API didn't follow the specified format, so it is re-running now.")

                while True:
                    hard_prompt = hardboiled_prompt + "\n\n" + vote_prompt
                    response3 = self.call_llm.call_llms(hard_prompt, hypothesis)
                    
                    try:
                        response3 = json.loads(response3)
                        break
                    except Exception as e:
                        # print(e)
                        print("[INFO] 6-3: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
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
        return hypothesis