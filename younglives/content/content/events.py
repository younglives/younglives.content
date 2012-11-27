from xmlrpclib import ServerProxy

def pushToCountrySites(ob, event):
    import pdb;pdb.set_trace()
    client = ServerProxy('http://test_user:password@localhost:8080/india')
    weblion = {'/india/weblion': [
        {'title': 'PSU WebLion',
         'remoteUrl': 'http://weblion.psu.edu/'},
        'Link']
        }
    object_path = client.post_object(weblion)
    print object_path
