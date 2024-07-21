from django.urls import path
from restroapp import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('index',views.index),
        path('about',views.about),
        path('search',views.search),
        path('contact',views.contact),
        path('menu',views.menu),
        path('signup',views.signup),
        path('login',views.user_login),
        path('logout',views.user_logout),
        path('sort/<sid>',views.sort),
        path('catfilter/<cid>',views.catfilter),
        path('pricefilter',views.pricefilter),
        path('place_order',views.place_order),
        path('products',views.products),
        path('products/<pid>',views.products),
        path('addtocart/<pid>',views.addtocart),
        path('cart',views.cart),
        path('updateqty/<x>/<cid>',views.updateqty),
        path('remove/<cid>',views.remove),
        path('place_order',views.place_order),
        path('fetchorder',views.fetchorder),
        path('makepayment',views.makepayment),
        path('success',views.success),
        
    
   
        ]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
