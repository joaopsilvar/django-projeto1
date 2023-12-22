from django.shortcuts import render
from django.http import HttpResponse
from utils.recipes.factory import make_recipe
from .models import Recipe,Category
from django.http import Http404

# Create your views here.

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request,'recipes/pages/home.html',context={
        'recipes': recipes,
    })

def category(request,category_id):
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True).order_by('-id')
    
    if not recipes:
        raise Http404('Not Found')


    return render(request,'recipes/pages/category.html',context={
        'recipes': recipes,
        'title' : f'{recipes.first().category.name} - Category | '
    })

def recipe(request, id):
    recipe = Recipe.objects.get(
        id=id,
        is_published=True
    )
    return render(request,'recipes/pages/recipe-view.html',context={
        'recipe': recipe,
        'is_detail_page': True,
    })

def search(request,search_text):
    recipes = Recipe.objects.filter(title=search_text)
    return render(request,'recipes/pages/home.html',context={
        'recipes': recipes,
    })
