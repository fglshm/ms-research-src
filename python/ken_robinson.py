from nlp import NLP

nlp = NLP()
text = open('ken_robinson.txt').read().strip()
tokens = nlp.tokens(text)
tokens = nlp.rm(tokens)
tags = nlp.tags(tokens)

verb = []
adjective = []
adverb = []

for tag in tags:
    if 'JJ' in tag[1]:
        adjective.append(tag[0])
    elif 'VB' in tag[1]:
        verb.append(tag[0])
    elif 'RB' in tag[1]:
        adverb.append(tag[0])


print(f"verb: {', '.join(verb)}")
print(f"adjective: {', '.join(adjective)}")
print(f"adverb: {', '.join(adverb)}")
