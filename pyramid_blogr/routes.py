def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('register', '/register')
    config.add_route('register-error', '/register-error')
    config.add_route('register-success', '/question-success/{action}',
                     factory='pyramid_blogr.security.QuestionRecordFactory')
    config.add_route('question', '/question/{id:\d+}/{slug}')
    config.add_route('question_action', '/question/{action}',
                     factory='pyramid_blogr.security.QuestionRecordFactory')
    config.add_route('question_action_new', '/question/create',
                     factory='pyramid_blogr.security.QuestionRecordFactory')
    config.add_route('auth', '/sign/{action}')
    config.add_route('thanks', '/thanks')
