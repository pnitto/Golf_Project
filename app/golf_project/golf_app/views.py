from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView, TemplateView
from rest_framework import serializers
from rest_framework import generics
from golf_app.converter import scatter_to_base64, scatter_to_base641, scatter_to_base642
from .models import Hole, Scorecard, Comment, Golfer
from .forms import UserForm, GolferForm
import seaborn


class IndexView(TemplateView):
    template_name = "golf_app/index.html"


def user_registration(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        golfer_form = GolferForm(data=request.POST)
        if user_form.is_valid() and golfer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            golfer = golfer_form.save(commit=False)
            golfer.player = user
            golfer.save()
            registered = True
            return redirect("golf_app:login")
        else:
            pass
    else:
        user_form = UserForm()
        golfer_form = GolferForm()
    return render_to_response('registration/create_user.html',{'user_form': user_form, 'golfer_form': golfer_form, 'registered': registered} , context)



@login_required(login_url='golf_app:login')
def graphs(request):
    golfer = Golfer.objects.get(player=request.user)
    top_score = Scorecard.objects.get_best_scorecard(golfer)
    top_player_scores = Scorecard.objects.top_5_player_scores(golfer)
    top_player_gir = Scorecard.objects.top_5_gir(golfer)
    top_player_fir = Scorecard.objects.top_5_fir(golfer)

    graph_one = scatter_to_base64((range(len((golfer.scores_for_scorecards))), (golfer.scores_for_scorecards)), request.user)
    data = (request.user.golfer.par_type_list, range(len((golfer.gir_for_scorecards))))
    graph_two = scatter_to_base641(data, request.user)

    data1= (request.user.golfer.par_type_list, range(len((golfer.fir_for_scorecards))))
    graph_three = scatter_to_base642(data1, request.user)
    return render_to_response('golf_app/scorecard_graphs.html', {"graph_one": graph_one,
                                                                 "graph_two": graph_two,
                                                                 "graph_three": graph_three,
                                                                 "top_score": top_score,
                                                                 "top_player_scores" : top_player_scores,
                                                                 "top_player_gir": top_player_gir,
                                                                 "top_player_fir": top_player_fir,}, context_instance=RequestContext(request))

def home(request):

    #golfer = Golfer.objects.get(player=request.user)
    #top_score = Scorecard.objects.get_best_scorecard(golfer)
    context = {}
    return render_to_response("home.html", context, context_instance=RequestContext(request))

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
    fields = ['par_type','player_score','green_in_regulation', 'fairway_in_regulation']
    template = "hole_form.html"
    success_url = reverse_lazy("golf_app:scorecard_detail")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scorecard_pk'] = self.kwargs.get('pk')
        return context

    def form_valid(self, form):
        score_pk = Hole.objects.get(id=self.kwargs['pk']).scorecard.id
        form.instance.scorecard_id = score_pk
        form.instance.scorecard = Hole.objects.get(id=self.kwargs['pk']).scorecard
        self.success_url = reverse_lazy("golf_app:scorecard_detail", kwargs={'pk': score_pk})
        return super().form_valid(form)

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(HoleUpdateView, self).dispatch(*args, **kwargs)


class HoleCreateView(CreateView):
    model = Hole
    fields = ['hole_number','par_type','player_score', 'green_in_regulation', 'fairway_in_regulation']
    template_name = "golf_app/create_hole.html"
    #success_url = reverse_lazy("golf_app:scorecard_detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scorecard_pk'] = self.kwargs.get('pk')
        return context

    #Thank you Bekk!!!!!! He helped me a lot with this!!
    def form_valid(self, form):
        score_pk = self.kwargs['pk']
        form.instance.scorecard_id = self.kwargs['pk']
        form.instance.scorecard = Scorecard.objects.get(id=self.kwargs['pk'])
        self.success_url = reverse_lazy("golf_app:scorecard_detail", kwargs={'pk': score_pk})
        return super().form_valid(form)

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(HoleCreateView, self).dispatch(*args, **kwargs)


class HoleDetailView(DetailView):
    model = Hole
    fields = ['scorecard', 'hole_number', 'hole_length', 'player_score', 'green_in_regulation','fairway_in_regulation']
    success_url = reverse_lazy("golf_app:scorecard_detail")
    template = "golf_app/hole_detail.html"
    slug_field = "id"

    @method_decorator(login_required(login_url="golf_app:login"))
    def dispatch(self, *args, **kwargs):
        return super(HoleDetailView, self).dispatch(*args, **kwargs)


class HoleDeleteView(DeleteView):
    model = Hole

    def get_success_url(self):
        return reverse('golf_app:scorecard_detail', kwargs={'pk':self.object.scorecard.pk})


class ScorecardListView(ListView):
    model = Scorecard
    fields = ['player', 'course_name','par_total', 'course_length', 'timestamp']
    template = "scorecard_list.html"
    success_url = reverse_lazy("golf_app:scorecard_history")

    def get_queryset(self):
        return Scorecard.objects.filter(player__player=self.request.user)

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(ScorecardListView, self).dispatch(*args, **kwargs)

class ScorecardDetailView(DetailView):
    model = Scorecard
    template = "scorecard_detail.html"

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(ScorecardDetailView, self).dispatch(*args,**kwargs)


class ScorecardCreateView(CreateView):
    model = Scorecard
    fields = ['course_name','par_total']
    template = "scorecard_form.html"
    #success_url = reverse_lazy("golf_app:scorecard_history")

    def form_valid(self, form):
        golfer = Golfer.objects.get(player=self.request.user)
        form.instance.player = golfer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('golf_app:scorecard_detail', kwargs={'pk':self.object.id})

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(ScorecardCreateView, self).dispatch(*args, **kwargs)



class ScorecardDeleteView(DeleteView):
    model = Scorecard
    success_url = reverse_lazy("golf_app:scorecard_history")

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(ScorecardDeleteView, self).dispatch(*args, **kwargs)


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

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(CommentUpdateView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(player__player=self.request.user)

class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('golf_app:comment_history')

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(CommentDeleteView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(player__player=self.request.user)

class CommentCreateView(CreateView):
    model = Comment
    fields = ['course_name', 'comment', 'course_rating']
    template = "comment_form.html"
    success_url = reverse_lazy('golf_app:comment_history')

    def form_valid(self, form):
        golfer = Golfer.objects.get(player=self.request.user)
        form.instance.player = golfer
        return super().form_valid(form)

    def get_queryset(self):
        return Comment.objects.filter(player__player=self.request.user)

    @method_decorator(login_required(login_url='golf_app:login'))
    def dispatch(self, *args, **kwargs):
        return super(CommentCreateView, self).dispatch(*args, **kwargs)