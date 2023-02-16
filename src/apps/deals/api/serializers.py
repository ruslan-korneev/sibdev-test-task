import csv

from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from src.apps.deals.models import Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = "__all__"


class DealCreateListSerializer(serializers.Serializer):
    deals = serializers.FileField(
        write_only=True,
        validators=[FileExtensionValidator(allowed_extensions=("csv",))],
    )
    username = serializers.CharField(source="customer", read_only=True)
    spent_money = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    gems = serializers.ListField(child=serializers.CharField(), read_only=True)

    def save(self):
        file = self.validated_data["deals"].read().decode("utf-8")
        deals = [
            dict(
                customer=row[0],
                item=row[1],
                total=row[2],
                quantity=row[3],
                date=row[4],
            )
            for row in list(csv.reader(file.splitlines(), delimiter=","))[1:]
        ]

        serializer = DealSerializer(data=deals, many=True)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError(
                [
                    {**detail, "line": line}
                    for line, detail in enumerate(exc.detail, start=2)
                    if detail
                ],
            )

        Deal.objects.all().delete()
        serializer.save()
