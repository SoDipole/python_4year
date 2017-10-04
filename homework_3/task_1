import re
from pattern.web import Wikipedia, plaintext
from collections import Counter
import math
import unittest

class WikiParser:
    def __init__(self):
        pass
    
    def get_articles(self, start):
        articles = []
        start_article = Wikipedia().article(start)
        
        if start_article:
            for link in start_article.links:
                article = Wikipedia().article(link)
                if article:
                    sections = []
                    for section in article.sections:
                        text = plaintext(section.source).lower()
                        text = self.parce_text(text)
                        sections.append(text)
                    articles.append(" ".join(sections))
        return articles
    
    def parce_text(self, text):
        parced_text = re.sub("\[.+?\]", " ", text)
        parced_text = re.sub("[^\w\s\.\!\?]|\n|_", " ", parced_text)
        parced_text = re.sub("\s{2,}", " ", parced_text)
        parced_text = re.sub("(^\s)|(\s$)", "", parced_text)
        return parced_text

class TextStatistics:
    def __init__(self, articles):
        self.articles = articles
    
    def get_top_3grams(self, n, use_idf=False):
        n_docs = 0
        ngrams = Counter()
        df = Counter()
        for text in self.articles:
            sentences = re.split("[\.\!\?]", text)
            for sentence in sentences:
                if len(sentence) >= 3:
                    ngrams.update([sentence[i:i+3] for i in xrange(len(sentence)-2)])
                    df.update(set([sentence[i:i+3] for i in xrange(len(sentence)-2)]))
                    n_docs += 1
            
        ngrams_list = []
        ngrams_freq = []
        if not use_idf:
            for ngram, freq in ngrams.most_common()[:n]:
                ngrams_list.append(ngram)
                ngrams_freq.append(freq)
        else:
            ngrams_dict = {}
            for ngram, freq in ngrams.items():
                idf = math.log(n_docs/float(df[ngram]))
                ngrams_dict[ngram] = freq*idf
            for ngram, freq in sorted(ngrams_dict.items(), key=lambda x: x[1], reverse=True)[:n]:
                ngrams_list.append(ngram)
                ngrams_freq.append(freq) 
                
        return (ngrams_list, ngrams_freq)

    def get_top_words(self, n, use_idf=False):
        stop_list = ["the", "a", "an", "on", "in", "at", "since", "for", "ago", 
                         "before", "to", "past", "to", "till", "by", "beside", "under", 
                         "below", "over", "above", "across", "through", "into", "towards", 
                         "onto", "from", "of", "off", "until", "with"]
        n_docs = len(self.articles)
        words = Counter()
        df = Counter()
        for text in self.articles:
            text = re.sub("[\.\!\?\d]", "", text)
            tokens = text.split()
            words.update([token for token in tokens if token not in stop_list])
            df.update(set([token for token in tokens if token not in stop_list]))
            
        words_list = []
        words_freq = []
        if not use_idf:
            for word, freq in words.most_common()[:n]:
                words_list.append(word)
                words_freq.append(freq)
        else:
            words_dict = {}
            for word, freq in words.items():
                idf = math.log(n_docs/float(df[word]))
                words_dict[word] = freq*idf
            for word, freq in sorted(words_dict.items(), key=lambda x: x[1], reverse=True)[:n]:
                words_list.append(word)
                words_freq.append(freq)                
                
        return (words_list, words_freq)
    
    
class Experiment:
    def __init___(self):
        pass
    
    def show_results(self):
        wp = WikiParser()
        articles = wp.get_articles('Natural language processing')
        
        ts = TextStatistics(articles)
        ngrams_list, ngrams_freq = ts.get_top_3grams(20, use_idf = True)
        print("--------------------------\nTop 20 3-grams:\n--------------------------")
        for ngram, freq in zip(ngrams_list, ngrams_freq):
            print(str(ngram) + " : " + str(freq))
            
        words_list, words_freq = ts.get_top_words(20, use_idf = True)
        print("--------------------------\nTop 20 words:\n--------------------------")
        for ngram, freq in zip(words_list, words_freq):
            print(str(ngram) + " : " + str(freq)) 
            

class TestTextStatistics(unittest.TestCase):
    def test_normal_input(self):
        articles = ["i like trains", "do you like trains? no."]
        ts = TextStatistics(articles)
        self.assertEqual((["rai", "tra", " tr"], [2, 2, 2]), 
                         ts.get_top_3grams(3, use_idf = False))
        self.assertEqual((['like', 'trains'], [2, 2]), 
                         ts.get_top_words(2, use_idf = False))
        self.assertEqual(([' no', ' yo', 'do '], [1.0986122886681098, 1.0986122886681098, 1.0986122886681098]), 
                         ts.get_top_3grams(3, use_idf = True))
        self.assertEqual((['do', 'no'], [0.6931471805599453, 0.6931471805599453]), 
                         ts.get_top_words(2, use_idf = True))        

"""
--------------------------
Top 20 3-grams:
--------------------------
 th : 43512.0184906
the : 40315.1054526
he  : 36295.7865414
ion : 30734.4002369
 in : 30322.9273053
ing : 29342.2034953
tio : 28978.4130024
 of : 28648.1835244
on  : 28145.7985337
of  : 27921.603096
ng  : 27584.378583
 an : 27379.0335695
ed  : 27247.7003659
es  : 26677.6490432
ati : 26568.121017
 co : 26034.9508523
nd  : 25935.9055525
and : 25612.6260224
al  : 25475.5499875
in  : 24819.8738372
--------------------------
Top 20 words:
--------------------------
displaystyle : 2397.762133
turing : 1983.71634617
x : 1076.04914504
arabic : 1056.102492
i : 1033.96301826
eu : 959.295076853
chomsky : 945.188302688
retrieved : 929.781600256
german : 918.237831572
p : 903.018696205
n : 899.404218141
speech : 874.351612393
tone : 833.856058214
spanish : 828.75974413
learning : 827.645700243
european : 822.513937414
translation : 819.783597964
synthesis : 798.278048912
languages : 796.165784218
turkish : 757.896110442
"""
