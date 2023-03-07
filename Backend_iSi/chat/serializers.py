from rest_framework import serializers
from .models import Thread, Message


class _OnlyOneMessageSerializer_(serializers.ListSerializer):
    def to_representation(self, data):
        last_message = data.all().last()
        if last_message:
            data = [last_message]
        return super(_OnlyOneMessageSerializer_, self).to_representation(data)

class _OneMessageSerializer_(serializers.ModelSerializer):
    class Meta:
        model = Message
        list_serializer_class = _OnlyOneMessageSerializer_
        fields = '__all__'
        read_only_fields = ['created',]

class ThredsFilterSerializer(serializers.ModelSerializer):
    chanel = _OneMessageSerializer_(source='thread_set', many=True)
    class Meta:
        model = Thread
        fields = ['id', 'name', 'participants', 'created', 'updated', 'chanel']
        read_only_fields = ['created', 'updated',]

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ['participants', 'created', 'updated']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "text", "created", "is_read", "thread", "sender"]
        read_only_fields = ['sender',]

class MarkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "text", "created", "is_read", "thread", "sender"]
