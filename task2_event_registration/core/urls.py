from django.contrib import admin
from django.urls import path

from events.views import (
    cancel_registration,
    event_detail,
    event_list,
    login_view,
    my_registrations,
    register_for_event,
    signup,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', event_list),
    path('events/<int:event_id>/', event_detail),
    path('events/<int:event_id>/register/', register_for_event),
    path('registrations/', my_registrations),
    path('registrations/<int:registration_id>/cancel/', cancel_registration),
    path('signup/', signup),
    path('login/', login_view),
]