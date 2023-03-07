from django.urls import path
from projects import views
from projects.views import ProjectView

"""
定义类视图路由
path('project/', ProjectView.as_view())
"""

urlpatterns = [
    path('project/<int:pk>/', ProjectView.as_view())
]
