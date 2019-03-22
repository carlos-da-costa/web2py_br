
@auth.requires_membership('admin')
def manage_categories():
    return dict(grid=SQLFORM.grid(db.category))


def list_articles():
    articles = db(db.article).select(orderby=~db.article.created_on)
    return dict(articles=articles)


def list_categories():
    categories = db(db.category).select(orderby=~db.category.created_on)
    return dict(categories=categories)


def list_category():
    category = db(db.category.identifier==request.vars.category).select().first()
    if category:
        articles = db(db.article.category==category.id).select()
        return dict(articles=articles, category=category)
    else:
        raise HTTP(404)


def article():
    article = db(db.article.identifier == request.vars.id).select().render(0)
    if article:
        return dict(article=article)
    else:
        HTTP(404)


@auth.requires_membership('admin')
def manage_articles():
    grid = SQLFORM.grid(db.article)
    return dict(grid=grid)


@auth.requires_membership('admin')
def edit_article():
    if request.vars.article:
        article = db(db.article.identifier==request.vars.article).select().first()
        if article:
            form = SQLFORM(article.id).process()
        else:
            HTTP(404)
    else:
        form = SQLFORM(db.article).process()
    return dict(form=form)