from django.shortcuts import render
from .models import Books, Bible
from search import functions as f

def bible_index(request):
    versos = Bible.objects.all()
    return render(request, 'bible_index.html', {'versos': versos} )


def bible_read(request, slug, chapter=1):
    slug = slug.title()
    this_book = Books.objects.filter(abbreviation=slug).first()

    book_verses = Bible.objects.filter(book_id=this_book.id, chapter=chapter)
    # primeiro_verso = Bible.objects.filter(book_id=this_book.id, chapter=chapter, verse='1').first()
    # primeiro_verso = book_verses.filter(verse='1')[0]
    book_list = Bible.objects.filter(verse='1').order_by('id')
    ### PEGAR INDICE ATUAL NA LISTA 'LIVROS'
    # livro_atual = book_list.filter(verse=primeiro_verso).first()
    index_list = [f'{this_book.book_id.abbreviation} {this_book.chapter}' for this_book in book_list]
    current_index = index_list.index(f'{slug} {chapter}')

    try:
        previous_chapter = book_list[current_index-1]
    except:
        previous_chapter = book_list[1329]

    try:
        next_chapter = book_list[current_index+1]
    except:
        next_chapter = book_list[0]


    # if current_index == 0:
    #     previous_chapter = book_list[1329]
    # else:
    #     previous_chapter = book_list[current_index-1]

    # if current_index == 1329:
    #     next_chapter = book_list[0]
    # else:
    #     next_chapter = book_list[current_index+1]


    # teste1 = primeiro_verso
    # teste2 = previous_chapter
    # teste3 = next_chapter

    # return render(request, 'bible_read.html', {'teste1': teste1, 'teste2': teste2, 'teste3': teste3, 'current_index': current_index, 'indices': indices} )
    # return render(request, 'bible_read.html', {'this_book': this_book, 'book_verses': book_verses, 'book_list': book_list} )
    return render(request, 'bible_read.html', {'book_verses': book_verses, 'previous_chapter': previous_chapter, 'next_chapter': next_chapter} )


def bible_search(request):
    search_term = request.POST.get('bible_search')

    if search_term:
        q1 = f.make_query(search_term, 'text')
        without_stopwords = f.unique_words(search_term).difference(f.stopwords)
        q2 = f.make_query(' '.join(without_stopwords), 'text')

        object_list = Bible.objects.filter(q2)
        count = object_list.count()
        results = f.sorting_by_scores(search_term, object_list)
        return render(request, 'bible_search.html', {'results': results, 'search': search_term, 'count': count})

    else:
        return render(request, 'bible_search.html', {'results': [], 'search': '', 'count': 0})


def bible_edit(request):
    pass
