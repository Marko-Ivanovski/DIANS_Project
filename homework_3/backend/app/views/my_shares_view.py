from datetime import date

from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from ..models import MyShares, Share
from ..serializer import MySharesSerializer, ShareSerializer

class MyStocksView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        transaction_type = request.query_params.get('transaction_type')
        user = request.user

        if transaction_type not in ['BUY', 'SELL']:
            return Response({"error": "Invalid transaction type."}, status=400)

        if transaction_type == 'BUY':
            max_date = Share.objects.aggregate(max_date=Max('date'))['max_date']
            shares = Share.objects.filter(quantity_of_shares__gt=0, date=max_date)
            serializer = ShareSerializer(shares, many=True)
            return Response(serializer.data)

        elif transaction_type == 'SELL':
            my_shares = MyShares.objects.filter(user=user)
            serializer = MySharesSerializer(my_shares, many=True)
            return Response(serializer.data)

    @transaction.atomic
    def post(self, request):
        print(request.data)
        user = request.user
        share_id = request.data.get('share_id')
        quantity = int(request.data.get('quantity', 0))
        transaction_type = request.data.get('transaction_type')

        if not share_id or quantity <= 0:
            return Response({"error": "Invalid share ID or quantity."}, status=400)

        if transaction_type == 'BUY':
            try:
                # Lock the share row for the transaction
                share = Share.objects.select_for_update().get(id=share_id)

                if share.quantity_of_shares < quantity:
                    return Response({"error": "Insufficient shares available."}, status=400)

                total_cost = quantity * share.price_of_last_transaction
                user_balance = user.current_balance

                # Check if user has enough balance to buy the shares
                if user_balance < total_cost:
                    return Response({"error": "Insufficient balance to purchase shares."}, status=400)

                # Update or create an entry in MyShares
                my_share, created = MyShares.objects.get_or_create(
                    user=user,
                    share=share,
                    firm=share.firm,
                    defaults={
                        'quantity': 0,
                        'price_of_last_transaction': share.price_of_last_transaction,
                        'purchase_date': share.date,
                    }
                )
                my_share.quantity += quantity
                my_share.price_of_last_transaction = share.price_of_last_transaction
                my_share.purchase_date = share.date
                my_share.save()

                # Update the Shares table
                share.quantity_of_shares -= quantity
                share.save()

                user.current_balance -= total_cost
                user.save()

                return Response({
                    "message": "Successfully bought shares.",
                    "updated_share": ShareSerializer(share).data,
                    "my_share": MySharesSerializer(my_share).data,
                    "updated_balance": str(user.current_balance),
                })
            except Share.DoesNotExist:
                return Response({"error": "Share not found."}, status=404)

        elif transaction_type == 'SELL':
            try:
                # Lock the MyShares row for the transaction
                my_share = MyShares.objects.select_for_update().get(user=user, id=share_id)

                if my_share.quantity < quantity:
                    return Response({"error": "Insufficient shares to sell."}, status=400)

                total_proceeds = quantity * my_share.price_of_last_transaction

                # Update or delete the entry in MyShares
                my_share.quantity -= quantity
                my_share.save()

                if my_share.quantity == 0:
                    my_share.delete()

                # Update or create an entry in the Shares table
                share, created = Share.objects.get_or_create(
                    id=my_share.share.id,
                    defaults={
                        'quantity_of_shares': 0,
                        'price_of_last_transaction': my_share.price_of_last_transaction,
                        'date': my_share.purchase_date,
                    }
                )
                share.quantity_of_shares += quantity
                share.price_of_last_transaction = my_share.price_of_last_transaction
                share.save()

                user.current_balance += total_proceeds
                user.save()

                sell_date = date.today()

                return Response({
                    "message": "Successfully sold shares.",
                    "updated_my_share": MySharesSerializer(my_share).data if my_share.quantity > 0 else None,
                    "available_share": ShareSerializer(share).data,
                    "sell_date": sell_date,
                    "updated_balance": str(user.current_balance),
                })
            except MyShares.DoesNotExist:
                return Response({"error": "Share not found in MyShares."}, status=404)

        return Response({"error": "Invalid transaction type."}, status=400)
