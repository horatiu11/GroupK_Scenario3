from django.conf.urls import url

from . import views

app_name = 'mainapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^authentication/$', views.authentication, name='authentication'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^mainpage/$', views.mainpage, name='mainpage'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^addref/$', views.addref, name='addref'),
    url(r'^deleteref/$', views.deleteref, name='deleteref'),
    url(r'^deletelist/$', views.deletelist, name='deletelist'),
    url(r'^saveref/$', views.saveref, name='saveref'),
    url(r'^errormsg/$', views.errormsg, name='errormsg'),
]