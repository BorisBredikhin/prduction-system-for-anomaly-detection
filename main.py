import json

from rules import KnowledgeBase

# todo: rewrite as fnction
f=open('./example_data/rules.json', 'r')
knowledges: KnowledgeBase = json.load(f)
f.close()

print(knowledges)

