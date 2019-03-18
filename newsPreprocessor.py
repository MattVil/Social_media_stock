import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COMPANIES = ['Tesla', 'Google', 'Apple', 'Facebook', 'Amazon', 'General Motor',
             'CVS Health', 'Chevron', 'Verizon', 'JP Morgan']

def plot_category_distribution(data):
    plot = data.category.value_counts(normalize=True).plot(kind='bar', grid=True, figsize=(16, 9))
    fig = plot.get_figure()
    fig.savefig("./visualization/categoryDistribution.png")

def plot_company_distribution(newsDic):
    names = newsDic.keys()
    values = [len(newsDic[x]) for x in names]

    fig, ax = plt.subplots()
    ax.bar(names, values)
    plt.show()

def main():

    data = pd.read_csv('./data/news/news.csv')
    plot_category_distribution(data)

    data['fullText'] = data[['title', 'description']].apply(lambda x: ' '.join(x), axis=1)

    newsPandas = {}
    for comp in COMPANIES:
        newsPandas[comp] = data[data['fullText'].str.contains('(?i){}'.format(comp), na=False)]


    for company in newsPandas.keys():
        news = []
        for index, row in newsPandas[company].iterrows():
            text = row['fullText']  # TODO: do preprocessing step
            date = row['publishedAt']
            news.append([text, date])

        with open("./data/news/{}.txt".format(company.replace(' ', '_')), "wb") as f:
            pickle.dump(news, f)

if __name__ == '__main__':
    main()
