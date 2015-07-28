from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from rest_framework import serializers
from rest_framework import generics
from .models import Hole, Scorecard, Comment


def user_registration(request):
    if request.POST:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_form = UserCreationForm({
            'username': username,
            'password1': password1,
            'password2': password2,
        })
        try:
            user_form.save(commit=True)
            return HttpResponseRedirect("accounts/login")
        except ValueError:
            return render_to_response("registration/create_user.html",
                                      {'form': user_form},
                                      context_instance=RequestContext(request))

    return render_to_response("registration/create_user.html",
                              {'form': UserCreationForm()},
                              context_instance=RequestContext(request))


def home(request):
    context = {}
    return render_to_response("base.html", context, context_instance=RequestContext(request))


# Not sure if I even need serializers yet!!
class HoleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hole
        fields = ['scorecard', 'hole_number', 'par_type', 'hole_length',
                  'player_score', 'green_in_regulation', 'fairway_in_regulation', 'timestamp']


class HoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hole
        fields = ['hole_number', 'par_type', 'hole_length', 'player_score', 'green_in_regulation',
                  'fairway_in_regulation']


class HoleListView(ListView):
    model = Hole
    # fields = ['hole_number','par_type','hole_length', 'player_score','green_in_regulation', 'fairway_in_regulation']
    template = "scorecard_detail.html"
    success_url = reverse_lazy("golf_app:scorecard_detail")


class HoleUpdateView(UpdateView):
    model = Hole
    fields = ['player_score', 'green_in_regulation', 'fairway_in_regulation']
    template = "hole_form.html"
    success_url = reverse_lazy("golf_app:scorecard_detail")
# I need this view to go back to the scorecard

class HoleCreateView(CreateView):
    model = Hole
    fields = ['hole_number','par_type','player_score', 'green_in_regulation', 'fairway_in_regulation']
    template = "create_hole.html"
    success_url = reverse_lazy("golf_app:scorecard_detail")

    #Thank you Bekk!!!!!! He helped me a lot with this!!
    def form_valid(self, form):
        score_pk = self.kwargs['pk']
        form.instance.scorecard_id = self.kwargs['pk']
        form.instance.scorecard = Scorecard.objects.get(id=self.kwargs['pk'])
        self.success_url = reverse_lazy("golf_app:scorecard_detail", kwargs={'pk': score_pk})
        return super().form_valid(form)


class HoleDetailView(DetailView):
    model = Hole
    fields = ['scorecard', 'hole_number', 'par_type', 'hole_length', 'player_score', 'green_in_regulation',
              'fairway_in_regulation']
    #Need this view to go back to the scorecard
    success_url = reverse_lazy("golf_app:scorecard_detail")
    template = "hole_detail.html"
    slug_field = "id"


class ScorecardListView(ListView):
    model = Scorecard
    fields = ['player', 'course_name', 'course_length', 'timestamp']
    template = "scorecard_list.html"
    success_url = reverse_lazy("golf_app:scorecard_history")


class ScorecardDetailView(DetailView):
    model = Scorecard
    template = "scorecard_detail.html"


class ScorecardCreateView(CreateView):
    model = Scorecard
    fields = ['course_name']
    template = "scorecard_form.html"
    success_url = reverse_lazy("golf_app:scorecard_history")


class CommentListView(ListView):
    model = Comment
    fields = ['player', 'course_name', 'comment', 'course_rating', 'timestamp']
    template = "course_list.html"
    success_url = reverse_lazy('golf_app:comment_history')


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ['course_name', 'comment', 'course_rating']
    template = "comment_form.html"
    success_url = reverse_lazy('golf_app:comment_history')


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('golf_app:comment_history')


class CommentCreateView(CreateView):
    model = Comment
    fields = ['player', 'course_name', 'comment', 'course_rating']
    template = "comment_form.html"
    success_url = reverse_lazy('golf_app:comment_history')
