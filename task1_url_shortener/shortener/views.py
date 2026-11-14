import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import ShortURL
from .utils import generate_code


def go_to_url(request, code):
    link = get_object_or_404(ShortURL, short_code=code)
    return redirect(link.original_url)


@csrf_exempt
def shorten_url(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    original_url = data.get("url")
    if not original_url:
        return JsonResponse({"error": "url is required"}, status=400)

    code = generate_code()
    while ShortURL.objects.filter(short_code=code).exists():
        code = generate_code()

    link = ShortURL.objects.create(original_url=original_url, short_code=code)
    short_url = request.build_absolute_uri(f"/{link.short_code}/")
    return JsonResponse({"short_code": link.short_code, "short_url": short_url}, status=201)