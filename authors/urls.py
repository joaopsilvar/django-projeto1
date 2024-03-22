from django.urls import path
from. import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/recipe/new/', views.DashboardRecipeNew.as_view(), name='dashboard_recipe_new'),
    path('dashboard/recipe/<int:id>/edit/', views.DashboardRecipeEdit.as_view(), name='dashboard_recipe_edit'),
]
