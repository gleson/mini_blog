from django.shortcuts import render
from django.http import HttpResponse
from bible.models import Books, Bible
# from _operator import contains
from . import functions as f
from django.db.models import Q


def search(request):
    return render(request, 'index.html')


def results(request):
    search_term = request.POST.get('search')
    # object_list = Bible.objects.all()

    if search:
        q1 = f.make_query(search_term, 'text')
        without_stopwords = f.unique_words(search_term).difference(f.stopwords)
        q2 = f.make_query(' '.join(without_stopwords), 'text')

        ### UNION ### => query = (query1 | query2)

        object_list = Bible.objects.filter(q2)

    count = object_list.count()
    verses = f.sorting_by_scores(search_term, object_list)

    return render(request, 'results.html', {'verses': verses, 'search': search_term, 'count': count})



# def ordenar_resultados(object_list):
#     for obj in object_list:
#         score = 0
#         if obj.text.isupper():
#             score += 100
#         if 'Deus' in obj.text:
#             score += 200
#         if 'prov' in obj.text:
#             score += 100
#         if 'Pedro' in obj.text:
#             score += 150
#         obj.score = score
    
#     return sorted(object_list, key=lambda obj: obj.score, reverse=True)


# https://docs.djangoproject.com/en/4.0/topics/db/queries/