# State S0: Start state
# State S1: Article (e.g., "The")
# State S2: Noun (e.g., "cat", "mouse")
# State S3: Verb (e.g., "eats")

# Transitions:
# S0 -> S1 (Article)
# S1 -> S2 (Noun)
# S2 -> S3 (Verb)
# S3 -> S2 (Noun)
# S2 -> Accept State

class RTN:

    def __init__(self, start_state):
        self.states = set()
        self.transitions = []
        self.start_state = start_state
        self.result = []

    def add_transition(self, name, condition, previous_state, next_state):
        self.states.add(previous_state)
        self.states.add(next_state)
        self.transitions.append({'name': name, 'condition': condition,
                                'previous_state': previous_state, 'next_state': next_state})

    def parse(self, sentence: str):
        tokens = sentence.split(" ")
        self.result = []
        r = self.parse_helper(tokens, self.start_state)
        print("Sentence: " + sentence)
        print(self.result)
        return r

    def parse_helper(self, token, state):
        if not token:
            return True
        if state in self.states:
            transition = [
                t for t in self.transitions if t['previous_state'] == state][0]
            condition = transition['condition']
            if condition(token[0]):
                self.result.append({transition['name']: token[0]})
                return self.parse_helper(token[1:], transition['next_state'])
            else:
                return False


# conditions

def is_article(word):
    return word.lower() in ['a', 'an', 'the']


def is_noun(word):
    return word.lower() in ['cat', 'dog', 'mouse']


def is_verb(word):
    return word.lower() in ['ate', 'killed', 'hates']


# model
rtn = RTN("S1")

rtn.add_transition("Article", is_article, "S1", "S2")
rtn.add_transition("Noun", is_noun, "S2", "S3")
rtn.add_transition("Verb", is_verb,  "S3", "S4")
rtn.add_transition("Article", is_article,  "S4", "S5")
rtn.add_transition("Noun", is_noun,  "S5", "S6")

print('-----------------------------------------')
print(rtn.parse("The cat ate a mouse"))
print('-----------------------------------------',end="\n\n\n")
print(rtn.parse("A Dog ate mouse a"))
print('-----------------------------------------',end="\n\n\n")
print(rtn.parse("The dog hates the cat"))
print('-----------------------------------------')
