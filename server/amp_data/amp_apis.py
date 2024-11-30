from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest
import json

from server.helpers import get_weeks_in_past_six_months
from server.models import AmpRecord


class AmpRecordListCreateView(View):

    def get(self, request):
        # Fetch all AmpRecord objects
        weeks = get_weeks_in_past_six_months()
        records = AmpRecord.objects.filter(date__in=weeks)

        # Manually convert each record to a dictionary (this could be optimized if needed)
        data = [
            {
                f"{record.date}": {
                    'name': record.name,
                    'note_first_contentful_paint': record.note_first_contentful_paint,
                    'note_total_blocking_time': record.note_total_blocking_time,
                    'note_speed_index': record.note_speed_index,
                    'note_largest_contentful_paint': record.note_largest_contentful_paint,
                    'note_cumulative_layout_shift': record.note_cumulative_layout_shift,
                    'video_first_contentful_paint': record.video_first_contentful_paint,
                    'video_total_blocking_time': record.video_total_blocking_time,
                    'video_speed_index': record.video_speed_index,
                    'video_largest_contentful_paint': record.video_largest_contentful_paint,
                    'video_cumulative_layout_shift': record.video_cumulative_layout_shift,
                }
            }
            for record in records
        ]

        return JsonResponse(data, safe=False)