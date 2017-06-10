from django.conf.urls import url
from . import views

urlpatterns = (
    # url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    # url(r'^stokvel/$', views.StokvelView.as_view(), name='stokvel'),
    # url(r'^stokvel/pay/$', views.PayStokvelView.as_view(), name='pay-stokvel'),
    # url(r'^event/$', views.EventView.as_view(), name='event'),
    # url(r'^vote/$', views.VoteView.as_view(), name='vote'),
)