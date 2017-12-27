from ..services.user import UserService
from ..services.question_record import QuestionRecordService
from ..models.vote_record import VoteRecord


class QuestionTemplateService(object):

    @classmethod
    def template_prep(cls,request):
        page = int(request.params.get('page', 1))
        paginator = QuestionRecordService.get_paginator(request, page)
        author_list = UserService.all_users(request)
        paginator.totalUserVotes = 0
        # total the votes on each question
        #there must be a better way to do this
        query = request.dbsession.query(VoteRecord)
        # time enfficieny is n^2 
        for question in paginator.items:
            question.author = author_list[question.user_id - 1].name
            question.totalVotes = 0
            for vote in query:
                if vote.question_id == question.id:
                    question.totalVotes += vote.vote
        #calculate the totalUserVotes
        for vote in query:
            if author_list[vote.user_id-1].name == request.authenticated_userid:
                paginator.totalUserVotes += 1
        paginator.setAuthors = setAuthors(request)
        return paginator
        
def setAuthors(request):
        setAuthors = []
        user_list = UserService.all_users(request)
        # i need to sort the users for users that have written a question set
        # i can do this by sorting out the questions, and checking if their author ids match
        question_list = QuestionRecordService.all(request)
        for user in user_list:
            for question in question_list:
                if user.id == question.user_id:
                    setAuthors.append(user)
                    break
        return setAuthors
        

            
