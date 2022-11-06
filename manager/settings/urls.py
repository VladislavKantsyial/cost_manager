from django.urls import path
from .views import SettingsListView

urlpatterns = [
    path("settings/", SettingsListView.as_view(), name="settings"),
]
