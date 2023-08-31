from call_llm import CallLLM
import json
import random

# LLMのENUM
class LLM_KIND:
    ANGEL_PROMPT = """You are an angel. You always try to be positive and tolerant. You are also sincere, ascetic and optimistic about things."""
    DEVIL_PROMPT = """You are the devil. You constantly try to be critical and intolerant. You are also dishonest, hedonistic, and pessimistic about things."""
    HARDBOILED_PROMPT = """You are a hard-boiled person. You are ruthless, not driven by emotions or circumstances, but because you are ruthless, you keep your promises and are dependable."""
    EMOTIONAL_PROMPT = """You are an emotional person. You tend to rely on passion and momentum, and you tend to be intense in your joy, anger, and sorrow."""

class HYPOTHESIS_TASK:
    RANDOM_IDEA_METHOD = """Random Idea method: A random selection of things (or a random selection of nouns from a dictionary) is used to expand the idea by associating it with an area of interest."""
    STIMULATING_IDEAS = """Stimulating Ideas: This method involves making a list of things that you wish were this way, exaggerating certain parts, reversing, eliminating, or combining with other things, etc., and then selecting the most outlandish of these ideas as the basis for a new idea."""
    CHALLENGING_IDEAS = """Challenging Ideas: This is a method of generating new ideas by considering why something exists or why it is the way it is."""
    CONCEPTUAL_DIFFUSION_IDEATION = """Conceptual Diffusion Ideation: This method generates ideas by considering whether a concept can be applied broadly to other things."""
    REBUTTAL_IDEATION = """Rebuttal Ideation: Generating ideas by questioning what is considered obvious and needless to say and attempting to disprove it persuasively, considering widely supported ideas to be wrong."""
    LINEAR_THINKING = """Linear thinking: focus on one thing to infer causal relationships."""
    CRITICAL_THINKING = """Critical thinking: Examine things and information from diverse angles and understand them logically and objectively, rather than accepting them uncritically. Examine the thoughts of oneself and others without assuming that one's own beliefs are correct. Think meta-advantageously and from one higher standpoint."""
    INTEGRATED_THINKING = """Integrated thinking: See and think about things from short-, medium-, and long-term perspectives."""

