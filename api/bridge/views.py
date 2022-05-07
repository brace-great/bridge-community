from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User, Group, AnonymousUser
from .models import *
from rest_framework.permissions import *
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework.decorators import action
from .serializers import *
from .permissions import *
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import requests
from django.http import HttpResponse
from django.db import connection, transaction
import django.utils.timezone as timezone

# @api_view(['GET'])  # XXX
# def api_root(request, format=None):
#     return Response({
#         'users': reverse('user-list', request=request, format=format),
#     })


# class DiscussWithTagView(viewsets.ModelViewSet):
#     queryset = DiscussWithTag.objects.all()
#     serializer_class = DiscussWithTagSerializer
#     permission_classes = [AllowAny]

#     def get_queryset(self):
#         """
#         This view should return a list of all the purchases
#         for the currently authenticated user.
#         """
#         keyword = self.request.data.keyword
#         return DiscussWithTag.objects.filter(tag=keyword) | DiscussWithTag.objects.filter(title_contains=keyword)
class DiscussWithTagView(generics.GenericAPIView):

    def put(self, request, *args, **kwargs):

        if(len(request.data) == 1):
            payload = {
                'keyword': request.data['keyword'],
                'keyword2': '%'+request.data['keyword']+'%'

            }
            with connection.cursor() as cursor:
                rs = DiscussWithTag.objects.raw(
                    "select * from bridge_discusstag WHERE tag = %(keyword)s OR title like %(keyword2)s;", payload)
                # rs = DiscussWithTag.objects.raw(
                #     "select * from discuss_with_tag WHERE tag = %(keyword)s OR title like %(keyword2)s;", payload)
                serializer = DiscussWithTagSerializer(rs, many=True)
                rs = Comment.objects.raw(
                    "select * from bridge_comment WHERE discuss_id in (select id from discuss_with_tag WHERE tag = %(keyword)s OR title like %(keyword2)s);", payload)
                serializer2 = CommentSerializer(rs, many=True)
                return Response({'discuss': serializer.data, 'comments': serializer2.data})

        return super().put(request, *args, **kwargs)


class ChangeEmail(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        payload = {'email': request.data['email'],
                   'username': request.data['username']}
        with connection.cursor() as cursor:

            cursor.execute(
                "UPDATE auth_user SET is_active = 0,email = %(email)s WHERE username = %(username)s;", payload)

        url = "http://localhost:8000/api/auth/users/resend_activation/"  # TODO部署时需要修改
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return HttpResponse("验证邮件已发送到您的新邮箱，请查收", status=status.HTTP_200_OK)
        else:
            return Response(response.json())


class ActivateUser(generics.GenericAPIView):

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8000/api/auth/users/activation/"  # TODO
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return HttpResponse("验证成功")
        else:
            return Response(response.json())


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return ChatMessage.objects.filter(sender=user) | ChatMessage.objects.filter(receiver=user)

    def put(self, request, *args, **kwargs):

        if(len(request.data) == 1 and request.data['sender'] != request.user.username):
            payload = {
                'username': request.user.username,
                'sender': request.data['sender']
            }
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE bridge_chatmessage SET isread_receiver = 1 WHERE receiver = %(username)s AND sender = %(sender)s;", payload)
                return HttpResponse(status=status.HTTP_200_OK)
        if(request.user.username != request.data['sender']):
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return super().put(request, *args, **kwargs)


class NotifyViewSet(viewsets.ModelViewSet):
    queryset = Notify.objects.all()
    serializer_class = NotifySerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Notify.objects.filter(username=user)

    def put(self, request, *args, **kwargs):

        if(len(request.data) == 1 and request.data['username'] == request.user.username):
            payload = {
                'username': request.user.username,
            }
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE bridge_notify SET isread = 1 WHERE username = %(username)s;", payload)
                return HttpResponse(status=status.HTTP_200_OK)
        if(request.user.username != request.data['username']):
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)

        return super().put(request, *args, **kwargs)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        # print(request)
        # payload = {"content_id": request.data['title']}
        # with connection.cursor() as cursor:
        #     rs = Discuss.objects.raw(
        #         "select * from bridge_discuss WHERE content_id = %(content_id)s;", payload)
        # print(rs)
        # return Response(status=status.HTTP_200_OK)
        return super().destroy(request, *args, **kwargs)


