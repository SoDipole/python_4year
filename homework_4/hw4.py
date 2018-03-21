#Оценка сложности: O((T+nP)*n_patterns)

import unittest

def poly_hash(s, x=31, p=997):
    h = 0
    for j in range(len(s)-1, -1, -1):
        h = (h * x + ord(s[j]) + p) % p
    return h

def search_rabin_multi(text, patterns):
    """
    text - строка, в которой выполняется поиск
    patterns = [pattern_1, pattern_2, ..., pattern_n] - массив паттернов, которые нужно найти в строке text
    По аналогии с оригинальным алгоритмом, функция возвращает массив [indices_1, indices_2, ... indices_n]
    При этом indices_i - массив индексов [pos_1, pos_2, ... pos_n], с которых начинаетй pattern_i в строке text.
    Если pattern_i ни разу не встречается в строке text, ему соотвествует пустой массив, т.е. indices_i = []
    """
    x = 31
    p = 997
    
    indices = [list() for x in range(len(patterns))]
    
    pattern_i = 0
    
    for pattern in patterns:
        if len(pattern) > len(text):
            continue
        
        precomputed = [0] * (len(text) - len(pattern) + 1)
        precomputed[-1] = poly_hash(text[-len(pattern):], x, p)
        
        factor = 1
        for i in range(len(pattern)):
            factor = (factor*x + p) % p
            
        for i in range(len(text) - len(pattern)-1, -1, -1):
            precomputed[i] = (precomputed[i+1] * x + ord(text[i]) - factor * ord(text[i+len(pattern)]) + p) % p
        
        pattern_hash = poly_hash(pattern, x, p)
        for i in range(len(precomputed)):
            if precomputed[i] == pattern_hash:
                if text[i: i + len(pattern)] == pattern:
                    indices[pattern_i].append(i)
        pattern_i += 1
        
    return indices

def search_rabin2(text, pattern, x=31, p=997):
    indices = []
    
    if len(pattern) == 0:
        return []
    
    if len(text) < len(pattern):
        return []
    
    # precompute hashes
    precomputed = [0] * (len(text) - len(pattern) + 1)
    precomputed[-1] = poly_hash(text[-len(pattern):], x, p)
    
    factor = 1
    for i in range(len(pattern)):
        factor = (factor*x + p) % p
        
    for i in range(len(text) - len(pattern)-1, -1, -1):
        precomputed[i] = (precomputed[i+1] * x + ord(text[i]) - factor * ord(text[i+len(pattern)]) + p) % p
    
    pattern_hash = poly_hash(pattern, x, p)
    for i in range(len(precomputed)):
        if precomputed[i] == pattern_hash:
            if text[i: i + len(pattern)] == pattern:
                indices.append(i)
    
    return indices

class TestSearchRabinMulti(unittest.TestCase):
    def test_text_shorter(self):
        self.assertEqual([[],[],[]],search_rabin_multi("аб",["абв","абвгд","абаба"]))    
    
    def test_normal(self):
        self.assertEqual([[], [], [15, 28], [30]],search_rabin_multi("И пускай на меня не обижается наш",["арод", "народный", "я", "наш"]))
        self.assertEqual([[6], [6], [0, 2]],search_rabin_multi("абабабабвгд",["абв","абвгд","абаба"]))
        self.assertEqual([[],[],[]],search_rabin_multi("абабабабвгд",["z","pd","g"]))

    def test_no_patterns(self):
        self.assertEqual([],search_rabin_multi("аб",[]))
    
    def test_no_text(self):
        self.assertEqual([[],[],[]],search_rabin_multi("",["абв","абвгд","абаба"]))
        
    
unittest.main()

        
#text = "И пускай на меня не обижается наш прославленный защитник - франкофон «Монреаль Канадиенс» Maxime – я всегда с некоторой опаской относился к этому народу. Народу способному с таким благоговением доводить до цирроза всю пернатую живность, заставлять специальных поисковых свиней копошиться в грязи в поисках сумчатых грибов, ковыряться в тине, собирая брюхоногих и двустворчатых."
#text = "И пуска"
#patterns = ["арод", "народный", "я", "наш"]
#print(search_rabin_multi(text, patterns))