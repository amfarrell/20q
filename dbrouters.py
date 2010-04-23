import pdb
CSC_apps = (
        'django.contrib.auth',
        #'django.contrib.contenttypes',
        #'django.contrib.sessions',
        #'django.contrib.sites',
        #'django.contrib.admin',
        'csc.pseudo_auth',
        'csc.corpus',
        'csc.conceptnet',
        'csc.nl',
        'voting',
        'events',
        'south',
        #'django.contrib.markup',
        #'corpus.parse',
        #'realm',
        ) 
class gamesRouter(object):
    """
    This directs all of the requests for ConceptNet objects to the
    ConceptNet database. Everything else goes to localhost.
    """
    def onCSC(self,db_table):
        """
        Is this database table actually stored on csc-sql.mit.edu?
        """
        if 'conceptnet' in db_table:
            return True
        else:
            if db_table in\
                ('corpus_language',
                        ) :
                return True
        return False
    def db_for_read(self,model,**hints):
        """

        """
        if model._meta.app_label in CSC_apps :
            return 'ConceptNet'
        elif self.onCSC(model._meta.db_table):
            return 'ConceptNet'
        else:
            return 'default'

    def db_for_write(self,model,**hints):
        if model._meta.app_label in CSC_apps :
            return 'ConceptNet'
        elif self.onCSC(model._meta.db_table):
            return 'ConceptNet'
        else:
            return 'default'

