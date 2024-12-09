# Generated by Django 5.1.3 on 2024-12-07 02:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Firm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("firm_id", models.CharField(max_length=10, unique=True)),
                ("name", models.CharField(blank=True, max_length=30)),
            ],
            options={
                "db_table": "firms",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=15)),
                ("last_name", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=30, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "current_balance",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
                ),
                ("password", models.CharField(max_length=8000)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Share",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "price_of_last_transaction",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "max_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "min_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "average_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "percent_changed",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                ("quantity_of_shares", models.IntegerField(default=0)),
                (
                    "total_profit",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "firm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shares",
                        to="app.firm",
                    ),
                ),
            ],
            options={
                "db_table": "shares",
            },
        ),
        migrations.CreateModel(
            name="TransactionShare",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_type",
                    models.CharField(
                        choices=[("BUY", "Buy"), ("SELL", "Sell")], max_length=4
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("transaction_date", models.DateTimeField(auto_now_add=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "firm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.firm"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_shares",
                        to="app.user",
                    ),
                ),
            ],
            options={
                "db_table": "transactions_shares",
            },
        ),
        migrations.CreateModel(
            name="TransactionLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_account_type",
                    models.CharField(
                        choices=[("DEPOSIT", "Deposit"), ("WITHDRAW", "Withdraw")],
                        max_length=20,
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transactions_logs",
                        to="app.user",
                    ),
                ),
            ],
            options={
                "db_table": "transactions_logs",
            },
        ),
    ]
