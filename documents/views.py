from django.shortcuts import render
from .models import Catechism
from search import functions as f

def catechism_index(request):
    return render(request, 'catechism_index.html')


def catechism_read(request, slug):
    numbers = []
    start, end = 1, 10
    for value in slug.split(','):
        if '-' in value:
            start, end = value.split('-')
            numbers += list(range(int(start), int(end) + 1))
        else:
            numbers.append(int(value))

    paragraphs = Catechism.objects.filter(number__in=numbers)
    if int(start) > 10:
        previous_lnk = f'{int(start)-10}-{int(start)-1}'
    else:
        previous_lnk = '1-10'

    return render(request, 'catechism_read.html', {'paragraphs': paragraphs, 'next_lnk': f'{int(end)+1}-{int(end)+10}', 'previous_lnk': previous_lnk} )


def catechism_search(request):
    search_term = request.POST.get('catechism_search')

    if search_term:
        q1 = f.make_query(search_term, 'text')
        without_stopwords = f.unique_words(search_term).difference(f.stopwords)
        q2 = f.make_query(' '.join(without_stopwords), 'text')

        object_list = Catechism.objects.filter(q1)

    count = object_list.count()
    results = f.sorting_by_scores(search_term, object_list)

    return render(request, 'catechism_search.html', {'results': results, 'search': search_term, 'count': count})
