import asyncio
from asgiref.sync import sync_to_async
from django.db.models import Prefetch
from django.db.models import Count
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .models import Thread, Message
from .serializers import MessageSerializer, ThreadSerializer, ThredsFilterSerializer, MarkReadSerializer


class CreateThread(ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    http_method_names = ['post', 'delete']
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.POST
        try:
            thread_name = data['name']
        except KeyError:
            raise ValidationError(['Key not found'])

        try:
            thread_room = Thread.objects.get(name=thread_name)
        except Exception as ex_error:
            new_thread = Thread.objects.create(name=thread_name)
            new_thread.participants.add(request.user)
            return Response(status=status.HTTP_200_OK, data=ThreadSerializer(new_thread).data)

        if thread_room.participants.count() < 2:
            thread_room.participants.add(request.user)
            return Response(status=status.HTTP_200_OK, data=ThreadSerializer(thread_room).data)
        else:
            raise ValidationError(['Thread is full'])


    @action(detail=True, methods=['delete'])
    def delete(self, request, *args, **kwargs):
        try:
            data = request.POST['name']
        except KeyError:
            raise ValidationError(['Key not found'])
        try:
            my_threads = Thread.objects.get(name=data)
            my_threads.participants.remove(request.user)
            if my_threads.participants.count() == 0:
                my_threads.delete()
                return Response(status=status.HTTP_200_OK, data={'response': f'Participants: {data}, was delete'})
            else:
                return Response(status=status.HTTP_200_OK, data={'response': f'You logout from {data}.'})
        except Exception as ex_error:
            raise ValidationError([f'{ex_error}. Object not found'])


class ThredsListByUser(ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThredsFilterSerializer
    http_method_names = ['get',]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants',]


class CreateReadMessage(ModelViewSet):
    queryset = Message.objects.all().prefetch_related('sender')
    serializer_class = MessageSerializer
    http_method_names = ['get', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['thread', ]
    permission_classes = [permissions.IsAuthenticated]

    def _create_message_(self, obj, sender):
        if 'text' in obj and 'thread' in obj:
            Message.objects.create(
                thread=Thread.objects.get(id=obj['thread']),
                sender=sender,
                text=obj['text']
            )

    def create(self, request, *args, **kwargs):
        data = request.POST
        if type(data) == list:
            for i in data:
                self._create_message_(i, request.user)
        elif type(data) == dict:
            self._create_message_(data, request.user)
        else:
            raise ValidationError(['No valid format data'])


class MarkReadMassages(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return a list of the not readed messages.
        """
        my_messages = [{'id': mess.id, 'text': mess.text} for mess in Message.objects.filter(sender=request.user, is_read=False)] #filter(sender=self.request.user)
        not_readed = len(my_messages)
        return Response({'not readed': not_readed,'messages': my_messages})

    def _change_status_(self, message_id):
        msg_to_update = Message.objects.get(id=message_id)
        msg_to_update.is_read = True
        msg_to_update.save()

    def _get_id_(self, data):
        if type(data) == list:
            for i in data:
                self._change_status_(i)
        elif type(data) == str or type(data) == int:
            self._change_status_(data)
        else:
            raise ValidationError([f'I dont know what is {type(data)}'])

    def _data_format_id_arrey_(self, data):
        if 'id' in data:
            self._get_id_(data['id'])
        else:
            raise ValidationError(['Request dont have key ID'])

    def put(self, request, *args, **kwargs):
        self._data_format_id_arrey_(request.data)
        return Response(status=status.HTTP_200_OK, data={'response': f'All message`s marked as read.'})

