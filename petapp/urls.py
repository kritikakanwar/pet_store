"""
URL configuration for petstoreproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import PetList,PetDetail, petlistviewCM,search
from django.conf import settings
from django.conf.urls.static import static
from .import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v.menu,name='menu'),
    path('petlist/',PetList.as_view(),name='petList'),
    path('petdetail/<slug:slug>/',PetDetail.as_view(),name='petdetail'),
    path('petlistage/',petlistviewCM.as_view(),name='petlistage'),
    path('search/',v.search,name='Search'),
    path('register/',v.registration,name='register'),
    path('login/',v.login,name='Login'),
    path('addtocart/',v.addtocart,name='atc'),
    path('viewcart/',v.viewcart,name='vc'),
    path('changequantity',v.changequantity,name='cq'),
    path('summary/',v.summarypage,name='summary'),
    path('placeorder/',v.placeorder,name='placeorder'),
    path('logout/',v.login,name='Logout'),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)