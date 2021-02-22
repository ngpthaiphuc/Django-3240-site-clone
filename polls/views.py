from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
#from django.template import loader

from .models import Choice, Question, Thought
#from .forms import InputForm
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def thought_button():
    return HttpResponseRedirect(reverse('polls:thoughts'))
    #this code doesn't do anything...?

class ThoughtView(generic.CreateView):
    model = Thought
    template_name = 'polls/thought_form.html'
    fields = ["title_field", "description_field"]
    #labels = {"title_field": "Thought Title", "description_field": "Description", }
    success_url = "thoughts/list"
    #def get_success_url(self):
    #    return reverse('thought-detail', kwargs={'pk': self.pk})

'''
def thought_input(request):
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = InputForm()
    return render(request, 'polls/thought.html', {'input': form})
'''

def thought_list(request):
    thoughts = Thought.objects.all()
    return render(request, 'polls/list.html', {'thoughts_list': thoughts})
'''
class ThoughtList(generic.ListView):
    template_name = 'polls/list.html'
    context_object_name = 'thoughts_list'

    def get_queryset(self):
        return Thought.objects.all()
'''