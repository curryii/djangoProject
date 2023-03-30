from django.urls import path
from projects import views
from projects.views import ProjectView, ProjectViewId, ProjectViewSet

"""
定义类视图路由
path('project/', ProjectView.as_view())
"""

"""path('project/', ProjectView.as_view()),
    path('project/<int:id>/', ProjectViewId.as_view()),"""

urlpatterns = [
    path("project/", views.ProjectViewSet.as_view({
        "get": "list",
        "post": "create"
    })),
    path("project/<int:id>/", views.ProjectViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy"
    }))
]
