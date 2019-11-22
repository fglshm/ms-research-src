from nlp import NLP

s1 = "When I was 27 years old, I left a very demanding job in management consulting for a job that was even more demanding: teaching."
s2 = "I went to teach seventh graders math in the New York City public schools."

nlp = NLP()

s1_tokens = nlp.tokens(s1)
s1_tokens = nlp.rm(s1_tokens)

s2_tokens = nlp.tokens(s2)
s2_tokens = nlp.rm(s2_tokens)

s1_tags = nlp.tags(s1_tokens)
s2_tags = nlp.tags(s2_tokens)

s1_3grams = nlp.ngrams(s1_tags, 3)
s2_3grams = nlp.ngrams(s2_tags, 3)

seen_3grams = set()

count = 0

for pair in s1_3grams:
    count += 1
    categories = tuple(map(lambda x: x[1], list(pair)))
    if categories not in seen_3grams:
        seen_3grams.add(categories)

print(len(seen_3grams))
print(count)
