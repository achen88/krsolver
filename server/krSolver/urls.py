from django.urls import path, re_path

from . import views

urlpatterns = [
	re_path('(?P<cookie>[a-zA-Z0-9_]*)/(?P<captchaUrl>.*)', views.solve, name='solve'),
]
