"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from boards import views
urlpatterns = [
    url(r'^$',views.BoardListView.as_view(),name='home'),
    url(r'^signup/$',accounts_views.signup,name='signup'),
    url(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'^boards/(?P<pk>\d+)/$',views.TopicListView.as_view(),name='board_topics'),#FCV分页
    url(r'^boards/(?P<pk>\d+)/new/$',views.new_topic,name='new_topic'),
    url(r"^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$",views.topic_posts,name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',views.reply_topic,name='reply_topic'),
    url(r'^new_post/$',views.NewPostView.as_view(),name='new_post'),
    url(r'^boards/(?P<pk>\d+)topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(),name='edit_post'),
    url(r'^settings/account/$',accounts_views.UserUpdateView.as_view(),name='my_account'),
    url(r'^admin/', admin.site.urls),

]
