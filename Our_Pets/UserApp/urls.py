from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    
    path('',views.homepage),
    path('login',views.login),
    path('signup',views.signup),
    path('logout',views.logout),
    path('viewsSection/<id>', views.viewsSection),
    path('showPets/<id>',views.showPets),
    path('readMore/<id>',views.readMore),
    path('addTocart',views.addTocart),
    path('showAllCart',views.showAllCart),
    path('remove',views.removeItem),
    path('MakePayment',views.MakePayment),
    path('otp',views.otp),
    path('license',views.license),
    path('about',views.about),
    path('gallary',views.gallary),
    path('contact',views.contact),
    
]


