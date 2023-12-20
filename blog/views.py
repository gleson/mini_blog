from django.shortcuts import render, get_object_or_404
from .models import Category, Post

def home(request):
    return render(request, 'home.html')


def my_view(request, url):
    # Dividir a URL pelos segmentos ("/")
    segmentos = url.split('/')

    # Verificar se o último segmento é um slug ou uma categoria
    ultimo_segmento = segmentos[-1]
    postagem = Post.objects.filter(slug=ultimo_segmento)
    if postagem:
        postagem = postagem.first()
        
        # context = {'postagem': ''}
        # Chega aqui, mas o if abaixo não está sendo satisfeito
        # Testa se o slug do post está na raiz ou se as categorias da url estão corretas
        # if len(segmentos)==1 or (postagem.category.get_cat_list()[-1:]==segmentos[:-1]):
        if len(segmentos)==1 or (postagem.category.get_cat_list()[-1:]==segmentos[:-1]):
            context = {
                'postagem': postagem
            }
            return render(request, 'post.html', context)
        
        return render(request, 'post.html', {'context': f'{len(segmentos)} {postagem.category.get_cat_list()[-1:]} {segmentos[:-1]}'})
        

    else:
        categoria = Category.objects.filter(slug=ultimo_segmento)
        # categoria = get_object_or_404(Category, slug=ultimo_segmento)
        if categoria:
            # É uma categoria
            root_categories = Category.objects.filter(parent=None)
            category_tree = []
            for root_category in root_categories:
                category_tree.append(generate_category_tree(root_category))

            # categoria = categoria.first()
            categoria = categoria[0]
            context = {
                'categoria': categoria,
                'postagens': Post.objects.filter(category=categoria),
                'category_tree': category_tree
            }
            return render(request, 'categoria.html', context)


def generate_category_tree(category, current_path=''):
    category_path = current_path + '/' + category.slug if current_path else category.slug
    category_link = f'<a class="dropdown-item" href="/{category_path}">{category.name}</a>'

    subcategories = category.category_set.all()
    if subcategories:
        subcategory_links = [
            generate_category_tree(subcategory, category_path)
            for subcategory in subcategories
        ]
        subcategory_links_html = '<ul>' + ''.join(subcategory_links) + '</ul>'
        category_link += subcategory_links_html

    return f'<li>{category_link}</li>'




def generate_bootstrap_menu(category):
    menu_html = ""
    
    if category.active and category.on_menu:
        if category.megamenu:
            # Crie um Mega Menu
            menu_html += f'<li class="nav-item dropdown has-megamenu">\n'
            menu_html += f'  <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">{category.name}</a>\n'
            menu_html += f'  <div class="dropdown-menu megamenu" role="menu">\n'
            menu_html += f'    <div class="row g-3">\n'
            
            # Ordene as subcategorias com base no campo 'order'
            subcategories = category.category_set.filter(active=True, on_menu=True).order_by('order')
            
            for subcategory in subcategories:
                menu_html += '<div class="col-lg-3 col-6">'
                menu_html += f'<div class="col-megamenu">'
                menu_html += f'<h6 class="title"><a href="/{subcategory.slug}">{subcategory.name}</a></h6>'
                menu_html += '<ul class="list-unstyled">'
                
                # Ordene as subcategorias da subcategoria atual
                sub_subcategories = subcategory.category_set.filter(active=True, on_menu=True).order_by('order')
                
                for sub_subcategory in sub_subcategories:
                    menu_html += f'<li><a href="/{sub_subcategory.slug}">{sub_subcategory.name}</a></li>'
                    # Exibir as postagens relacionadas à sub-subcategoria
                    posts = Post.objects.filter(category=sub_subcategory).order_by('order', 'publish')
                    for post in posts:
                        menu_html += f'<li>🙌 <a href="/{sub_subcategory.slug}/{post.slug}">{post.title}</a></li>'

                # Exibir as postagens relacionadas à subcategoria
                posts = Post.objects.filter(category=subcategory).order_by('order', 'publish')
                for post in posts:
                    menu_html += f'<li>⭐ <a href="/{subcategory.slug}/{post.slug}">{post.title}</a></li>'

                menu_html += '</ul></div></div>'
            
            # Fim do conteúdo do Mega Menu
            menu_html += f'    </div>\n  </div>\n</li>'
        else:
            # Crie um item de menu Dropdown
            menu_html += f'<li class="nav-item dropdown">'
            menu_html += f'<a class="nav-link dropdown-toggle" href="#" id="/{category.slug}-dropdown" data-bs-toggle="dropdown" aria-expanded="false">{category.name}</a>'
            menu_html += f'<ul class="dropdown-menu" aria-labelledby="/{category.slug}-dropdown">'
            
            # Ordene as subcategorias com base no campo 'order'
            subcategories = category.category_set.filter(active=True, on_menu=True).order_by('order')
            
            # for subcategory in subcategories:
            #     menu_html += generate_bootstrap_menu(subcategory)
            # category_path = current_path + '/' + category.slug if current_path else category.slug
            for subcategory in subcategories:
                subcategory_link = generate_category_tree(subcategory, category.slug)
                menu_html += subcategory_link

            menu_html += '</ul></li>'

    return menu_html





MENU = """<nav class="navbar navbar-expand-lg navbar-dark bg-dark" aria-label="Eighth navbar example">
  <div class="container">
    <a class="navbar-brand" href="/">Católico Fiel</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample07" aria-controls="navbarsExample07" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarsExample07">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link" href="/biblia/">Bíblia</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="dropdown07" data-bs-toggle="dropdown" aria-expanded="false">Documentos</a>
          <ul class="dropdown-menu" aria-labelledby="dropdown07">
            <li><a class="dropdown-item" href="/docs/catecismo/">Catecismo</a></li>
            <li><a class="dropdown-item" href="#">Catecismo de Pio X</a></li>
            <li><a class="dropdown-item" href="#">Catecismo de Trento</a></li>
            <li><a class="dropdown-item" href="#">Didaque</a></li>
          </ul>
        </li>

        ###MEGAMENU###
        

        <li class="nav-item">
          <a class="nav-link" href="/criando_menu">Atualiza Menu</a>
        </li>
      </ul>
      <form action="{% url 'results' %}" method="POST" class="form-inline my-2 my-lg-0">{% csrf_token %}
       <input class="form-control" type="text" name="search" placeholder="Buscar no site" aria-label="Search">
      </form>
    </div>
  </div>
</nav>"""



def criando_menu(request, MENU=MENU):

    main_categories = Category.objects.filter(parent=None, active=True, on_menu=True).order_by('order', 'name')

    dropdown = []
    for main_category in main_categories:
        dropdown.append(generate_bootstrap_menu(main_category))
    dropdown = '\n'.join(dropdown)
    MENU = MENU.replace('###MEGAMENU###', dropdown)
    # from pathlib import Path
    # import os
    # # Build paths inside the project like this: BASE_DIR / 'subdir'.
    # BASE_DIR = Path(__file__).resolve().parent.parent
    # path = os.path.join(BASE_DIR, 'templates')

    with open('C:/Users/SONY/OneDrive/Documentos/_Gleson/Proj/mini_blog/templates/inc_navbar.html', 'w', encoding='utf-8') as file:
        file.write(MENU)

    # from django.conf import settings
    # templates_config = getattr(settings, 'TEMPLATES', None)
    from django.http import HttpResponse
    
    return HttpResponse('Template salvo com sucesso!')
    # return render(request, 'criando_menu.html', {'main_categories': main_categories, 'dropdown': dropdown})