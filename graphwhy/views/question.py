from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.user import User
from ..models.question_record import QuestionRecord
from ..models.question_option import AnswerOption
from ..models.option_vote import OptionVote
from ..models.vote_record import VoteRecord
from ..services.question_record import QuestionRecordService
from ..forms import QuestionCreateForm, QuestionUpdateForm #, VoteCreateForm
from ..services.question_templating import QuestionTemplateService

import pprint
import logging
import datetime
from datetime import timedelta
log = logging.getLogger(__name__)    
    
@view_config(route_name='question_downvote', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def downvote(request):
    vote = VoteRecord()
    userQuery = request.dbsession.query(User)
    userQuery = userQuery.filter(User.name == request.authenticated_userid).first()

    voteQuery = request.dbsession.query(VoteRecord)
    voteQuery = voteQuery.filter(VoteRecord.question_id == int(request.matchdict.get('id',-1)))
    voteQuery = voteQuery.filter(VoteRecord.creator_id == userQuery.id).first()
    
    if voteQuery:
        voteQuery.vote = -1
        request.tm.commit()
    else:
        setattr(vote, 'creator_id', userQuery.id)
        question_id = int(request.matchdict.get('id',-1))
        setattr(vote, 'question_id', question_id)
        setattr(vote, 'vote', -1)
        request.dbsession.add(vote)
    return HTTPFound(location=request.route_url('question_action_new'))


@view_config(route_name='question_upvote', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def upvote(request):
    vote = VoteRecord()
    query = request.dbsession.query(User)
    query = query.filter(User.name == request.authenticated_userid).first()
    setattr(option_vote, 'creator_id', query.id)
    setattr(option_vote, 'option_id', int(request.matchdict.get('optionid', -1)))
    setattr(option_vote, 'question_id', int(request.matchdict.get('questionid', -1)))
    request.dbsession.add(option_vote)
    return HTTPFound(location=request.route_url('question_action_new'))
    

@view_config(route_name='submit_vote', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def question_option_vote(request):
    option_vote = OptionVote()
    userQuery = request.dbsession.query(User)
    userQuery = userQuery.filter(User.name == request.authenticated_userid).first()
   
    optionQuery = request.dbsession.query(OptionVote) 
    optionQuery = optionQuery.filter(OptionVote.creator == userQuery)

    questionQuery = request.dbsession.query(QuestionRecord).filter(QuestionRecord.id == int(request.matchdict.get('questionid',-1))).first()
    optionQuery = optionQuery.filter(OptionVote.question == questionQuery and OptionVote.question.created.date.day != questionQuery.created.date.day).first()
 
 
    if optionQuery:
        optionQuery.created = datetime.datetime.utcnow()
        optionQuery.option_id = int(request.matchdict.get('optionid', -1))
        request.tm.commit()
    else:    
        setattr(option_vote, 'creator_id', userQuery.id)
        setattr(option_vote, 'option_id', int(request.matchdict.get('optionid', -1)))
        setattr(option_vote, 'question_id', int(request.matchdict.get('questionid', -1)))
        request.dbsession.add(option_vote)    
    return HTTPFound(location=request.route_url('question_action_new'))


@view_config(route_name='register-success', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
@view_config(route_name='question_action', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def question_create(request):
    request.active_page = 'question'
    paginator = QuestionTemplateService.template_prep(request)
    entry = QuestionRecord()
    entry_options = AnswerOption()
    form = QuestionCreateForm(request.POST)
    if request.method == 'POST' and form.validate():

        '''
        log.debug("\n\n\n\n\n\n\n\n\n\n\n\n %s \n\n\n\n\n", debugString)
        debugString = pprint.pformat(vars(form.description), indent=4)
        log.debug("\n\n\n\n\n\n\n\n\n\n\n\n %s \n\n\n\n\n", debugString)
        debugString = pprint.pformat(vars(form.question_option.entries[0].form._fields['question_option']), indent=4)
        log.debug("\n\n\n\n\n\n\n\n\n\n\n\n %s \n\n\n\n\n", debugString)
        ''' 

        '''
        form.description.data (check if empty)
        form.question.data
        form.question_option.entries (array)
        form.type.data               
        '''
        # The string that you get from Javascript
        date_string = '2017-12-31'
        date_format = '%Y-%m-%d'
        try:
            date_obj = datetime.datetime.strptime(form.date.data, date_format)
            setattr(entry, 'date', date_obj)
        except ValueError:
            setattr(entry, 'date', datetime.datetime.today() - timedelta(days=3))
            print("Incorrect data format, should be YYYY-MM-DD")

        setattr(entry, 'color', form.color.data)
        setattr(entry, 'question', form.question.data)
        setattr(entry, 'type', form.type.data)
        #if(form.description.data != "")
        setattr(entry, 'description', form.description.data)
   
        query = request.dbsession.query(User)
        query = query.filter(User.name == request.authenticated_userid).first()
        setattr(entry, 'user_id', query.id)      
        request.dbsession.add(entry)
        
        
        # populate question_options (answer_options)
        userid = query.id
        query = request.dbsession.query(QuestionRecord)
        query = query.filter(QuestionRecord.question == request.POST.get('question')).first()
        for val in form.question_option.entries:
            entry_options = AnswerOption()
            setattr(entry_options, 'option_text', val.form._fields['question_option'].data)
            setattr(entry_options, 'creator_id', userid)
            setattr(entry_options, 'question_id', query.id)
            request.dbsession.add(entry_options)
        
        paginator = QuestionTemplateService.template_prep(request)
   
        return HTTPFound(location=request.route_url('question_action_new'))
    return {'form': form, 'action': request.matchdict.get('action'), 'paginator': paginator}
