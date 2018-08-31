import markovify
import re
import spacy
import sys


def build_models():
    global NLP, SAVE_FP

    print("Loading NLP models", end="...")
    sys.stdout.flush()
    NLP = spacy.load("en")
    print("done")

    print("Loading riddles", end="...")
    sys.stdout.flush()
    with open("riddles.txt", "r") as f:
        riddles_text = f.read()
    print("done")

    print("Building riddles markov chain", end="...")
    sys.stdout.flush()
    riddles_model = POSifiedText(riddles_text, state_size=2, retain_original=False)
    print("done")

    print("Loading answers", end="...")
    sys.stdout.flush()
    with open("answers.txt", "r") as g:
        answers_text = g.read()
    print("done")

    print("Building answers markov chain", end="...")
    sys.stdout.flush()
    answers_model = POSifiedText(answers_text, state_size=2, retain_original=False)
    print("done")

    SAVE_FP = open("saved_riddles.txt", "a")

    return riddles_model, answers_model

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in NLP(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def generate_riddles(riddles_model, answers_model):
    while True:
        riddle = riddles_model.make_sentence().strip()
        answer = answers_model.make_sentence().strip()

        print(riddle)
        print("=>", answer)
        choice = input("Save riddle? [y/n] ")
        save_riddle(choice, riddle, answer)
        print()


def save_riddle(choice, riddle, answer):
    if choice in ["y", "Y", "yes", "YES", "Yes"]:
        SAVE_FP.write(riddle + "\n" + answer + "\n\n")
    elif choice in ["n", "N", "no", "NO", "No"]:
        return
    else:
        sys.exit("[!] Invalid choice")


if __name__ == "__main__":
    riddles, answers = build_models()
    generate_riddles(riddles, answers)
