from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Template

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
        # Testa se o slug do post está no raiz ou se as categorias da url estão corretas
        if len(segmentos)==1 or (postagem.category.get_cat_list()==segmentos[:-1]):
            context = {
                'postagem': postagem
            }
            return render(request, 'post.html', context)
        
    else:
        # categoria = Category.objects.filter(slug=ultimo_segmento)
        categoria = get_object_or_404(Category, slug=ultimo_segmento)        
        if categoria.exists():
            # É uma categoria
            root_categories = Category.objects.filter(parent=None)
            category_tree = []
            for root_category in root_categories:
                category_tree.append(generate_category_tree(root_category))
            
            categoria = categoria.first()
            context = {
                'categoria': categoria,
                'postagens': Post.objects.filter(category=categoria),
                'category_tree': category_tree
            }
            return render(request, 'categoria.html', context)



# def my_view(request, url):
#     # Dividir a URL pelos segmentos ("/")
#     segmentos = url.split('/')

#     # Verificar se o último segmento é um slug ou uma categoria
#     ultimo_segmento = segmentos[-1]
#     if re.match(r'^[-\w]+$', ultimo_segmento):  # Verifica se é um slug válido
#         # É um post
#         postagem = Post.objects.get(slug=ultimo_segmento)
#         print('/'.join(postagem.category.get_cat_list()))
#         context = {
#             'postagem': postagem,
#             'caminho_completo': '/'.join(postagem.category.get_cat_list()) + '/' + ultimo_segmento
#         }
#         return render(request, 'post.html', context)
#     else:
#         # É uma categoria
#         categoria = Category.objects.get(slug=ultimo_segmento)
#         context = {
#             'categoria': categoria
#         }
#         return render(request, 'categoria.html', context)

def generate_category_tree(category, current_path=''):
    category_path = current_path + '/' + category.slug if current_path else category.slug
    category_link = f'<a href="/{category_path}">{category.name}</a>'
    
    subcategories = category.category_set.all()
    if subcategories:
        subcategory_links = [
            generate_category_tree(subcategory, category_path)
            for subcategory in subcategories
        ]
        subcategory_links_html = '<ul>' + ''.join(subcategory_links) + '</ul>'
        category_link += subcategory_links_html

    return f'<li>{category_link}</li>'


