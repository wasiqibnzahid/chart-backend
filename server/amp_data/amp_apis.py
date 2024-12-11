from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from server.models import AmpRecord


class AmpPerformanceReportView(View):

    def get(self, request):
        records = AmpRecord.objects.all().exclude(
                Q(note_first_contentful_paint=0) &
                Q(note_total_blocking_time=0) &
                Q(note_speed_index=0) &
                Q(note_largest_contentful_paint=0) &
                Q(note_cumulative_layout_shift=0) &
                Q(video_first_contentful_paint=0) &
                Q(video_total_blocking_time=0) &
                Q(video_speed_index=0) &
                Q(video_largest_contentful_paint=0) &
                Q(video_cumulative_layout_shift=0)
            ).values(
            'id', 'name', 'note_first_contentful_paint', 'note_total_blocking_time',
            'note_speed_index', 'note_largest_contentful_paint', 'note_cumulative_layout_shift',
            'video_first_contentful_paint', 'video_total_blocking_time', 'video_speed_index',
            'video_largest_contentful_paint', 'video_cumulative_layout_shift',
            'date'
        )
        # records = AmpRecord.objects.all()
        # mode = request.GET.get("mode", "week")
        # if(mode == "week"):
        #     date_filters = get_weeks_in_past_six_months()
        # elif(mode == "month"):
        #     date_filters = get_previous_months_of_current_year()

        # Manually convert each record to a dictionary (this could be optimized if needed)
        # data = {}
        # for record in records:
        #     values = {
        #         'name': record.name,
        #         'note_first_contentful_paint': record.note_first_contentful_paint,
        #         'note_total_blocking_time': record.note_total_blocking_time,
        #         'note_speed_index': record.note_speed_index,
        #         'note_largest_contentful_paint': record.note_largest_contentful_paint,
        #         'note_cumulative_layout_shift': record.note_cumulative_layout_shift,
        #         'video_first_contentful_paint': record.video_first_contentful_paint,
        #         'video_total_blocking_time': record.video_total_blocking_time,
        #         'video_speed_index': record.video_speed_index,
        #         'video_largest_contentful_paint': record.video_largest_contentful_paint,
        #         'video_cumulative_layout_shift': record.video_cumulative_layout_shift,
        #         'total_first_contentful_paint': (record.video_first_contentful_paint + record.note_first_contentful_paint) / 2,
        #         'total_total_blocking_time': (record.video_total_blocking_time + record.note_total_blocking_time) / 2 ,
        #         'total_speed_index': (record.video_speed_index + record.note_speed_index) / 2,
        #         'total_largest_contentful_paint': (record.video_largest_contentful_paint + record.note_largest_contentful_paint) / 2,
        #         'total_cumulative_layout_shift': (record.video_cumulative_layout_shift + record.note_cumulative_layout_shift) / 2,
        #     }
            
        #     if mode == "week":
        #         date_key = f"{record.date}"
        #     elif mode == "month":
        #         date_key = f"{record.date.year}-{record.date.month:02d}"
        #     elif mode == "year":
        #         date_key = str(record.date.year)  # Use year as the key

        #     # Group by the selected date (week, month, or year)
        #     if date_key in data:
        #         # If the date already exists, append the values to the list for that date
        #         data[date_key].append(values)
        #     else:
        #         # If the date does not exist, create a new list with the current values
        #         data[date_key] = [values]

        return JsonResponse(list(records), safe=False)