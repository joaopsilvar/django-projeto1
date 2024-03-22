from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe
from authors.forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class Register(View):
    def get(self,request):
        register_form_data = request.session.get('register_form_data', None)
        form = RegisterForm(register_form_data)
        return render(request, 'authors/pages/register_view.html', {
            'form': form,
            'form_action': reverse('authors:register'),
        })

    def post(self,request):
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

class Login(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'authors/pages/login.html', {
            'form': form,
            'form_action': reverse('authors:login')
        })

    def post(self,request):
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

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class Logout(View):
    def post(self,request):
        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Invalid logout user')
            return redirect(reverse('authors:login'))

        messages.success(request, 'Logout out successfully')
        logout(request)
        return redirect(reverse('authors:login'))

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)   
class Dashboard(View):
    def get(self,request):
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

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeEdit(View):
    def get_recipe(self, id):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )

    def get(self, request, id):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id):
        recipe = self.get_recipe(id)
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
            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(id,))
            )

        return self.render_recipe(form)

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeNew(View):
    def get(self,request):
        register_form_data = request.session.get('register_form_data', None)
        form = AuthorRecipeForm(register_form_data)
        return render(request, 'authors/pages/dashboard_recipe.html', {
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_new')
        })
     
    def post(self,request):
        request.session['register_form_data'] = request.POST
        #salvar arquivos na sessão implementar
        
        form = AuthorRecipeForm(
            data=request.POST,
            files=request.FILES,
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

@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(View):
    def post(self,request):        
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