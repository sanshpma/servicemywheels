from django.conf import settings

def make_session_available(request):

    if request.session.session_key == None:
        request.session.save()
    return {'SERVICEMYWHEELS_SESSION_KEY_IDENTIFIER': request.session.session_key}