import random

END_OF_SENTENCE_CHARS = ['.', '?', '!']

def init():

    f = open("fellowship.txt", 'r').read().split('\n')

    markov = {}

    for i in f:
        words = i.split()
        if len(words) > 2:
            for j in range(0, len(words) - 2):
                if (words[j], words[j+1]) in markov:
                    markov[words[j], words[j+1]].append(words[j+2])
                else:
                    markov[words[j], words[j+1]] = [words[j+2]]
            if (words[-2], words[-1]) in markov:
                markov[words[-2], words[-1]].append('.')
            else:
                markov[words[-2], words[-1]] = ['.']
    return markov

def get_sentence(markov):
    """
    get_sentence: A short description

    Args:
    dict: markov dictionary used
    """
    sentence = []

    key = list(random.choice(markov.keys()))

    while key[0][0].islower(): # makes sure it starts on a capital string
        key = list(random.choice(markov.keys()))

    value = random.choice(markov[key[0], key[1]])

    sentence += key
    sentence.append(value)

    while (key[0], key[1]) in markov and value[-1] not in END_OF_SENTENCE_CHARS:
        key[0] = key[1]
        key[1] = value
        value = random.choice(markov[key[0], key[1]])
        sentence.append(value)

    return " ".join(sentence)
