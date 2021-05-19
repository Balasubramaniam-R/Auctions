from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name='auctions'

urlpatterns = [
    path("",views.active_list,name="active_list"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("all_list",views.all_list,name="all_list"),
    path("watch_list",views.watch_list,name="watch_list"),
    path("create",views.create,name="create"),
    path("item/<int:item_id>",views.entry,name="entry"),
    path("item/<int:item_id>/bid/<int:cur_bid_id>",views.bid,name="bid"),
    path("close/<int:item_id>",views.close,name="close"),
    path("add/<int:item_id>/bid/<int:cur_bid_id>",views.add_to_watch_list,name="add_to_watch_list"),
    path("remove/<int:item_id>/bid/<int:cur_bid_id>",views.remove_from_watch_list,name="remove_from_watch_list"),
    path("add_comment/<int:item_id>",views.add_comment,name="add_comment"),
    path("categories/<int:category_id>/active/<str:is_active>",views.Categories,name="Categories"),


    
]

#urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)