from rest_framework import serializers
import citymngmt.models as cityModels

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = cityModels.City
        fields = '__all__'

class BusStopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityModels.BusStops
        fields = '__all__'

class CompanyRelationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityModels.CompanyRelations
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = cityModels.Company
        fields = '__all__'

class LinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = cityModels.Line
        fields = '__all__'