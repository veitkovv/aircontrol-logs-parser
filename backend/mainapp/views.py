from rest_framework.views import APIView, Response
from django.conf import settings

from .utils import scan_logs, start_roll_fabric


class ScanLogsView(APIView):
    def post(self, request, *args, **kwargs):
        my_result = scan_logs(settings.LOGS_PATH)  # Скан файловой системы
        start_roll_fabric(my_result)
        return Response(data={"status": "done"})
