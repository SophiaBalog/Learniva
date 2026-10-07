from .permissions import is_teacher

def user_role(request):
    return {'is_teacher': is_teacher(request.user)}