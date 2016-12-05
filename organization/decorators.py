'''
Created on Dec 5, 2016

@author: nanda
'''
from django.contrib.auth import get_user
from cLIMS import settings
from django.shortcuts import redirect

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

            