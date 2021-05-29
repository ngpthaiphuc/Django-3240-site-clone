from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import FriendRequest, Account, FriendList
from django.db import connection
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, AccountAuthenticationForm, UpdateStatusForm, AccountUpdateForm, UpdateLocationForm
import json
from django.contrib.auth import logout
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.auth.hashers import make_password
import random
from .friend_request_status import FriendRequestStatus
from django.conf import settings
from .util import get_friend_request_or_false
# import allauth user account model if your find it

static_users = [
    {
        'userId': '5',
        'userName': 'Test Username',
        'email': 'hello@test.com',
        'homeLocation': '70.0321,-12.01233',
        'friends': ['John', 'Jonathan', 'Johan'],
        'savedLocations':{'Home,70.2913,-36.1239', 'Car,70.1293,-45.1293'},
    },
    {
        'userId': '5',
        'userName': 'Test Username',
        'email': 'hello@test.com',
        'homeLocation': '70.0321,-12.01233',
        'friends': ['John', 'Jonathan', 'Johan'],
        'savedLocations':{'Home,70.2913,-36.1239', 'Car,70.1293,-45.1293'},
    },
    {
        'userId': '5',
        'userName': 'Test Username',
        'email': 'hello@test.com',
        'homeLocation': '70.0321,-12.01233',
        'friends': ['John', 'Jonathan', 'Johan'],
        'savedLocations':{'Home,70.2913,-36.1239', 'Car,70.1293,-45.1293'},
    },
    {
        'userId': '5',
        'userName': 'Test Username',
        'email': 'hello@test.com',
        'homeLocation': '70.0321,-12.01233',
        'friends': ['John', 'Jonathan', 'Johan'],
        'savedLocations':{'Home,70.2913,-36.1239', 'Car,70.1293,-45.1293'},
    },
]


# Create your views here.

def showPricing(request):
    print("REQUEST - showPricing")
    # queryW
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    # models: django.contrib.auth.models.User
    # models: allauth.account.models.EmailAddress
    # models: login.models.User

    #User_list = User.objects.all()
    User_list = static_users
    context = {'users_list': User_list}

    # when we pass a context to the render function alongside a template, we can access that variable and loop over its contents with:
    # {% for anything in <Key in context>%}
    # >> inside the for loop, we have access to every object in {{ post.title }}
    # always end for loops with {% endfor %}
    return render(request, 'login/pricing.html', context)
    # return render(request, 'login/login.html', User.objects.all())

# save current location


def saveCurrentLocation(user):
    loc = user.savedLocations

# Search button directs to search page


def search(request, *args, **kwargs):
    context = get_friends_list(request, *args, **kwargs)
    return render(request, 'login/search.html', context)

def find(request, *args, **kwargs):
    context = get_friends_list(request, *args, **kwargs)
    return render(request, 'login/find.html', context)

#/***************************************************************************************
#*  REFERENCES
#*  Title: Real-time Chat Messenger (only for account and friends system)
#*  Author: CodingWithMitch
#*  Date: Oct 16th, 2020
#*  URL: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9KUJZJUmnDFYQfVyXYjX6r
#*
#***************************************************************************************/

def friends_list_view(request, *args, **kwargs):
    context = get_friends_list(request, *args, **kwargs)
    print(context)
    if 'users_list' in context.keys():
        context['friends'] = context['users_list']
    
    context['users_list'] = get_friends_list(request)['users_list']
    return render(request, "login/friend_list.html", context)

def account_view(request, *args, **kwargs):
    if (not request.user.is_authenticated):
        context = {}
        context['not_loggedin'] = True
        return render(request, "login/main_page_noupdate.html", context)
    context = get_friends_list(request)
    print(context)
    """
    - Logic here is kind of tricky
        is_self
        is_friend
            -1: NO_REQUEST_SENT
            0: THEM_SENT_TO_YOU
            1: YOU_SENT_TO_THEM
    """
    if request.POST:
        print(request.POST)
        if 'status' in request.POST:
            form = UpdateStatusForm(request.POST)
            form.save(int(request.POST['pk']))
            redirect("map:main-page")
        if 'username' in request.POST:
            form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                redirect("map:main-page")
            else:
                context['error'] = "username not valid or already in use."

    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return None
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.image_url
        context['hide_email'] = account.hide_email
        context['status'] = account.status
        

        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends
    
        # Define template variables
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value # range: ENUM -> friend/friend_request_status.FriendRequestStatus
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
                if get_friend_request_or_false(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
                # CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                # CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "login/account_view.html", context)


def hoosaroundme(request, *args, **kwargs):
    cur_user = request.user
    context={}
    if (not cur_user.is_authenticated):
        context['not_loggedin'] = True
        return render(request, 'login/main_page_noupdate.html', context)
    # do some processing to show list of friends online:
    users_online = getAllUsersOnline()
    #print(users_online)
    nearby_count = 0
    for u in users_online:
        #print(u.username,u.homeLongitude,u.homeLatitude)
        currLat = float(u.homeLongitude)
        if(currLat != 0 ):
            nearby_count=nearby_count+1
    #User_list = User.objects.all()
    context['all_nearby_users'] = users_online
    context = get_friends_list(request, *args, **kwargs)
    friend_list = context['users_list']
    friend_rec = []
    count = 0
    user_size = len(users_online)
    friend_list_size = len(friend_list)
    while count < min(user_size - friend_list_size, 3):
        user = users_online[int(random.random()*user_size)]
        if (user not in friend_list) and (user.pk != cur_user.pk) and (user not in friend_rec):
            friend_rec.append(user)
            count = count + 1
    context['friend_rec'] = friend_rec
    context['all_nearby_users'] = users_online
    context['nearby_count'] = nearby_count
    print("CONTEXT:",context)
    return render(request, 'login/hoosaroundme.html', context)


def getAllUsersOnline():
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)
    # models: django.contrib.auth.models.User
    # models: allauth.account.models.EmailAddress
    # models: login.models.User

    User_list = Account.objects.all()

    return User_list


