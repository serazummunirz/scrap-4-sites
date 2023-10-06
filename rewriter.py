from tinq import Tinq
tinq = Tinq(api_key='key-45c78e0c-41c2-448c-aaf1-4736bc6c76da-651d3c3f6a5d1')


text = "The process of learning a new piece of music is fantastic. You start from nothing, practise, improve, and finally get the fruits of your hard work, as farmers do during the harvest time."
rewritten = tinq.rewrite(text=text, mode='standard')
print(rewritten['original'])
print("\n")
rewritten_phrases = rewritten['paraphrases']

all_phrases_list = []

for rewritten_phrase in rewritten_phrases:
    all_phrases_list.append(rewritten_phrase['paraphrases'][0])

full_article = " ".join(all_phrases_list)
print(full_article)