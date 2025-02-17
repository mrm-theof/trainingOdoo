{
    'name': "real estate",
    'depends': ['base', 'web'],
    'application': True,
    'data': [
       'security/ir.model.access.csv',
       'views/estate_property_views.xml',
       'views/estate_property_type.xml',
       'views/estate_property_offer.xml',
        'views/estate_property_tag.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml',
    ],


}
