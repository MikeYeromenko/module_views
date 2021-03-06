"""module URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from modshop import views

urlpatterns = [
    path('', views.start_page, name='start'),
    path('admin/', admin.site.urls),
    path('registration/', views.RegisterUser.as_view(), name='registration'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('shopping/', views.GoodsListView.as_view(), name='shopping'),
    # path('purchase/<int:pk>/<int:id_goods>', views.PurchaseCreateView.as_view(), name='purchase'),
    path('purchase/<int:pk>/', views.PurchaseCreateView.as_view(), name='purchase'),
    path('purchases/', views.PurchesListView.as_view(), name='purchases'),
    path('return/<int:pk>/', views.GoodsReturnView.as_view(), name='return'),
    path('goods_update/<int:pk>/', views.GoodsUpdateView.as_view(), name='goods_update'),
    # path(r'^goods_update/(?P<pk>\d+)/$', views.GoodsUpdateView.as_view(), name='goods_update'),
    path('goods_add/', views.GoodsCreateView.as_view(), name='goods_add'),
    path('goods_return_list/', views.GoodsReturnAdminView.as_view(), name='goods_return'),
    path('return_decision/<int:pk>/', views.WorkWithReturnView.as_view(), name='return_decision'),
]
