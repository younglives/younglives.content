""" Helper methods for extender modifiers. """


def fiddle_visibility(schema, 
                      enabled_schematas=[], disabled_schematas=[], 
                      enabled_fields=[], disabled_fields=[]):
    
    for i in schema.widgets():
        fld = schema[i]
        if fld.schemata in enabled_schematas: 
            schema[i].widget.visible={'edit':'visible', 'view':'visible'}
        elif fld.schemata in disabled_schematas:
            schema[i].widget.visible={'edit':'invisible', 'view':'invisible'}
            
    for e in enabled_fields: 
        schema[e].widget.visible={'edit':'visible', 'view':'visible'}
    for d in disabled_fields: 
        schema[d].widget.visible={'edit':'invisible', 'view':'invisible'}