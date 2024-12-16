from rest_framework import generics
from rest_framework.views import APIView
from ..models import Share, Firm
from ..serializer import ShareSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta

class ShareView(generics.ListAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer

class ShareByFirmView(generics.ListAPIView):
    serializer_class = ShareSerializer

    def get_queryset(self):
        firm_id = self.kwargs['firm_id']
        return Share.objects.filter(firm__firm_id=firm_id)


class SharesFilteredView(APIView):
    def get(self, request, *args, **kwargs):
        firm_id = request.query_params.get('firm_id')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        # Validate query parameters
        if not firm_id:
            raise ValidationError({"firm_id": "This parameter is required."})

        if not Firm.objects.filter(firm_id=firm_id).exists():
            raise ValidationError({"firm_id": "The specified firm_id does not exist."})

        if not from_date or not to_date:
            raise ValidationError({"date_range": "Both from_date and to_date parameters are required."})

        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"date_range": "Invalid date format. Use YYYY-MM-DD."})

        # Ensure the range is within one year
        if to_date_obj - from_date_obj > timedelta(days=365):
            raise ValidationError({"date_range": "The date range must not exceed one year."})

        # Perform the filtering based on date range
        shares = Share.objects.filter(
            firm__firm_id=firm_id,
            date__range=(from_date_obj, to_date_obj)
        ).order_by('date')

        if not shares.exists():
            raise ValidationError({"no_data": "No shares found for the given parameters."})

        # Serialize and return the response
        serializer = ShareSerializer(shares, many=True)
        return Response(serializer.data)