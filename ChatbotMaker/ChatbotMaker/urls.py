"""ChatbotMaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DesignerApp import views
urlpatterns = [
    path('admin/', admin.site.urls),#Admin Site
    path('test/', views.test, name='test'),#Test Site
    # path('login/', views.login, name='login'),#Stale Login Page
    path('assistants/', views.get_assistants, name='get_assistants'),#Gives a list of all assistants with details
    path('assistants/<str:assistant_sid>/', views.get_assistant, name='get_assistant'),#Useless
    path('assistants/<str:assistant_sid>/tasks/', views.get_tasks, name='get_tasks'),#Gives tasks page where you see details of all your tasks
    path('assistants/<str:assistant_sid>/tasks/<str:task_sid>/', views.get_task, name='get_task'),#Gets the specific edit page for a Task
    # path('assistants/<str:assistant_sid>/tree/tasks/<str:task_sid>/', views.get_relationships, name='get_relationships'),#Shows a page with the tree of tasks.
    path('assistants/<str:assistant_sid>/tree/', views.tree, name='tree'),#Shows a page with the tree of tasks.
    # path('assistants/<str:assistant>/tasks/create_task', views.create_task, name='create_task'),#Create a whole new task.
]
