import markovify
import re
import spacy
import sys

# From markovify repository
class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in NLP(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def print_step(text):
    print(text, end="...")
    sys.stdout.flush()

def build_models(riddles_path="riddles.txt", answers_path="answers.txt", save_path="saved_riddles.txt"):
    '''Use markovify to build riddles and answers Markov chains'''
    global NLP, SAVE_FP
    
    print_step("Loading NLP models")
    NLP = spacy.load("en")
    print("done")

    print_step("Loading riddles")
    with open(riddles_path, "r") as f:
        riddles_text = f.read()
    print("done")

    print_step("Building riddles markov chain")
    riddles_model = POSifiedText(riddles_text, state_size=2, retain_original=False)
    print("done")

    print_step("Loading answers")
    with open(answers_path, "r") as g:
        answers_text = g.read()
    print("done")

    print_step("Building answers markov chain")
    answers_model = POSifiedText(answers_text, state_size=2, retain_original=False)
    print("done")

    SAVE_FP = open(save_path, "a")

    return riddles_model, answers_model


def generate_riddles(riddles_model, answers_model):
    '''Generate riddles from models and prompt user to save or throw away'''
    while True:
        riddle = riddles_model.make_sentence().strip()
        answer = answers_model.make_sentence().strip()

        print(riddle)
        print("=>", answer)
        choice = input("Save riddle? [y/n] ")
        save_riddle(choice, riddle, answer)
        print()


def save_riddle(choice, riddle, answer):
    '''Prompt to see if user wnats to save riddle'''
    if choice in ["y", "Y", "yes", "YES", "Yes"]:
        SAVE_FP.write(riddle + "\n" + answer + "\n\n")
    elif choice in ["n", "N", "no", "NO", "No"]:
        return
    else:
        sys.exit("[!] Invalid choice")


if __name__ == "__main__":
    riddles, answers = build_models()
    generate_riddles(riddles, answers)
