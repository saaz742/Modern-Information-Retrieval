import requests
import mwparserfromhell
import re

def call_wiki(title):
    response = requests.get(
        'https://fa.wikibooks.org/w/api.php',
        params={
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'content'
        }).json()
    page = next(iter(response['query']['pages'].values()))
    wikicode = page['revisions'][0]['*']
    parsed_wikicode = mwparserfromhell.parse(wikicode)
    return parsed_wikicode.strip_code()

pages = str(call_wiki('کتاب_آشپزی/فهرست_غذاهای_محلی_ایران')).split('\n')[99:100]  #[1:423] are recepies
for i in pages:
    m = re.search("^([^\(\/]+)*.* (\(.*\))*", i)
    name = m.group(1)[1:]
    title = name.replace(" ", "_")
    title =  "کتاب_آشپزی/"+ title
    inpu = call_wiki(title)
    if(inpu.find("دستور شماره دو") != -1):
        inp2 = inpu[inpu.find("دستور شماره یک"):inpu.find("دستور شماره دو")]
    else:
        inp2 = inpu[inpu.find("دستور شماره یک"):inpu.find("جستار")]

    with open("recipe.txt", "w", encoding="utf-8") as f:
        f.write(inp2)