from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from ribbit_app.forms import UserCreateForm, RibbitForm
from ribbit_app.models import Ribbit


def index(request, auth_form=None, user_form=None):
    # User id logged in
    if request.user.is_authenticated():
        ribbit_form = RibbitForm()
        ribbit_form.fields["content"].widget.attrs['class'] = "ribbitText"
        user = request.user
        ribbit = Ribbit.objects.filter(user=user.id).latest('creation_date')
        return render(request,
                      'buddies.html',
                      {'ribbit_form': ribbit_form, 'user': user,
                       'ribbit': ribbit,
                       'next_url': '/', })
    else:
        # User is either not logged in or is anonymous
        auth_form = auth_form or AuthenticationForm()
        user_form = user_form or UserCreateForm()

        auth_form.fields['username'].widget.attrs['placeholder'] = "Username"
        auth_form.fields['password'].widget.attrs['placeholder'] = "Password"

        for key, error in auth_form.errors.iteritems():
            auth_form.fields[key].widget.attrs['value'] = ''.join(error)
            auth_form.fields[key].widget.attrs['class'] = "error"

        user_form.fields['username'].widget.attrs['placeholder'] = "Username"
        user_form.fields['password1'].widget.attrs['placeholder'] = "Password"
        user_form.fields['password2'].widget.attrs['placeholder'] = "Password Confirmation"
        user_form.fields['email'].widget.attrs['placeholder'] = "Email"
        user_form.fields['first_name'].widget.attrs['placeholder'] = "First Name"
        user_form.fields['last_name'].widget.attrs['placeholder'] = "Last Name"

        for key, error in user_form.errors.iteritems():
            user_form.fields[key].widget.attrs['value'] = ''.join(error)
            user_form.fields[key].widget.attrs['class'] = "error"

        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 'user_form': user_form, })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')


@login_required
def public(request, ribbit_form=None):
    ribbit_form = ribbit_form or RibbitForm()
    ribbit_form.fields["content"].widget.attrs['class'] = "ribbitText"
    ribbits = Ribbit.objects.reverse()[:10]
    return render(request,
                  'public.html',
                  {'ribbit_form': ribbit_form, 'next_url': '/public',
                   'ribbits': ribbits, })


@login_required
def submit(request):
    if request.method == "POST":
        ribbit_form = RibbitForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if ribbit_form.is_valid():
            ribbit = ribbit_form.save(commit=False)
            ribbit.user = request.user
            ribbit.save()
            return redirect(next_url)
        else:
            ribbit_form.fields["content"].widget.attrs['class'] = "ribbitText error"
            ribbit_form.fields["content"].widget.attrs['placeholder'] = ''.join(ribbit_form.errors['content'])
            return public(request, ribbit_form)
    return redirect('/')
