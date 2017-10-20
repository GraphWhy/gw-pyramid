from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from ..models.user import User
from ..models.question_record import QuestionRecord
from ..services.question_record import QuestionRecordService
from ..forms import QuestionCreateForm, QuestionUpdateForm
from ..services.question_templating import QuestionTemplateService



@view_config(route_name='register-success', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_question_success.jinja2',
             permission='create')
@view_config(route_name='question_action', match_param='action=create',
             renderer='pyramid_blogr:templates/edit_question.jinja2',
             permission='create')
def question_create(request):
    paginator = QuestionTemplateService.author_names(request)
    entry = QuestionRecord()
    form = QuestionCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        query = request.dbsession.query(User)
        query = query.filter(User.name == request.authenticated_userid).first()
        setattr(entry, 'user_id', query.id)
        request.dbsession.add(entry)
        return HTTPFound(location=request.route_url('question_action_new'))
    return {'form': form, 'action': request.matchdict.get('action'), 'paginator': paginator}
