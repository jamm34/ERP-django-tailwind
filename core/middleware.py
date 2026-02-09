from django.conf import settings
from django.shortcuts import render


class Custom404Middleware:
    """Muestra una página 404 amigable incluso con DEBUG=True.

    Django, por defecto, cuando DEBUG=True muestra el 404 técnico.
    Con este middleware, si una respuesta termina en 404 y el cliente espera HTML,
    devolvemos la plantilla `404.html`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code != 404:
            return response

        # Evitar capturar assets (estáticos / favicon)
        path = (request.path_info or "").lstrip("/")
        static_prefix = (getattr(settings, "STATIC_URL", "static/") or "static/").lstrip("/")
        if path.startswith(static_prefix) or path == "favicon.ico":
            return response

        # Solo para navegadores / peticiones HTML
        accept = request.headers.get("Accept", "")
        if accept and ("text/html" not in accept and "*/*" not in accept):
            return response

        # Importante: devolver un HttpResponse ya renderizado para que otros
        # middlewares (ej. CommonMiddleware) puedan acceder a response.content.
        return render(request, "404.html", status=404)
