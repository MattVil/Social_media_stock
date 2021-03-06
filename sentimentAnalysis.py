import nltk
import numpy as np
import itertools, pickle
import pickle
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report, confusion_matrix

from utils import COMPANIES, PROJECT_PATH
from stockScraper import get_daily_change


PATH_TRAINING = PROJECT_PATH + "text-emotion-classification/"
MODEL_NAME = "checkpoint-1.144.h5"
MAX_SEQUENCE_LENGTH = 30

def predict_emotion(sentences):
    with open(PATH_TRAINING + 'tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    classes = ["neutral", "happy", "sad", "hate","anger"]

    model = load_model(PATH_TRAINING + MODEL_NAME)
    sequences_test = tokenizer.texts_to_sequences(sentences)
    data_int_t = pad_sequences(sequences_test, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH-5))
    data_test = pad_sequences(data_int_t, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
    y_prob = model.predict(data_test)
    return y_prob

def predict_positivity(sentences):
    pred = np.zeros((len(sentences),))
    sia = SentimentIntensityAnalyzer()
    for i, sentence in enumerate(sentences):
        y = sia.polarity_scores(sentence)
        pred[i] = y['compound']
    return pred

def predict_daily_positivity(data):
    pred = np.zeros((len(data),))
    sia = SentimentIntensityAnalyzer()
    for i, date in enumerate(data.keys()):
        nbSentence = len(data[date])
        for sentence in data[date]:
            y = sia.polarity_scores(sentence)
            pred[i] += y['compound']
        pred[i] = pred[i]/nbSentence
    return pred

def predict_daily_emotion(data):
    with open(PATH_TRAINING + 'tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    classes = ["neutral", "happy", "sad", "hate","anger"]

    model = load_model(PATH_TRAINING + MODEL_NAME)
    pred = np.zeros((len(data), 5))
    for i, key in enumerate(data.keys()):
        nbSentence = len(data[key])
        for news in data[key]:
            sequences_test = tokenizer.texts_to_sequences([news])
            data_int_t = pad_sequences(sequences_test, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH-5))
            data_test = pad_sequences(data_int_t, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
            pred[i] += model.predict(data_test)[0]
        pred[i] = pred[i]/nbSentence
    return pred

def sortByDate(data):
    dic = {}
    for news, date in data:
        dateTime = date.split('T')
        date = dateTime[0]
        if(date not in dic):
            dic[date] = [news]
        else:
            dic[date].append(news)
    return dic

def plot_confusion_matrix(cm, labels,
                          normalize=True,
                          title='Confusion Matrix (Validation Set)',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    else:
        pass

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def download():
    nltk.download('vader_lexicon')

def loadCompany(company):
    with open(PROJECT_PATH+"data/news/{}.txt".format(company), "rb") as f:
        return pickle.load(f)
    print("Error while reading the {}.txt file.".format(company))
    return None

def plot_analysis(predictions, dates, company):
    positivity = predictions[:,0]
    neutral = predictions[:,1]
    happy = predictions[:,2]
    sad = predictions[:,3]
    hate = predictions[:,4]
    anger = predictions[:,5]

    plt.xticks(rotation=90)
    plt.title(company, fontsize=16, fontweight='bold')
    plt.plot(dates, positivity, label="Positivity")
    plt.plot(dates, neutral, label="Neutral")
    plt.plot(dates, happy, label="Happy")
    plt.plot(dates, sad, label="Sad")
    plt.plot(dates, hate, label="Hate")
    plt.plot(dates, anger, label="Anger")
    plt.legend(loc='lower left')
    plt.show()

def main():
    # download()

    sentences = ["He told us a very exciting adventure story.",
                 "Mary plays the piano.",
                 "She borrowed the book from him many years ago and hasn't yet returned it.",
                 "Christmas is coming.",
                 "She did not cheat on the test, for it was not the right thing to do.",
                 "I would have gotten the promotion, but my attendance wasn’t good enough.",
                 "My Mum tries to be cool by saying that she likes all the same things that I do.",
                 "He didn’t want to go to the dentist, yet he went anyway.",
                 "The quick brown fox jumps over the lazy dog.",
                 "I want to buy a onesie… but know it won’t suit me.",
                 "What baby bonus scheme ??? To grow up a kid in Singapore you think is easy now bo ??? Both parent need to work to grow up a kid until 21 , you think tats easy bo ??? Think la"]

    data, label = [], []
    for companyName in COMPANIES:

        sentences = []
        dates = []

        companyName = companyName.replace(' ', '_')
        company = loadCompany(companyName)
        for news, date in company:
            sentences.append(news)
            dates.append(date)

        dic = sortByDate(company)
        y_pos = predict_daily_positivity(dic)
        y_emo = predict_daily_emotion(dic)

        y_final = np.c_[y_pos, y_emo]

        # plot_analysis(y_final, dic.keys(), companyName)
        dates = dic.keys()
        stock_changes = []
        for idx, date in enumerate(dates):
            date_splited = date.split('-')
            stock_changes.append(get_daily_change(companyName, (int(date_splited[1]), int(date_splited[2]), int(date_splited[0]))))
        stock_changes = np.asarray(stock_changes)
        print(stock_changes)
        print(y_final)
        print(stock_changes.shape)
        print(y_final.shape)
        for i in range(len(stock_changes)):
            if(stock_changes[i] != None):
                data.append(stock_changes[i])
                label.append(y_final[i])

    data = np.asarray(data)
    label = np.asarray(label)
    print(data)
    print(label)
    print(data.shape)
    print(label.shape)
    np.save(PROJECT_PATH+"data/emo.npy", data)
    np.save(PROJECT_PATH+"data/label.npy", label)

if __name__ == '__main__':
    main()
