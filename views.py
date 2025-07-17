from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', block=True)
def test_view(request):
    return JsonResponse({'message': 'This is a rate-limited view'})
