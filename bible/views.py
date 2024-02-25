from django.shortcuts import render, redirect
from .models import Books, Bible
from search import functions as f

def bible_index(request):
    versos = Bible.objects.all()
    return render(request, 'bible_index.html', {'versos': versos} )


def bible_read(request, slug, chapter=1):
    slug = slug.title()
    this_book = Books.objects.filter(abbreviation=slug).first()

    book_verses = Bible.objects.filter(book_id=this_book.id, chapter=chapter)
    book_list = Bible.objects.filter(verse='1').order_by('id')
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


def bible_update(request):
    verse_id = request.POST.get('verse_id')
    verse = Bible.objects.filter(id=verse_id).first()

    verse.text = request.POST.get('verse_text')
    verse.save()
    return redirect(f'/biblia/{verse.book_id.abbreviation}/{verse.chapter}')