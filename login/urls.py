"""CS3240F18 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from .views import(
	send_friend_request,
	friend_requests,
	accept_friend_request,
	remove_friend,
	decline_friend_request,
	cancel_friend_request,
    register_view,
    main_page,
    search,
    find,
    showPricing,
    hoosaroundme,
    login_view,
    friends_list_view,
    account_view,
)
app_name = 'map'
urlpatterns = [
    path('', main_page, name='home'),
    path('', main_page, name='main-page'),
    path('search', search, name='search-page'),
    path('find', find, name='find-page'),
    path('pricing', showPricing, name='pricing-page'),
    path('hoosaroundme', hoosaroundme, name='hoosaroundme-page'),
    path('register', register_view, name = 'register'),
    path('logina', login_view, name = 'login'),
    path('view/<user_id>/', account_view, name="account_view"),
    path('list/<user_id>', friends_list_view, name='list'),
	path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request/', send_friend_request, name='friend-request'),
    path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),
    path('friend_requests/<user_id>/', friend_requests, name='friend-requests'),
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
]
