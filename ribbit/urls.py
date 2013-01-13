from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'ribbit_app.views.index'),
    url(r'^login$', 'ribbit_app.views.login_view'),
    url(r'^logout$', 'ribbit_app.views.logout_view'),
    url(r'^signup$', 'ribbit_app.views.signup'),
    url(r'^ribbits$', 'ribbit_app.views.public'),
    url(r'^submit$', 'ribbit_app.views.submit'),
    url(r'^users/$', 'ribbit_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'ribbit_app.views.users'),
    url(r'^follow$', 'ribbit_app.views.follow'),
    # url(r'^ribbit/', include('ribbit.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