# def account_view(request, *args, **kwargs):
#     context = {}
#     user_id = kwargs.get("userId")


def get_friends_list(request, *args, **kwargs):
    context = {}
    user = request.user
    if not user.is_authenticated:
        context['info'] = "User not logged in."
        return context
    if user.is_authenticated:
        if args:
            user_id = args[0]
        elif kwargs:
            user_id = kwargs.get("user_id")
        else:
            user_id = user.pk
        print("in get_friends_list: user_id =  " + str(user_id))
        if user_id:
            try:
                this_user = Account.objects.get(pk=user_id)
                context['this_user'] = this_user
            except Account.DoesNotExist:
                context['info'] = "User does not exist."
                return context
            try:
                friend_list = FriendList.objects.get(user=this_user)
            except FriendList.DoesNotExist:
                context['info'] = "Could not find a friends list for {this_user.username}"
                return context
            friends = []  
            # get the authenticated users friend list
            auth_user_friend_list = FriendList.objects.get(user=this_user)
            for friend in friend_list.friends.all():
                friends.append(friend)
            context['users_list'] = friends
    else:
        context['info'] = "You must be friends to view their friends list."
        return context
        context['people_within_radius'] = personradius(myLat, myLong)
    return context



def main_page(request, *args, **kwargs):
    print(kwargs)
    context = {}
    user = request.user
    if request.POST:
        print(request.POST)
        form = UpdateLocationForm(request.POST)
        try:
            int(request.POST['pk'])
        except:
            return render(request, "login/main_page_noupdate.html", context)
        form.save(int(request.POST['pk']))
        context = get_friends_list(request, *args, **kwargs)
        if 'register' in kwargs.keys():
            context['register'] = 'True'
        print(context)
        return render(request, "login/main_page_noupdate.html", context)

    context = get_friends_list(request, *args, **kwargs)
    if 'register' in kwargs.keys():
        context['register'] = 'True'
    print(context)
    return render(request, "login/main_page.html", context)


def friend_requests(request, *args, **kwargs):
    context = get_friends_list(request, *args, **kwargs)
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        account = Account.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(
                receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You can't view another users friend requets.")
    else:
        redirect("main-page")
    return render(request, "login/friend_requests.html", context)


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            kwargs = {'register': True}
            args = []
            return main_page(request, *args, **kwargs)
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'login/register.html', context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return friends_list_view(request, args, {'user_id': user.pk})

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if destination:
                    return redirect(destination)
                return main_page(request, user.pk)

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "login/login-account.html", context)


def send_friend_request(request, *args, **kwargs):
    print("in views")
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                # Get any friend requests (active and not-active)
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver)
                # find if any of them are active (pending)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception(
                                "You already sent them a friend request.")
                    # If none are active create a new friend request
                    friend_request = FriendRequest(
                        sender=user, receiver=receiver)
                    friend_request.save()
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    print(str(e))
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                # There are no friend requests so create one.
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent."
        else:
            payload['response'] = "Unable to sent a friend request."
    else:
        payload['response'] = "You must be authenticated to send a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            print(friend_request)
            # confirm that is the correct request
            print(friend_request.receiver)
            print(user)
            if friend_request.receiver == user:
                if friend_request:
                    # found the request. Now accept it
                    updated_notification = friend_request.accept()
                    payload['response'] = "Friend request accepted."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to accept a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = Account.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something went wrong: {str(e)}"
        else:
            payload['response'] = "There was an error. Unable to remove that friend."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to remove a friend."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # confirm that is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    # found the request. Now decline it
                    payload['response'] = "Friend request declined."
                    friend_request.is_active = False
                    friend_request.save()
            else:
                payload['response'] = "That is not your friend request to decline."
        else:
            payload['response'] = "Unable to decline that friend request."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to decline a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(
                    sender=user, receiver=receiver, is_active=True)
            except FriendRequest.DoesNotExist:
                payload['response'] = "Nothing to cancel. Friend request does not exist."

            # There should only ever be ONE active friend request at any given time. Cancel them all just in case.
            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cance()
                payload['response'] = "Friend request canceled."
            else:
                # found the request. Now cancel it
                friend_requests.first().cancel()
                payload['response'] = "Friend request canceled."
        else:
            payload['response'] = "Unable to cancel that friend request."
    else:
        # should never happen
        payload['response'] = "You must be authenticated to cancel a friend request."
    return HttpResponse(json.dumps(payload), content_type="application/json")


def personradius():
    for x in range(0, 10):
        currentuser = Account.objects.get(pk=user_id)

        lat = currentuser.savedLocations.split(',')[1]
        lng = currentuser.savedLocations.split(',')[2]
    point = Point(lng, lat)
    Place.objects.filter(location__distance_lt=(point, Distance(km=radius)))
