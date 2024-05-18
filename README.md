Summary

This code is a tool for analyzing the online presence of enterprises by identifying common misspellings of given keywords, finding the official website URLs of provided enterprise names, and scraping data from those websites to determine occurrences of the misspelled keywords.

Libraries Used

re: Regular expressions module used for string manipulation.
matplotlib.pyplot: Library for creating static, animated, and interactive visualizations in Python.
openai: Library for interfacing with the OpenAI API, used for text completion and generation tasks.
apify_client: Library for the Apify API, used for web scraping tasks.

Functions

find_typos(keyword_list)

Input: List of keywords
Output: List of misspellings generated using OpenAI API
Description: Generates 5 misspellings for each keyword provided in the list using the GPT-3.5 model.

find_websites(enterprise_list)

Input: List of enterprise names
Output: List of official website URLs
Description: Uses the OpenAI API to find the official homepage URLs for each enterprise provided in the list.

scrape_data(typo_list, websites)

Input: List of misspellings and list of website URLs
Output: List of occurrence counts for each misspelling on each website
Description: Scrapes each website for occurrences of each misspelling in the provided list and returns the counts.

Usage

Run the script.
Input enterprise names one at a time until finished.
Input keywords one at a time until finished.
Select an insight request option:
Enter "1" for the number of occurrences of misspelled keywords.
Enter "2" to create a custom insight request.
View the results either as a bar chart showing occurrence counts for each misspelling per enterprise or as a response to a custom insight request.
