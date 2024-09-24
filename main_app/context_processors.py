from .models import Profile
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

def background(request):
    is_authenticated = request.user.is_authenticated
    context = {}
    logger.debug(f"User: {request.user}")
    if is_authenticated:
        try:
            background = Profile.objects.get(user=request.user).background
            context = {'background': background}
        except ObjectDoesNotExist:
            logger.warning(f"No Profile found for user: {request.user}")
    return context