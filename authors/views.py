from django.shortcuts import render, redirect
from authors.forms import RegisterForm
from django.http import Http404

def register_view(request): 
    #request.session['number'] = request.session.get('number') or 1
    #request.session['number'] += 1

    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm()

    #print(form)

    return render(request, 'authors/pages/register_view.html', {
        'form': form
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    #print(POST)

    return redirect('authors:register')
