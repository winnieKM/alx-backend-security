import time
from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit = 100  # max requests
        self.time_window = 60  # seconds

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')

        # Create cache key for this IP
        key = f"rl:{ip}"
        data = cache.get(key)

        current_time = time.time()

        if data:
            requests, first_request_time = data

            if current_time - first_request_time < self.time_window:
                if requests >= self.rate_limit:
                    return HttpResponseForbidden("Rate limit exceeded. Try again later.")
                else:
                    cache.set(key, (requests + 1, first_request_time), timeout=self.time_window)
            else:
                cache.set(key, (1, current_time), timeout=self.time_window)
        else:
            cache.set(key, (1, current_time), timeout=self.time_window)

        return self.get_response(request)
