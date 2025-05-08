import traceback
from django.http import JsonResponse

class ShowErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)
        return response