from django.urls import path
from interfaces import views
from interfaces.views import InterfaceView, InterfaceViewId

urlpatterns = [
    path('interface/', InterfaceView.as_view()),
    path('interface/<int:pk>/', InterfaceViewId.as_view())
]
