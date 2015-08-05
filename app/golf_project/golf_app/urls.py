
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from .views import home, HoleListView, HoleUpdateView, user_registration, HoleCreateView, HoleDetailView, \
    ScorecardListView, ScorecardCreateView, CommentListView, CommentUpdateView, CommentDeleteView, CommentCreateView, \
    ScorecardDetailView, ScorecardDeleteView, HoleDeleteView, IndexView, graphs
from django.contrib.auth.views import login, logout




urlpatterns = [
    url(r'^holes/$', HoleListView.as_view(),name="holes"),
    url(r'^update_hole/(?P<pk>\d+)/$', HoleUpdateView.as_view(),name="update_hole"),
    url(r'^home/$',home,name="home"),
    url(r'^registration/$', user_registration, name="user_registration"),
    url(r'^logout/$', logout, {'next_page': 'golf_app:home'}, name="logout"),
    url(r'^accounts/login/$',login, name="login"),
    url(r'^create_hole/(?P<pk>\d+)$', HoleCreateView.as_view(), name="create_hole"),
    url(r'^hole_detail/(?P<pk>\d+)/$', HoleDetailView.as_view(), name="hole_detail"),
    url(r'^scorecard_history/$', ScorecardListView.as_view(), name="scorecard_history"),
    url(r'^create_scorecard/$', ScorecardCreateView.as_view(), name="create_scorecard"),
    url(r'^comment_history/$', CommentListView.as_view(), name="comment_history"),
    url(r'^update_comment/(?P<pk>\d+)/$', CommentUpdateView.as_view(), name="update_comment"),
    url(r'^delete_comment/(?P<pk>\d+)$', CommentDeleteView.as_view(), name="delete_comment"),
    url(r'^create_comment/$', CommentCreateView.as_view(), name="create_comment"),
    url(r'^scorecard_detail/(?P<pk>\d+)$', ScorecardDetailView.as_view(), name="scorecard_detail"),
    url(r'^delete_scorecard/(?P<pk>\d+)$', ScorecardDeleteView.as_view(), name="delete_scorecard"),
    url(r'^delete_hole/(?P<pk>\d+)$', HoleDeleteView.as_view(), name="delete_hole"),
    url(r'^index/$', IndexView.as_view(), name="index"),
    url(r'^graph/$',graphs , name="graph"),

]