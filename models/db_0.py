# -*- coding: utf-8 -*-
from gluon.contrib.markdown import markdown2

db.define_table('suggestion',
               Field('body', 'text', label='Sugestão', comment='Sugestão sobre assuntos relacionados a Web2py ou desenvolvimento Web.'),
               Field('name', label='Nome', comment='Opcional'),
               Field('email', requires=IS_EMPTY_OR(IS_EMAIL()), label='E-mail', comment='Opcional. Não será divulgado.'),
               Field('likes', 'integer', default=0, readable=False, writable=False),
               Field('created', 'datetime', default=request.now, readable=False, writable=False)
               )


db.define_table('category',
                Field('title'),
                Field('identifier'),
                format='%(title)s'
                )

db.define_table('article',
                Field('title'),
                Field('identifier'),
                Field('body', 'text', represent=lambda v, r: XML(markdown2.markdown(v[:100])) if v else ''),
                Field('category', db.category)
                )