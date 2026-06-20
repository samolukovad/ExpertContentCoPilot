{
    'name': 'Expert Content CoPilot',
    'version': '1.0',
    'category': 'Content Management',
    'summary': 'Digital assistant for expert content creation',
    'description': """
        ExpertContentCoPilot helps experts and companies systematically create,
        store and develop professional content: articles, speeches, posts and training materials.
    """,
    'author': 'Samolukovad',
    'website': 'https://github.com/samolukovad/ExpertContentCoPilot',
    'depends': ['base', 'mail', 'calendar'],
    'data': [
        #'security/ir.model.access.csv',
        #'data/sequence_data.xml',
        'views/content_idea_views.xml',
        'views/content_article_views.xml',
        'views/content_plan_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}