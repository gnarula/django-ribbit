from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from ribbit_app.forms import UserCreateForm, RibbitForm
from ribbit_app.models import Ribbit


def index(request, auth_form=None, user_form=None):
    # User id logged in
    if request.user.is_authenticated():
        ribbit_form = RibbitForm()
        ribbit_form.fields["content"].widget.attrs['class'] = "ribbitText"
        user = request.user
        ribbits_self = Ribbit.objects.filter(user=user.id)
        ribbits_buddies = Ribbit.objects.filter(user__userprofile__in=user.profile.follows.all)
        ribbits = ribbits_self | ribbits_buddies

        return render(request,
                      'buddies.html',
                      {'ribbit_form': ribbit_form, 'user': user,
                       'ribbits': ribbits,
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


def get_latest(user):
    return user.ribbit_set.order_by('id').reverse()[0]


@login_required
def users(request, username="", ribbit_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        ribbits = Ribbit.objects.filter(user=user.id)
        if username == request.user.username or request.user.profile.follows.filter(user__username=username):
            # Self Profile
            return render(request, 'user.html', {'user': user, 'ribbits': ribbits, })
        return render(request, 'user.html', {'user': user, 'ribbits': ribbits, 'follow': True })
    users = User.objects.all()
    ribbits = map(get_latest, users)
    obj = zip(users,ribbits)
    ribbit_form = ribbit_form or RibbitForm()
    ribbit_form.fields["content"].widget.attrs['class'] = "ribbitText"
    return render(request, 'profiles.html', {'obj': obj, 'next_url': '/users/', 'ribbit_form': ribbit_form })

@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
