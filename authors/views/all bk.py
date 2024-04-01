from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from recipes.models import Recipe

from authors.forms.recipe_form import AuthorRecipeForm

from authors.forms import LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in.')

        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, f'Your are logged in with {authenticated_user}.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('authors:login'))

    messages.success(request, 'Logout out successfully')
    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(
        request,
        'authors/pages/dashboard.html',
        context={
            'recipes': recipes,
        }
    )

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    register_form_data = request.session.get('register_form_data', None)
    
    form = AuthorRecipeForm(register_form_data)
    return render(request, 'authors/pages/dashboard_recipe.html', {
        'form': form,
        'form_action': reverse('authors:dashboard_recipe_create')
    })
     
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):
    if not request.POST:
        raise Http404()
    
    request.session['register_form_data'] = request.POST
    #salvar arquivos na sessão implementar
    
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        # Agora, o form é válido e eu posso tentar salvar
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        
        recipe_title_filter = Recipe.objects.filter(title=recipe.title)
        if recipe_title_filter:
            messages.error(request, 'Ja existe uma receita com o nome informado!')
            return redirect(reverse('authors:dashboard_recipe_new'))
        
        recipe.save()
        messages.success(request, 'Sua receita foi salva com sucesso!')
        
        del(request.session['register_form_data'])
        return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
    
    return redirect(reverse('authors:dashboard_recipe_new'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        # Agora, o form é válido e eu posso tentar salvar
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Sua receita foi salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form
        }
    )

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404()
    
    id = request.POST.get('id')
    
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()
    
    recipe.delete()
    messages.success(request, 'Sua receita foi deletada com sucesso!')
    return redirect(reverse('authors:dashboard'))