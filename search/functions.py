from unidecode import unidecode
from django.db.models import Q
import re

stopwords = ('a', 'à', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo', 'as', 'às', 'até', 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele', 'deles', 'do', 'dos', 'e', 'é', 'ela', 'elas', 'ele', 'eles', 'em', 'era', 'essa', 'essas', 'esse', 'esses', 'esta', 'está', 'estas', 'este', 'estes', 'eu', 'foi', 'fora', 'fui', 'hei', 'isso', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me', 'mesmo', 'meu', 'meus', 'minha', 'minhas', 'na', 'nas', 'nem', 'no', 'nos', 'nós', 'nossa', 'nossas', 'nosso', 'nossos', 'num', 'numa', 'o', 'os', 'ou', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'por', 'qual', 'quando', 'que', 'quem', 'se', 'sem', 'seu', 'seus', 'só', 'somos', 'sou', 'sua', 'suas', 'também', 'te', 'tem', 'tém', 'teu', 'teus', 'tu', 'tua', 'tuas', 'um', 'uma', 'você', 'vocês', 'vos')

def remove_accents(text):
    return unidecode(text)

def remove_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def remove_punctuation(text):
    #punctuations = """!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~‘’“”"""   # todas
    punctuations = """!"'(),-.–/:;<>?[]‘’“”"""                     # essencial
    
    for punctuation in punctuations:
        text = text.replace(punctuation, ' ')    
        text = remove_spaces(text)
    return text

def adjust_text(text):
    text = text.lower()
    text = remove_punctuation(text)
    return text


def replace_wrongs(text):
    wrongs = (('ihaweh','iahweh'), ('enchergar', 'enxergar'), ('enchergamos', 'enxergamos'), ('farizeu', 'fariseu'), ('shaday', 'shaddai'), ('shadai', 'shaddai'), ('descendencia', 'descendência'))
    for wrong in wrongs:
        text = re.sub(fr'\b{wrong[0]}\b', f'{wrong[1]}', text)
    return text

def stemming(text):
    terms = (('corações','corac'),('coração','corac'),('saberas','sabera'))
    for term in terms:
        text = re.sub(fr'\b{term[0]}\b', f'{term[1]}', text)
    return text

def include_synonyms(text):
    synonyms_list = [('imputado', 'em conta', 'atribuído'), ('javé', 'iahweh'), ('beliar', 'belial'), ('abraão', 'abrão'), ('melquisedec', 'melquisedeque'), ('40', 'quarenta'), ('el shaddai', 'el shadai', 'el shadday', 'el shaday')]
    for synonyms in synonyms_list:
        for synonym in synonyms:
            new_text = re.sub(fr'\b{synonym}\b', f'#{",".join(synonyms)}#', text)
            if text != new_text:
                text = new_text
                break
    return text


def unique_words(words):
    if isinstance(words, list):
        unique_words = set()
        for word in words:
            if isinstance(word, list):
                for term in word:
                    unique_words.add(term)
            else:
                unique_words.add(word)
    else:
        unique_words = set(words.split())
    return unique_words  

def prepare_search_term(search):
    search = adjust_text(search)
    search = replace_wrongs(search)
    search = stemming(search)
    search = include_synonyms(search)
    search_blocks = search.split("#")
    search_terms = []
    for search_block in search_blocks:
        search_or_block = search_block.split(',')
        if len(search_or_block) > 1:
            search_terms.append(search_or_block)
        else:
            search_and_block = search_block.split()
            for search_and_word in search_and_block:
                search_terms.append(search_and_word)
    return search_terms

#from typing import Set
def unique_words(words):
    if isinstance(words, list):
        unique_words = set()
        for word in words:
            if isinstance(word, list):
                for term in word:
                    unique_words.add(term)
            else:
                unique_words.add(word)
    else:
        unique_words = set(words.split())
    return unique_words

def prepare_text(text):
    text = adjust_text(text)
    text = remove_accents(text)
    text = replace_wrongs(text)
    return text

def word_wrapper(text):
    words = text.split()
    wrapped_words = []
    i = 0
    while i+1 < len(words):
        wrapped_words.append(f'{words[i]} {words[i+1]}')
        i += 1
    return wrapped_words

def find_exact(find, in_text, score=1, multiplier=False):
    if re.search(fr'\b{find}\b', in_text):
        n = 1
        if multiplier:
            n = len(re.findall(fr'\b{find}\b', in_text))
        return score*n
    return 0



# from typing import List
# def busca_biblica(palavras_chave: List, campo_busca: str = 'text') -> List:
def make_query(search, field):
    keywords_list = prepare_search_term(search)
    and_clauses = []
    or_clauses = []
    for word in keywords_list:
        if isinstance(word, list):
            or_subclause = Q()
            for subword in word:
                # or_subclause |= Q(text__icontains=subword)
                or_subclause |= Q(**{f'{field}__icontains': subword})
            or_clauses.append(or_subclause)
        else:
            # and_clauses.append(Q(text__icontains=word))
            and_clauses.append(Q(**{f'{field}__icontains': word}))
    query = Q()
    if and_clauses:
        query &= Q(*and_clauses)
    if or_clauses:
        query &= Q(*or_clauses)

    return query

def sorting_by_scores(search, query_results):
    search_term = prepare_text(search)
    search_words_group = word_wrapper(search_term)
    search_unique = unique_words(search_term)
    unique_with_synonyms = unique_words(prepare_search_term(search))
    without_stopwords = search_unique.difference(stopwords)
    
    for obj in query_results:
        score = 0
        result = prepare_text(obj.text)

        # busca exata
        score += find_exact(search_term, result, 200, True)
        

        # busca grupos de palavras
        for word_group in search_words_group:
            score += find_exact(word_group, result, 50)
        
        # busca palavras únicas
        for unique in search_unique:
            score += find_exact(unique, result, 20)

        # busca palavras únicas com sinônimos
        for unique_with_synonym in unique_with_synonyms:
            score += find_exact(unique_with_synonym, result, 15)

        # busca palavras únicas sem stopwords
        for no_stopword in without_stopwords:
            score += find_exact(no_stopword, result, 30, True)
        
        # total_scores[i] += scores
        obj.score = score

    return sorted(query_results, key=lambda obj: obj.score, reverse=True)

