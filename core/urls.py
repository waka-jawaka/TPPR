from django.urls import path

from . import views


urlpatterns = [
	path('decision-paretto/', views.paretto_view, name='paretto_view'),
	path('normalized/(?P<normalize_data>\w+)', views.normalized_view, name='normalized_view'),
	path('weights/', views.weights_view, name='weights_view'),
	path('', views.basic_decision, name='decision'),
]