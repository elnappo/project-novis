import json
import logging

from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseServerError

logger = logging.getLogger("healthz")


# Based on https://www.ianlewis.org/en/kubernetes-health-checks-django
class HealthCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            if request.path == "/readiness":
                return self.readiness(request)
            elif request.path == "/healthz":
                return self.healthz(request)
        return self.get_response(request)

    @staticmethod
    def healthz(request: HttpRequest) -> HttpResponse:
        """
        Returns that the server is alive.
        """
        return HttpResponse(json.dumps({
            "hostname": settings.HOSTNAME,
            "status": "application is healthy"
        }), content_type="application/json")

    @staticmethod
    def readiness(request: HttpRequest) -> HttpResponse:
        """
        Returns that the server is ready to serve requests.
        """

        # Connect to each database and do a generic standard SQL query
        # that doesn't write any data and doesn't depend on any tables
        # being present.
        try:
            from django.db import connections
            for name in connections:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return HttpResponseServerError(json.dumps({
                        "hostname": settings.HOSTNAME,
                        "status": "db: invalid response"
                    }), content_type="application/json")
        except Exception as e:
            logger.exception(e)
            return HttpResponseServerError(json.dumps({
                "hostname": settings.HOSTNAME,
                "status": "db: can not connect to database"
            }), content_type="application/json")

        return HttpResponse(json.dumps({
            "hostname": settings.HOSTNAME,
            "status": "application is ready"
        }), content_type="application/json")
