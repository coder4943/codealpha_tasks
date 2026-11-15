from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from jobs.views import (
    apply_for_job,
    job_applications,
    job_detail,
    job_list,
    login_view,
    my_applications,
    post_job,
    signup,
    update_application_status,
    upload_resume,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', job_list),
    path('jobs/post/', post_job),
    path('jobs/<int:job_id>/', job_detail),
    path('jobs/<int:job_id>/apply/', apply_for_job),
    path('jobs/<int:job_id>/applications/', job_applications),
    path('applications/', my_applications),
    path('applications/<int:application_id>/status/', update_application_status),
    path('signup/', signup),
    path('login/', login_view),
    path('resume/', upload_resume),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)