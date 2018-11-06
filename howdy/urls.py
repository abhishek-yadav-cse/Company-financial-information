from django.conf.urls import url
from howdy import views


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    # url(r'^$', views.AboutPageView.as_view()), # Add this /about/ route
    url(r'^result', views.HomePageView.as_view()),
]