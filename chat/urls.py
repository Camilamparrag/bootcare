from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("<int:user_id>/", views.conversation, name="conversation"),
    path("send/<int:receiver_id>/", views.send_message, name="send"),
]
