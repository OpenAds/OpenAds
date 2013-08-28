from django.conf import settings


def color_processor(request):
    return {"body_back": settings.BACKGROUND_COLOR}