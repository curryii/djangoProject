from django.urls import path
from projects import views
from projects.views import ProjectView, ProjectViewId

"""
定义类视图路由
path('project/', ProjectView.as_view())
"""

urlpatterns = [
    path('project/', ProjectView.as_view()),
    path('project/<int:id>/', ProjectViewId.as_view())
]
