from django.shortcuts import render
from django.http import HttpResponse
from .models import Books, Bible
from search import functions as f

def bible_index(request):
    versos = Bible.objects.all()
    return render(request, 'bible_index.html', {'versos': versos} )


def bible_read(request, slug, chapter=1):
    slug = slug.title()
    # livros = Books.objects.all()
    livro = Books.objects.filter(abbreviation=slug).first()
    versos = Bible.objects.filter(book_id=livro.id, chapter=chapter)
    previous = versos.first()
    next = versos.last()
    previous_verse = Bible.objects.filter(id=(previous.id-1)).first()
    next_verse = Bible.objects.filter(id=(next.id+1)).first()
    last_chapter = livro.chapters
    # next_page = None #próximo capítulo, ou, próximo livro se (cap = max e livro != max)

    #next
    if int(chapter) < last_chapter:
        next_book = livro.abbreviation
        next_chapter = int(chapter)+1
    else:
        next_chapter = 1
        if livro.abbreviation == 'Ap':
            next_book = 'Índice'
        else:
            next_book = 1
    
    #previous
    if int(chapter) > 1:
        previous_book = livro.abbreviation
        previous_chapter = int(chapter)-1  
    elif int(chapter) == 1 and livro.abbreviation == 'Gn':
        previous_book = 'Índice'
    else:
        previous_book = None # LIVRO ANTERIOR


    
    # next_page = {'book': next_book, 'chapter': next_chapter, 'link': next_book.lower()}
    
    
    # previous_page = None #capítulo anterior, ou, livro anterior se (cap = min e livro != min)
    # if chapter < livro.chapters.__gt__:
        # next_page = Bible.objects.filter(book_id=livro.id, chapter=(chapter+1)).first()
    # else:
        # next_page = Bible.objects.filter(book_id=(livro.id+1), chapter=1).first()

    
        
    # previous_book = Books.objects.filter(id=previous_verse.book_id).first()
    # next_book = Books.objects.filter(id=next_verse.book_id).first()
    # next_book = Books.objects.filter(id=next_verse).first()
    # print(next_book)
    # previous_link = {'book': previous_book.book, 'chapter': previous_verse.chapter, 'link': previous_book.slug}
    # next_link = {'book': next_book.book, 'chapter': next_verse.chapter, 'link': next_book.slug}
    # return render(request, 'livro.html', {'versos': versos, 'livro': livro, 'previous_link': previous_link, 'next_link': next_link} )
    return render(request, 'bible_read.html', {'versos': versos, 'livro': livro} )


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

