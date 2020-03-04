"""Serializers used throughout the data Rest API
"""

from rest_framework_mongoengine.serializers import DocumentSerializer
from django_mongoengine import fields
import core_json_app.components.data.api as data_api
from core_main_app.components.data.models import Data


class DataSerializer(DocumentSerializer):
    """ Data serializer
    """
    dict_content = fields.DictField(blank=True)

    class Meta(object):
        """ Meta
        """
        model = Data
        fields = ["id",
                  "template",
                  "user_id",
                  "title",
                  "dict_content",
                  "last_modification_date"]
        read_only_fields = ('id', 'user_id', 'last_modification_date', )

    def create(self, validated_data):
        """
        Create and return a new `Data` instance, given the validated data.
        """
        # Create data
        instance = Data(
            template=validated_data['template'],
            title=validated_data['title'],
            user_id=str(validated_data['user'].id),
        )
        # Set JSON content
        instance.dict_content = validated_data['dict_content']
        # Save the data
        data_api.upsert(instance, validated_data['user'])
        # Encode the response body
        instance.dict_content = validated_data['dict_content']

        return instance

    def update(self, instance, validated_data):
        """
        Update and return an existing `Data` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.dict_content = validated_data.get('dict_content', instance.dict_content)
        return data_api.upsert(instance, validated_data['user'])