class MakeHypothesis:
    def __init__(self):
        self.call_llm = CallLLM()
        self.feedback_count = [None, None, None]
        self.prompt = '''The following options are given as tools for generating a hypothesis.
Please select the tools you need to make a hypothesis about the situation inferred from the User's input, and output them in JSON format referring to Example.

- Lateral thinking: Generate intuitive ideas by looking at things from a variety of perspectives.
- Linear thinking: focus on one thing to infer causal relationships.
- Critical thinking: Examine things and information from diverse angles and understand them logically and objectively, rather than accepting them uncritically. Examine the thoughts of oneself and others without assuming that one's own beliefs are correct. Think meta-advantageously and from one higher standpoint.
- Integrated thinking: See and think about things from short-, medium-, and long-term perspectives.

##Example
{"tool": "Lateral thinking"}'''


    def making_thinking_tool(self, input_t):
        prompt = self.prompt

        while True: # 思考方法選択のパース失敗に備えたループ
            response = self.call_llm.call_llms(prompt, input_t)
            try:
                response = json.loads(response)
                break
            except Exception as e:
                # print(e)
                print("[INFO] 1: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                # pass
        if response["tool"]=="Lateral thinking": # 水平思考が選択された場合
            lateral_prompt = '''The following options are given as tools for generating a hypothesis.
Please select the tools you need to make a hypothesis about the situation inferred from the User's input, and output them in JSON format referring to Example.

- Random Idea method: A random selection of things (or a random selection of nouns from a dictionary) is used to expand the idea by associating it with an area of interest.
- Stimulating Ideas: This method involves making a list of things that you wish were this way, exaggerating certain parts, reversing, eliminating, or combining with other things, etc., and then selecting the most outlandish of these ideas as the basis for a new idea.
- Challenging Ideas: This is a method of generating new ideas by considering why something exists or why it is the way it is.
- Conceptual Diffusion Ideation: This method generates ideas by considering whether a concept can be applied broadly to other things.
- Rebuttal Ideation: Generating ideas by questioning what is considered obvious and needless to say and attempting to disprove it persuasively, considering widely supported ideas to be wrong.

##Example
{"tool": "Stimulating Ideas"}'''

            while True: # 水平思考の選択のパース失敗に備えたループ
                response = self.call_llm.call_llms(lateral_prompt, input_t)
                try:
                    response = json.loads(response)
                    break
                except Exception as e:
                    # print(e)
                    print("[This is an Expected Error1-2] The response from OpenAI API didn't follow the specified format, so it is re-running now.")
                    # pass
        print(response)
        return response["tool"]

    def get_hypothesis_approval(self,approval_llms,vote_prompt,hypothesis) ->bool:
        '''
        仮説の提案を判断する関数
        '''
        print("approval_llms: ", approval_llms)
        responses = [] # {feedback:str, vote:str}
        # index取得しつつfor文を回す
        for idx, approval_llm in enumerate(approval_llms):
            while True: # パース失敗に備えたループ
                prompt = approval_llm + "\n\n" + vote_prompt
                response = self.call_llm.call_llms(prompt, hypothesis)
                print(response)
                try:
                    responses.append(json.loads(response))
                    break
                except Exception as e:
                    print(e)
                    print(f"[INFO] 2-{idx}: The response from OpenAI API didn't follow the specified format, so it is re-running now.")
        # feedback_countとvotesに詰めなおす
        self.feedback_count = [responses[0]["feedback"], responses[1]["feedback"], responses[2]["feedback"]]
        votes = [responses[0]["vote"], responses[1]["vote"], responses[2]["vote"]]

        agree_count = votes.count("agree")
        disagree_count = votes.count("disagree")
        print("Agree/Disagree: ", agree_count, "/", disagree_count)

        if agree_count >= 2:
            print("[Resolution] Approval")
            return True
        else:
            print("[Resolution] Rejection")
            return False

    def get_system_prompt(self, member_num)->str:

        # 仮説を提案する脳内会議メンバーを選択
        # member_numが1の場合は天使、2の場合は悪魔、3の場合はハードボイルド、4の場合は悲観的
        prompts = {
            1: LLM_KIND.ANGEL_PROMPT,
            2: LLM_KIND.DEVIL_PROMPT,
            3: LLM_KIND.HARDBOILED_PROMPT,
            4: LLM_KIND.EMOTIONAL_PROMPT
        }
        return prompts.get(member_num)

    def get_task_prompt(self, tool)->str:
        if tool == "Random Idea method":
            return HYPOTHESIS_TASK.RANDOM_IDEA_METHOD
        if tool == "Stimulating Ideas":
            return HYPOTHESIS_TASK.STIMULATING_IDEAS
        if tool == "Challenging Ideas":
            return HYPOTHESIS_TASK.CHALLENGING_IDEAS
        if tool == "Conceptual Diffusion Ideation":
            return HYPOTHESIS_TASK.CONCEPTUAL_DIFFUSION_IDEATION
        if tool == "Rebuttal Ideation":
            return HYPOTHESIS_TASK.REBUTTAL_IDEATION
        if tool == "Linear thinking":
            return HYPOTHESIS_TASK.LINEAR_THINKING
        if tool == "Critical thinking":
            return HYPOTHESIS_TASK.CRITICAL_THINKING
        if tool == "Integrated thinking":
            return HYPOTHESIS_TASK.INTEGRATED_THINKING
        raise Exception("Invalid tool name")

    def making_hypothesis(self, input_t, tool):
        random_llm = random.randint(1, 4) # 思考方法を入力として仮説を提案する脳内会議メンバーを選択
        system_prompt = self.get_system_prompt(random_llm)
        task_prompt = self.get_task_prompt(tool)

        while True: # 否決された場合永遠にフィードバックをするための全体ループ
            try:
                hypothesis = hypothesis # メンバーからのフィードバック時のみフィードバック前の仮説として定義
            except NameError:
                hypothesis = None
            # 一週目はfeedback_countが未定義なので、必ずNoneになる
            feedbacks = self.feedback_count
            if (feedbacks[0] == None) and (feedbacks[1] == None) and (feedbacks[2] == None):
                feedback = "None"
            else:
                # Noneが格納されている変数を排除
                filtered_feedback = ["- " + one_of_feedbacks for one_of_feedbacks in feedbacks if one_of_feedbacks is not None]
                # 改行で区切った文字列を生成
                feedback = "\n".join(filtered_feedback)

            while True:
                hypothesis_prompt = system_prompt + "\n\n" + task_prompt + f"Also, if a Hypothesis and Feedback exist, please modify the Hypothesis according to the Feedback.\n\nPlease output in JSON format referring to Example.\n\n##ExistingHypothesis\n{hypothesis}\n\n##Feedback\n{feedback}" + '\n\n##Example\n{{"hypothesis": "From this input, it may be said that the woman was lonely."}}'
                hypothesis = self.call_llm.call_llms(hypothesis_prompt, input_t)
                print(hypothesis)
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
                # 仮説を提案する脳内会議メンバーが天使の場合
                # 悪魔、ハードボイルド、悲観的の順に仮説を否決するかどうかを判断
                approval_llms = [LLM_KIND.DEVIL_PROMPT, LLM_KIND.HARDBOILED_PROMPT, LLM_KIND.EMOTIONAL_PROMPT]
                is_approval = self.get_hypothesis_approval(approval_llms,vote_prompt,hypothesis)
                if is_approval == True:
                    break
                
            elif random_llm == 2:
                approval_llms = [LLM_KIND.ANGEL_PROMPT, LLM_KIND.HARDBOILED_PROMPT, LLM_KIND.EMOTIONAL_PROMPT]
                is_approval = self.get_hypothesis_approval(approval_llms,vote_prompt,hypothesis)
                if is_approval == True:
                    break
            elif random_llm == 3:
                approval_llms = [LLM_KIND.ANGEL_PROMPT, LLM_KIND.DEVIL_PROMPT, LLM_KIND.EMOTIONAL_PROMPT]
                if is_approval == True:
                    break
            elif random_llm == 4:
                approval_llms = [LLM_KIND.ANGEL_PROMPT, LLM_KIND.DEVIL_PROMPT, LLM_KIND.HARDBOILED_PROMPT]
                is_approval = self.get_hypothesis_approval(approval_llms,vote_prompt,hypothesis)
                if is_approval == True:
                    break
        return hypothesis