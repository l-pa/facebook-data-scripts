import json
import sys
import os
import datetime

filename = sys.argv[1]  # first argument as filename

file = open(filename, 'r')  # or change filename to 'message.json'

jsonToFix = json.load(file)

# %Y-%m-%d %H:%M:%S

for i in jsonToFix['messages']:
    try:
        i['sender_name'] = i['sender_name'].encode('latin-1').decode('utf8')
        i['content'] = i['content'].encode('latin-1').decode('utf8')
    except Exception:
        pass

jsonToFix['title'] = jsonToFix['title'].encode('latin-1').decode('utf8')

filename = '{}_fixed.json'.format(
    os.path.splitext(filename)[0])
with open(filename, 'w', encoding='utf8') as fout:
    json.dump(jsonToFix, fout, indent=2, ensure_ascii=False)

print('{} {}'.format(os.getcwd(), filename))
