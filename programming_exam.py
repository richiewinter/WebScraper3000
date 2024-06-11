import re
import matplotlib.pyplot as plt
from openai import OpenAI
from apify_client import ApifyClient

OPENAI_API_KEY = "" #your api key here
APIFY_API_KEY = "" #your api key here

gpt_client = OpenAI(api_key = OPENAI_API_KEY)
apify_client = ApifyClient(APIFY_API_KEY)

#functions
#find_typos takes a keyword list of terms and uses openAI to generate 5 misspellings of the word.  It will return a list of [keyword, kywrad, ..., keyword2,keaswrd, ...]
def find_typos(keyword_list):

    typo_list=[]
    for original_keyword in keyword_list:
        completion = gpt_client.chat.completions.create(
            model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "give me a bullet point list of the \
                    5 most common typos of \"" + original_keyword + "\" with nothing \
                    else"}
            ]
        )

        message = completion.choices[0].message.content
        new_list = re.sub("- ","",message).split("\n")
        new_list.insert(0,original_keyword)
        typo_list.extend(new_list)
    print(typo_list)
    return(typo_list)

#find_websites takes the enterprise name(s) provided by user input and uses openAI to find the homepage of these websites to scrape. It returns website(s) url in a list
def find_websites(enterprise_list):
    websites = []
    for name in enterprise_list: 
        website_finder = gpt_client.chat.completions.create(
            model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": "find me the official website homepage for the brand\"" +name+ "\". return only the complete url (starting with https://) and no other words"}
            ]
        )
        websites.append(website_finder.choices[0].message.content)
    print(websites)
    return(websites)

#scrape_data takes the list of keywords/typos and the list of websites and scrapes each websites for occurances of each word.
def scrape_data(typo_list, websites):
    results = []
    for typo in typo_list:
        for site in websites:
            rinput = {
                "searchTerm": typo,
                "startUrls": [{"url": site}],
                "instructions":"Get from the page the number of occurrences of \""+typo+"\" and include no other words in your response. numeric response only"
            }
            run = apify_client.actor("drobnikj/gpt-scraper").call(run_input = rinput)
            dataset_id = run.get('defaultDatasetId')
            if dataset_id:
                dataset = apify_client.dataset(dataset_id)
                items = dataset.list_items().items
                for item in items:
                    results.append(int(item["answer"]))
                print(results)
    return results

print('\n\nAhoy welcome to Richies Coding Assessment')

#get enterprise list from user
enterprise_list = []
enterprise = ''
while enterprise != 'done':
    enterprise = input('please enter your enterprise one at a time.. type "done" if done: \n')
    if enterprise!='done':
        enterprise_list.append(enterprise)
print(enterprise_list)

#get keyword list from user
keyword_list =[]
keyword =''
while keyword != 'done':
    keyword = input('please enter your keyword one at a time.. type "done" if done: \n')
    if keyword!='done':
        keyword_list.append(keyword)
print(keyword_list)

#get insight from user
insight_number = input('\nSlect insight request option 1 or 2:\n 1  # of occurrences \n 2 create your own\n')
if insight_number == "1":
    insight_request = "Number of occurrences"
else :
    insight_request = input('What would you like to know?\n')

#print statements
print('\nyour enterprise name(s):', enterprise_list)
print('\nyour keyword(s):\n', keyword_list)
print('\nyour insight request:', insight_request)

typo_list = find_typos(keyword_list)
websites = find_websites(enterprise_list)


if insight_request == "Number of occurrences":
    scraped_data = scrape_data(typo_list, websites)
    print(scraped_data)
    fig, ax = plt.subplots(len(enterprise_list))
    heights = [scraped_data[x:x+len(typo_list)] for x in range(0, len(scraped_data), len(typo_list))]
    for i in range(len(heights)):
        ax[i].bar(typo_list, heights[i])
        ax[i].set_title(enterprise_list[i]+" : \n"+ insight_request)
    plt.show()
else:
    completion = gpt_client.chat.completions.create(
            model = "gpt-3.5-turbo",
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": insight_request + "?"}
            ]
        )
    print(completion.choices[0].message.content)
