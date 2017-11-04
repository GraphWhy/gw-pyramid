from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import remember, forget
from ..services.user import UserService
from ..forms import RegistrationForm
from ..models.user import User
from ..services.question_templating import QuestionTemplateService


# ROUTES IN ACTIVE USE ---
@view_config(route_name='home',
             renderer='pyramid_blogr:templates/register.jinja2')
@view_config(route_name='register-error',
             renderer='pyramid_blogr:templates/register-error.jinja2')
def index_page(request):
    paginator = QuestionTemplateService.template_prep(request)
    # sign-in form
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        # ensure people don't choose username over and over again
        username = form.username.data
        if username == 'username':
            return HTTPFound(location=request.route_url('register-error'))
        # if user exists then log them in - LOG IN LOGIC
        flag = request.dbsession.query(User).filter_by(name=username).all()
        if flag:
            user = UserService.by_name(username, request=request)
            if user and user.verify_password(request.POST.get('password')):
                headers = remember(request, user.name)
            else:
                headers = forget(request)
            return HTTPFound(location=request.route_url('question_action_new'), headers=headers)
        # create account logic
        new_user = User(name=username)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        # if all is successful
        headers = remember(request, username)
        return HTTPFound(location=request.route_url('register-success',action='create'), headers=headers)
    return {'form': form, 'paginator': paginator}


@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = UserService.by_name(username, request=request)
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(route_name='register',
             renderer='pyramid_blogr:templates/register.jinja2')
def register(request):
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_user = User(name=form.username.data)
        new_user.set_password(form.password.data.encode('utf8'))
        request.dbsession.add(new_user)
        return HTTPFound(location=request.route_url('home'))
    return {'form': form}
