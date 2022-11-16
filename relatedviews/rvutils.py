def subtractlists(include,exclude):
    return filter(lambda x: x not in exclude, include) 

def cstolist(value):
    """convert comma separated values to list identifying proper type.List object remains unchanged """
    if value in (None,'',u''):
        return []
    if isinstance(value,(str,str)):
        #do typecasting
        rawvalues=str(value).split(',')
        if rawvalues[0].isdigit():
            value = [int(v) for v in rawvalues]
        else:
            value = [v for v in rawvalues]
    elif isinstance(value,(int,)):
        value=[value]
    return value
