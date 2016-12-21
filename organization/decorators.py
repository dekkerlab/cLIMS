'''
Created on Dec 5, 2016

@author: nanda
'''
from django.contrib.auth import get_user
from cLIMS import settings
from django.shortcuts import redirect
from django.views.generic.base import View
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

def require_permission(view):
    
    def new_view(request, *args, **kwargs):
        user = get_user(request)
        ownerID = request.session['project_ownerId']
        if (user.id == ownerID):
            return view(request, *args, **kwargs)
        else:
            url = '{}?next={}'.format(
                settings.LOGIN_URL,
                request.path)
            return redirect(url)
    return new_view


def class_login_required(cls):
    if (not isinstance(cls, type) or not issubclass(cls, View)):
        raise ImproperlyConfigured("class_login_required must be applied to subclass of View class.")
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls