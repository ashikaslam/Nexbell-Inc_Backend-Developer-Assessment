from rest_framework import serializers
from .models import Rating

# class RatingSerializer(serializers.ModelSerializer):
#     commentors_name = serializers.SerializerMethodField()
#     class Meta:
#         model = Rating
#         fields = ['rating', 'comment', 'is_edited', 'edit_date','commentors_name']  # Exclude user and phone (they'll be handled in the view)
#         read_only_fields = ['is_edited', 'edit_date','commentors_name']
    
#     def get_commentors_name(self, obj):
#         try:
#             return obj.user.name
#         except Exception as e:"null"