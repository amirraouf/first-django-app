"""
^ for beginning of the text
$ for end of text
\d for a digit
+ to indicate that the previous item should be repeated at least once
() to capture part of the pattern
"""
import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from courses.views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^categories/$', categories, name='categories'),
    url(r'^profile/(?P<slug>[-\w]+)/$', profiler, name='profile'),
    url(r'^categories/(?P<category_name>[-\w]+)/$', categories_pages, name='category_detail'),
    url(r'^categories/(?P<category_name>[-\w]+)/(?P<spec_name>[-\w]+)$', specs_categories_pages, name='spec_detail'),
    url(r'^course/(?P<course_name>[-\w]+)/$', courses_detail, name='course_detail'),
    url(r'^register/$', register, name='register'),
    url(r'^register/choose_your_type/$', choose_your_type, name='choose_type'),

    url(r'^register/register_success/$', register_success, name='register_success'),
    url(r'^login/$', c_login, name='login'),
    url(r'^logout/$', logout_page, name='logout'),
    #url(r'^complete_registeration/$', register_complete_type, name='choose_type'),
    url(r'^no/$', course_create, name='no'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
