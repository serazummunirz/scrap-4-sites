return_data = [{'original': 'SEC Charges D. E. Shaw with Violating Whistleblower Protection Rule FOR IMMEDIATE RELEASE 2023-213 Washington D.C., Sept. 29, 2023 — The Securities and Exchange Commission today announced settled charges against New York-based registered investment adviser D. E. Shaw & Co., L.P. for raising impe', 'paraphrases': ['The SEC has charges against D. E. Shaw with violation of the Whistleblower Protection Rule.', 'The SEC today announced it has charges against a New York-based registered investment adviser.']}]


json_data = return_data[0]


rewritten = json_data['paraphrases']

for data in rewritten:
    print()