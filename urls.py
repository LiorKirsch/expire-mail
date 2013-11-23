from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'expire_mail.views.home', name='home'),
    url(r'^viewlimited/(?P<image_id>\w+)', 'expire_mail.views.getViewlimited', name='getViewlimited'),
    url(r'^addViewlimited$', 'expire_mail.views.addViewlimited', name='addViewlimited'),
    
    # url(r'^expire_mail/', include('expire_mail.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
