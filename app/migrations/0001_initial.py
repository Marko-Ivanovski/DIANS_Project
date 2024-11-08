# Generated by Django 4.1 on 2024-11-07 00:16

from django.db import migrations, models
import django.db.models.deletion


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
                ("name", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "firms",
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
                    "firm_id",
                    models.ForeignKey(
                        db_column="firm_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.firm",
                        to_field="firm_id",
                    ),
                ),
            ],
            options={
                "db_table": "shares",
            },
        ),
    ]
