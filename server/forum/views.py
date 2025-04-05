from .paginations import Default
from .permissions import IsUserObjectOrAdminPermission
from .models import (
    Question,
    Answer,
    QuestionLike,
    AnswerLike
)


from .serailizers import (
    QuestionSerailizer,
    AnswerSerailizer,
    EmptySerializer,
    QuestionDetailSerailizer
)

from utils.response.response import CustomResponse as cr 


from rest_framework.decorators import action 
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404




#! ViewSet For Question  
class QuestionViewSet(ModelViewSet):
    queryset=(
        Question.objects
        .all()
        .select_related('user')
    ).order_by('-time_stamp')

    # ! Adding Filters Backend
    filter_backends=[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    filterset_fields=['semester']
    pagination_class=Default

    # ! Fields Used For Searching
    search_fields = ['title','description']

    #! Fields Used For Ordering
    ordering_fields=['time_stamp']


    # ! For Specfying Method For ViewSet
    http_method_names=[
        'get',
        'options',
        'head',
        'post',
        'delete'
    ]

    # ! Custom Permission Called
    permission_classes=[IsUserObjectOrAdminPermission]


    def list(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return cr.success(
            data=serializer.data
            )


    def retrieve(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        instance = self.get_object()
        serializer = QuestionDetailSerailizer(instance)
        return cr.success(
            data=serializer.data
            )


    def create(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return cr.success(
            status=HTTP_201_CREATED,
            message="You Have Successfuly Created New Post"
        )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Post Deleted Successfully"
            )
    

    def get_serializer_class(self):
        """
        Overriding the serailzer class for assigning Empty Serializer 
        the custom action name  like 
        """
        if self.action=='like':
            return EmptySerializer
        return QuestionSerailizer 


    def get_serializer_context(self):
        """
        For Passing User_id as serializer Context
        """
        user_id=self.request.user.id
        return {'user_id':user_id} 
    

    # ! Custom Like Action 
    @action(
            detail=True,
            methods=['GET','POST','DELETE'],
            permission_classes=[IsAuthenticated]
        )
    def like(self,request,pk):
        """
        Custom Actions For Liking And Removing Like 
        From  Specific Question
        """
        user_id=request.user.id

        if request.method=='GET':
            try:
                question_like=QuestionLike.objects.filter(
                    user_id=user_id,
                    question_id=pk 
                )

                if question_like.exists():
                    return cr.success(data={
                        'is_liked':True
                    })
                return cr.success(data={
                    'is_liked':False
                })
            
            except Exception as e:
                return cr.error(
                    message="Some Error Occured In GET Method",
                    status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        if request.method=='POST':
            try:
                # ! Create's a QuestionLike  Instance For The Question
                QuestionLike.objects.create(
                    user_id=user_id,
                    question_id=pk #! Used the question id received in the URL Parameter
                )
                
                # !Get the Question Instance  and Increase The Number Of Likes by One
                question=Question.objects.get(id=pk)
                question.is_liked=True
                question.likes+=1
                question.save()
                
                return cr.success(status=HTTP_201_CREATED)
            
        
            except Exception as e:
                # ! Just For handeling Expections
                print('Error alert: A user is trying to like same object multiple times ')
                return cr.error(
                    message="Already Liked"
                    )
        

        if request.method=='DELETE':
            # !  Get The Object That Is Being Deleted By Its ID
            question_like=get_object_or_404(
                QuestionLike,
                user_id=user_id,
                question_id=pk #! Used the question id received in the URL Parameter
            )
            # ! Delete The Like Instance
            question_like.delete()
 
            # !Get the Question Instance  and Decrease The Number Of Likes by One
            question=Question.objects.get(id=pk)
            question.is_liked=False
            question.likes-=1
            question.save()
            
            return cr.success(status=HTTP_204_NO_CONTENT)




# ! ViewSet For Questions Answer
class AnswerViewSet(ModelViewSet):

    # ! Adding Filters Backend
    filter_backends=[SearchFilter,OrderingFilter]

    #! Fields Used For Ordering
    ordering_fields=['time_stamp']

    # ! For Specfying Method For ViewSet
    http_method_names=[
        'get',
        'options',
        'head',
        'post',
        'delete'
    ]

    # ! Custom Permission Called
    permission_classes=[IsUserObjectOrAdminPermission]

    def list(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return cr.success(
            data=serializer.data
            )


    def retrieve(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return cr.success(
            data=serializer.data
            )


    def create(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        question_id=self.kwargs['question_pk']
        question=Question.objects.get(id=question_id)
        question.answer_count+=1
        question.save()
        return cr.success(
            status=HTTP_201_CREATED,
            message="You Have Successfuly Created New Post"
        )
    

    def destroy(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        question_id=self.kwargs['question_pk']
        question=Question.objects.get(id=question_id)
        question.answer_count-=1
        question.save()
        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Post Deleted Successfully"
            )


    def get_queryset(self):
        """
        Overriding the queryset to filter the answer 
        by the question id present in the URL Parameter 
        """
        question_id=self.kwargs['question_pk']
        return (
            Answer.objects
            .filter(question_id=question_id)
            .select_related('user')
        ).order_by('-likes')


    def get_serializer_class(self):
        """
        Overriding the serailzer class for assigning Empty Serializer 
        the custom action name  like 
        """
        if self.action=='like':
            return EmptySerializer
        return AnswerSerailizer
    


    def get_serializer_context(self):
        """
        For Passing User_id as well as the questions 
        id as the context
        """
        user_id=self.request.user.id
        question_id=self.kwargs['question_pk']
        return {
            'user_id':user_id,
            'question_id':question_id
        }
    

    # ! Custom Like Action 
    @action(
            detail=True,
            methods=['GET','POST','DELETE'],
            permission_classes=[IsAuthenticated]
        )
    def like(self,request,pk,question_pk):
        """
        Custom Actions For Liking And Removing Like 
        From  Specific Question
        """
        user_id=request.user.id

        if request.method=='GET':
            try:
                answer_like=AnswerLike.objects.filter(
                    user_id=user_id,
                    answer_id=pk 
                )

                if answer_like.exists():
                    return cr.success(data={
                        'is_liked':True
                    })
                return cr.success(data={
                    'is_liked':False
                })
            
            except Exception as e:
                return cr.error(
                    message="Some Error Occured In GET Method",
                    status=HTTP_500_INTERNAL_SERVER_ERROR
            )

        if request.method=='POST':
            try:
                # ! Creates Answer Like Instance For The Answer
                AnswerLike.objects.create(
                    user_id=user_id,
                    answer_id=pk #! Used the answer id received in the URL Parameter
                )

                # ! Get the Answer Instance and Increase the no of likes by One
                answer=Answer.objects.get(id=pk)
                answer.is_liked=True
                answer.likes+=1
                answer.save()

                return cr.success(status=HTTP_201_CREATED)
            
            
            except Exception as e:
                # ! Just For handeling Expections
                print('Error alert: A user is trying to like same object multiple times ')
                return cr.error(
                    message="Already Liked"
                )
        

        if request.method=='DELETE':
            # ! Get the Answer Like Instance If Exists Else Return Error 
            answer_like=get_object_or_404(
                AnswerLike,
                user_id=user_id,
                answer_id=pk #! Used the _like id received in the URL Parameter
            )
            # ! Deletes the answer like instance
            answer_like.delete()

            # ! Get the Answer Instance and decrease the no of likes by One 
            answer=Answer.objects.get(id=pk)
            answer.is_liked=False
            answer.likes-=1
            answer.save()

            return cr.success(
                status=HTTP_204_NO_CONTENT)
            

    




