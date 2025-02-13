{
    'name': "real estate",
    'depends': ['base', 'web'],
    'application': True,
    'data': [
       'security/ir.model.access.csv',
       'views/estate_property_views.xml',
       'views/estate_property_type.xml',
       'views/estate_property_offer.xml',
    ],


}
