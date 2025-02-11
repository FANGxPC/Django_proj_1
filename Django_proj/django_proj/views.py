from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,Entryform
                        ####Purpose: Handles the logic of processing user requests and returning responses.


# Create your views here.
def index(request):
    return render(request, 'index.html')

def topics(request):
    topics=Topic.objects.order_by('date_added')
    context={'topics':topics}
    return render(request, 'topics.html',context)

def topic(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    entries=topic.entry_set.order_by('-date_added')
    context={'topic':topic,'entries':entries}
    return render(request,'topic.html',context)


def new_topic(request):
    if request.method!='POST':
        form=TopicForm()
    else:
        form=TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_proj:topics')
        
    context={'form':form}
    return render(request,'new_topic.html',context)


def new_entry(request,topic_id):
    topic=Topic.objects.get(id=topic_id)
    if request.method!='POST':
        form=Entryform()
    else:
        form=Entryform(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=topic
            new_entry.save()
            return redirect('django_proj:topic',topic_id=topic_id)
        
    context={'topic':topic,'form':form}
    return render(request,'new_entry.html',context)