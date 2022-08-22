import json

from django.http import  JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):
    def get(self, request):
        all_ads = Ad.objects.all()

        res = []
        for ad in all_ads:
            res.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            })
        return JsonResponse(res, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(name=data["name"],
                                    author=data["author"],
                                    price=data["price"],
                                    description=data["description"],
                                    address=data["address"],
                                    is_published=data["is_published"]
                                    )
        return JsonResponse({
                "id": new_ad.id,
                "name": new_ad.name,
                "author": new_ad.author,
                "price": new_ad.price,
                "description": new_ad.description,
                "address": new_ad.address,
                "is_published": new_ad.is_published},
            safe=False,
            json_dumps_params={"ensure_ascii": False})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Exception:
            return JsonResponse({"error": "item not found"}, status=404)

        return JsonResponse({
                   "id": ad.id,
                   "name": ad.name,
                   "author": ad.author,
                   "price": ad.price,
                   "description": ad.description,
                   "address": ad.address,
                   "is_published": ad.is_published},
            safe=False,
            json_dumps_params={"ensure_ascii": False}
        )


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            cat = self.get_object()
        except Exception:
            return JsonResponse({"error": "item not found"}, status=404)

        return JsonResponse({
                    "id": cat.id,
                    "name": cat.name},
                safe=False,
                json_dumps_params={"ensure_ascii": False})


