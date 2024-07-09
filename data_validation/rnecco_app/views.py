from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome! User data validation to ensure its authenticity.")


