from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm

import re
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression

def index(request):
    if request.method == "POST":
        review = request.POST.get("review")
        rev_s = text_transformer(review, load_vocabulary_rate('imdb.vocab', 'imdbEr.txt'))
        rev_s = text_fitter(375, rev_s)
        model_s = load_model("finalized_model.sav")
        rate = 1+int(str(round(model_s.predict_proba(rev_s.reshape(1, -1))[0][1], 1))[2])
        mood = 'Положительный' if rate > 5 else 'Отрицательный'
        return render(request, "evaluation.html", {"rate": rate,
                                                "mood": mood})
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})

def text_cleaner(text):
    text = text.lower()
    text = re.sub(r"[.,\")(>+<*/]", " ", text)
    text = re.sub(r"[']", "", text)
    text = re.sub(r"[!]", " !", text)
    return re.sub(r"[?]", " ?", text)

def text_transformer(text, vocabulary):
    cleaned_text = text_cleaner(text).split()
    for word in range(len(cleaned_text)):
        cleaned_text[word] = vocabulary[cleaned_text[word]] if vocabulary.get(cleaned_text[word]) != None else 0
    return cleaned_text

def load_model(filename):
        return pickle.load(open(filename, 'rb'))

def load_vocabulary_rate(vocab_words, vocab_rates):
    vocabulary = []
    expected_rating = []
    
    with open(vocab_words, 'r') as file_handler:
        vocabulary = file_handler.read().splitlines()

    with open(vocab_rates, 'r') as file_handler:
        expected_rating = list(map(float, file_handler.read().splitlines()))

    return dict(zip(vocabulary, expected_rating))

def load_vocabulary_numbs(vocab_words):
    vocabulary_numbs = {}
    number = 1
    
    with open(vocab_words, 'r') as file_handler:
        for word in file_handler:
            vocabulary_numbs[word.strip()] = number
            number += 1

    return vocabulary_numbs

def text_fitter(length, text):
    if len(text) < length:
        return np.array(list(text) + [0 for x in range(length-len(text))])

    expected_rating = []
    
    with open(vocab_words, 'r') as file_handler:
        vocabulary = file_handler.read().splitlines()

    with open(vocab_rates, 'r') as file_handler:
        expected_rating = list(map(float, file_handler.read().splitlines()))

    return dict(zip(vocabulary, expected_rating))

def load_vocabulary_numbs(vocab_words):
    vocabulary_numbs = {}
    number = 1
    
    with open(vocab_words, 'r') as file_handler:
        for word in file_handler:
            vocabulary_numbs[word.strip()] = number
            number += 1

    return vocabulary_numbs

def text_fitter(length, text):
    if len(text) < length:
        return np.array(list(text) + [0 for x in range(length-len(text))])
    else:
        return np.array(list(text)[:length])

