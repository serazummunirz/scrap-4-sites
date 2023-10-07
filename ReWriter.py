import os
from tinq import Tinq




text = "The process of learning a new piece of music is fantastic. You start from nothing, practise, improve, and finally get the fruits of your hard work, as farmers do during the harvest time."


def rewrite(tinq_api_key, scraped_articles_folder_name, rewritten_articles_folder_name):

    
    tinq = Tinq(api_key=tinq_api_key)

    total = 0

    files = os.listdir(scraped_articles_folder_name)
    for f in files:
        with open(f'{scraped_articles_folder_name}/{f}', 'r') as r:
            lines = r.readlines()[2:]
            article = " ".join(lines)
            print(article)
            print('\n')
            print('\n')
            print('\n')
            print('Rewritten:')
            print('\n')

            rewritten = tinq.rewrite(text=article[:100], mode='standard')
            rewritten_phrases = rewritten['paraphrases']

            paraphrases_list = []

            for rewritten_phrase in rewritten_phrases:
                paraphrases_list.append(rewritten_phrase['paraphrases'][0])
            
            rwritten_article = " ".join(paraphrases_list)
            print(rwritten_article)

            with open(f'{rewritten_articles_folder_name}/{f}', 'a') as wr:
                wr.write(rwritten_article)
            
            total += 1
        
        if total == 5:
            break






            # rewritten = tinq.rewrite(text=article, mode='standard')
            # rewritten_phrases = rewritten['paraphrases']

            # all_phrases_list = []

            # for rewritten_phrase in rewritten_phrases:
            #     all_phrases_list.append(rewritten_phrase['paraphrases'][0])

            # full_article = " ".join(all_phrases_list)
            # print(full_article)
            # break