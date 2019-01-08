from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.user import User
from ..models.question_record import QuestionRecord
from ..models.vote_record import VoteRecord
from ..services.question_record import QuestionRecordService
from ..forms import QuestionCreateForm, QuestionUpdateForm #, VoteCreateForm
from ..services.question_templating import QuestionTemplateService
    
    
@view_config(route_name='question_downvote', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def downvote(request):
    vote = VoteRecord()
    query = request.dbsession.query(User)
    query = query.filter(User.name == request.authenticated_userid).first()
    setattr(vote, 'user_id', query.id)
    question_id = int(request.matchdict.get('id',-1))
    setattr(vote, 'question_id', question_id)
    setattr(vote, 'vote', -1)
    request.dbsession.add(vote)
    return HTTPFound(location=request.route_url('question_action_new'))


@view_config(route_name='question_upvote', match_param='action=create',
             renderer='graphwhy:templates/questions_success.jinja2',
             permission='create')
def upvote(request):
    vote = VoteRecord()
    query = request.dbsession.query(User)
    query = query.filter(User.name == request.authenticated_userid).first()
    setattr(vote, 'user_id', query.id)
    question_id = int(request.matchdict.get('id',-1))
    setattr(vote, 'question_id', question_id)
    setattr(vote, 'vote', 1)
    request.dbsession.add(vote)
    return HTTPFound(location=request.route_url('question_action_new'))
    

@view_config(route_name='register-success', match_param='action=create',
             renderer='graphwhy:templates/questions_success.jinja2',
             permission='create')
@view_config(route_name='question_action', match_param='action=create',
             renderer='graphwhy:templates/questions.jinja2',
             permission='create')
def question_create(request):
    request.active_page = 'question'
    paginator = QuestionTemplateService.template_prep(request)
    entry = QuestionRecord()
    form = QuestionCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        query = request.dbsession.query(User)
        query = query.filter(User.name == request.authenticated_userid).first()
        setattr(entry, 'user_id', query.id)
        request.dbsession.add(entry)
        paginator = QuestionTemplateService.template_prep(request)
        return HTTPFound(location=request.route_url('question_action_new'))
    return {'form': form, 'action': request.matchdict.get('action'), 'paginator': paginator}