class DynamicViewSet(generics.GenericAPIView):
    queryset = Dynamic.objects.all()
    serializer_class = DynamicSerializer
    permission_classes = [AllowAny]

    def get(self, request, username, format=None):
        return Response({"data": self.queryset.filter(username=username).values()}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(notshow=False)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CommentSerializerAlter
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.serializer_class = CommentSerializer
        res = Discuss.objects.raw(
            'SELECT * FROM bridge_discuss WHERE id = %(discuss)s', serializer.data)
        payload = {
            'username': serializer.data['commenter'], 'time': timezone.now(), 'title': res[0].title, 'comment': serializer.data['id']}
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bridge_dynamic SET discuss = %(title)s,username = %(username)s,time=%(time)s,comment=%(comment)s;", payload)
        if(serializer.data['replyto'] == None):
            res = Discuss.objects.raw(
                'SELECT * FROM bridge_discuss WHERE id = %(discuss)s', serializer.data)
            payload = {
                'from_who': serializer.data['commenter'], 'time': timezone.now(), 'username': res[0].starter, 'discuss_title': res[0].title}
            if(payload['from_who'] != payload['username']):
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO bridge_notify SET discuss_title=%(discuss_title)s, from_who = %(from_who)s,username = %(username)s,time=%(time)s,event_type=1,isread=0;", payload)
        else:
            res = Comment.objects.raw(
                'SELECT * FROM bridge_comment WHERE id = %(replyto)s', serializer.data)
            res2 = Discuss.objects.raw(
                'SELECT * FROM bridge_discuss WHERE id = %(discuss)s', serializer.data)
            payload = {
                'from_who': serializer.data['commenter'], 'time': timezone.now(), 'username': res[0].commenter, 'discuss_title': res2[0].title}
            if(payload['from_who'] != payload['username']):
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO bridge_notify SET discuss_title=%(discuss_title)s, from_who = %(from_who)s,username = %(username)s,time=%(time)s,event_type=2,isread=0;", payload)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DiscussViewSet(viewsets.ModelViewSet):
    queryset = Discuss.objects.all()
    serializer_class = DiscussSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Discuss.objects.filter(isshow=True)

    def create(self, request, *args, **kwargs):
        request1 = request.data.dict()
        _mutable = request.data._mutable
        # set to mutable
        request.data._mutable = True
        # сhange the values you want
        request.data['isshow'] = True
        # print(request.data)
        # set mutable flag back
        request.data._mutable = _mutable
        tags = []
        for key, val in request1.items():
            if(key[0:4] == 'tags'):
                tags.append(val)

        res = super().create(request, *args, **kwargs)
        payload = {"title": res.data['title'], "tag": "",
                   "username": res.data['starter'], "time": timezone.now(), "id": res.data['id']}
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO bridge_dynamic SET discuss = %(title)s,username = %(username)s,time=%(time)s;", payload)
        for i in tags:
            payload['tag'] = i
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO bridge_discusstag SET tag = %(tag)s,discuss_id = %(id)s;", payload)
        return res


class UserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'username'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
    lookup_field = 'username'

    def partial_update(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        response_with_updated_instance = super(
            UserViewSet, self).partial_update(request, *args, **kwargs)
        return response_with_updated_instance

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     print(request.data)
    #     user = get_object_or_404(queryset, username=request.data.username)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         serializer.is_valid(raise_exception=True)
    #     except:
    #         return Response(serializer.data)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_queryset(self):
    #     user = self.request.user
    #     if(type(user) == AnonymousUser or user.is_superuser == 1):
    #         return User.objects.all()
    #     else:
    #         return User.objects.filter(username=user)

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     return Response({'status': 'password set'})
    # else:
    #     return Response(serializer.errors,
    #                     status=status.HTTP_400_BAD_REQUEST)

    # def get_permissions(self):
    #     if self.action == 'destroy':
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ReadOnlyModelViewSet):  # XXX
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
