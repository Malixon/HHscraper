from rest_framework import serializers

class SkillStatsSerializer(serializers.Serializer):
    name = serializers.CharField()
    mention_count = serializers.IntegerField()