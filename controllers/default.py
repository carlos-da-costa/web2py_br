# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    return dict()


def teste():
    return dict(r=request.env)


def sugestoes():

    def validation(form):
        captcha_resp = request.vars['g-recaptcha-response']
        import requests
        import simplejson as sj
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify',
                             data=dict(secrect='...',
                                       reponse=captcha_resp,
                                       # remoteip=request.env['REMOTE_ADDR']
                                       )
                             )

        st = sj.loads(resp.text)

        if st['success'] == False:
            form.errors.body = ''
            response.flash = 'Por favor, mostre que você não é um robô ;)'

    form = SQLFORM(db.suggestion, submit_button='Enviar Sugestão').process(onvalidation=validation)
    form[0].insert(-1, DIV(LABEL(_class='col-sm-3'),
                           XML('<div class="g-recaptcha col-sm-9" data-sitekey="6LeLalQUAAAAAKIUz-trwFN9pFRrMnRlgNdj8F3F"></div>'),
                           _class='form-group'
                           )
                   )
    suggestions = db(db.suggestion).select(db.suggestion.id,
                                           db.suggestion.body,
                                           db.suggestion.name,
                                           db.suggestion.created,
                                           db.suggestion.likes,
                                           orderby=~db.suggestion.created
                                           )

    if form.accepted:
        response.flash = 'Obrigado pela sua sugestão!'
    return dict(form=form, suggestions=suggestions)



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
