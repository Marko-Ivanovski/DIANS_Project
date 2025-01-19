import pandas as pd

from rest_framework import generics
from rest_framework.views import APIView
from ..models import Share, Firm
from ..serializer import ShareSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator
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
            date__range=(from_date_obj, to_date_obj),
            # quantity_of_shares__gt = 0
        ).order_by('date')

        if not shares.exists():
            raise ValidationError({"no_data": "No shares found for the given parameters."})

        # Serialize and return the response
        serializer = ShareSerializer(shares, many=True)
        return Response(serializer.data)

class TechnicalAnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        firm_id = request.query_params.get('firm_id')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        # Validate query parameters
        if not firm_id or not from_date or not to_date:
            raise ValidationError("Please provide firm_id, from_date, and to_date.")

        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Invalid date format. Use YYYY-MM-DD.")

        # Fetch historical share data
        shares = Share.objects.filter(
            firm__firm_id=firm_id,
            date__range=(from_date_obj, to_date_obj),
            # quantity_of_shares__gt=0
        ).order_by('date')

        if not shares.exists():
            raise ValidationError("No share data found for the given parameters.")

        # Convert to DataFrame
        data = pd.DataFrame(list(shares.values("date", "price_of_last_transaction")))
        data['date'] = pd.to_datetime(data['date'])
        data = data.sort_values('date').reset_index(drop=True)

        # Add technical indicators
        # Safe handling of SMA, EMA, and RSI calculation
        data['SMA_10'] = SMAIndicator(data['price_of_last_transaction'], window=10).sma_indicator()
        data['EMA_10'] = EMAIndicator(data['price_of_last_transaction'], window=10).ema_indicator()

        # Calculate RSI
        rsi_indicator = RSIIndicator(data['price_of_last_transaction'], window=14)
        rsi_values = rsi_indicator.rsi()

        # Prevent division by zero or NaN in RSI calculations
        data['RSI'] = rsi_values
        data['signal'] = data['RSI'].apply(lambda x: 'BUY' if x < 30 else 'SELL' if x > 70 else 'HOLD')

        # Handle division by zero cases for the technical analysis
        data['SMA_10'] = data['SMA_10'].fillna(0)
        data['EMA_10'] = data['EMA_10'].fillna(0)

        # Ensure no zero values in RSI to avoid errors
        data['RSI'] = data['RSI'].apply(lambda x: 0 if pd.isna(x) else x)

        # Filter out rows where SMA_10, EMA_10, or RSI are 0
        data = data[(data['SMA_10'] != 0) & (data['EMA_10'] != 0) & (data['RSI'] != 0)]

        # Prepare the response with additional data
        response_data = data[['date', 'price_of_last_transaction', 'SMA_10', 'EMA_10', 'RSI', 'signal']].to_dict('records')

        # Return the data as a response
        return Response(response_data)