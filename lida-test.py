from lida import Manager, TextGenerationConfig , llm 
import ssl 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
OPENAI_API_KEY = "sk-proj-5gE0qduJ4m1YbcUDoWDMT3BlbkFJdDjnMG3THJQz0Z963Li0"

text_gen = llm("openai")
lida = Manager(text_gen = llm("openai", api_key = OPENAI_API_KEY)) 
textgen_config = TextGenerationConfig(n = 1, temperature = 0.5, model="gpt-3.5-turbo-0301", use_cache = True)
df = pd.read_csv("cars_fixed.csv")

summary = lida.summarize("cars_fixed.csv", summary_method="default", textgen_config=textgen_config)  
goals = lida.goals(summary, n = 3, textgen_config = textgen_config)

for goal in goals:
    #print(goal)
    print("\nGoal:")
    print(f"Question: {goal.question}")
    print(f"Visualization: {goal.visualization}")
    print(f"Rationale: {goal.rationale}")
    print(f"Index: {goal.index}")

    print(df)
    
    if "scatter plot" in goal.visualization:
        x_col = goal.visualization.split(' of ')[1].split(' vs ')[0]
        y_col = goal.visualization.split(' vs ')[1]
        print(x_col)
        print(y_col)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_col, y=y_col)
        plt.title(goal.visualization)
        plt.show()
    
    elif "box plot" in goal.visualization:
        y_col = goal.visualization.split(' of ')[1].split(' by ')[0]
        x_col = goal.visualization.split(' by ')[1]
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(goal.visualization)
        plt.show()

    elif "violin plot" in goal.visualization:
        y_col = goal.visualization.split(' of ')[1].split(' by ')[0].split(' and ')[1]
        x_col = goal.visualization.split(' of ')[1].split(' by ')[0].split(' and ')[0]
        hue_col = goal.visualization.split(' by ')[1]
        print(y_col)
        print(x_col)
        print(hue_col)
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=df, x=x_col, y=y_col, hue=hue_col)
        plt.title(goal.visualization)
        plt.show()