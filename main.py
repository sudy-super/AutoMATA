from hypothesis import MakeHypothesis
from act import MakeAction
from word import MakeWord
from judge_finish import JudgeFinish
from make_memory import MakeMemory
from fix_hypothesis import FixHypothesis

class AutoMATA():
    def __init__(self):
        self.make_hypothesis = MakeHypothesis()
        self.make_action = MakeAction()
        self.make_word = MakeWord()
        self.judge_finish = JudgeFinish()
        self.make_memory = MakeMemory()
        self.fix_hypothesis = FixHypothesis()

    def main(self):
        # parallel_type_hypothesis = input("Parallel Mode in Hypothesis Generation:(y/n):")
        # parallel_type_action = input("Parallel Mode in Action Generation:(y/n):")
        input_t = input("User:")
        all_list = []
        tool = self.make_hypothesis.making_thinking_tool(input_t)
        print(f"[TOOL]{tool}")
        hypothesis = self.make_hypothesis.making_hypothesis(input_t, tool)
        print(f"[HYPOTHESIS]{hypothesis}")
        
        while True:
            action = self.make_action.making_action(input_t, hypothesis)
            print(f"[ACTION]{action}")
            word = self.make_word.making_word(action)
            print("System:" + word)
            input_t_n = input("User:")
            all_dict = {
                "input_t": input_t,
                "hypothesis": hypothesis,
                "input_t_n": input_t_n
                }

            judge_result = self.judge_finish.judging_finish(input_t, hypothesis, word, input_t_n)
            if judge_result == "True":
                self.make_memory.making_memory(all_dict)
                break
            hypothesis = self.fix_hypothesis.fixing_hypothesis(input_t, tool, hypothesis, input_t_n)
            print(f"[FIX_HYPOTHESIS]{hypothesis}")
        print("----Finish----")

if __name__ == "__main__":
    automata = AutoMATA()
    automata.main()