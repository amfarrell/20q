import db_password

ADMINS = ('Catherine Olsson', 'catherio@mit.edu'
)
DATABASES = {
        'default':{
            'NAME':'/home/catherio/Activities_UROP-Commonsense-Computing/test20q/test20qDB.db',
            'ENGINE': 'django.db.backends.sqlite3',
            'USER': '',
            'PASSWORD':'',
            },
        'ConceptNet':{
            'NAME':'ConceptNet',
            'ENGINE':"postgresql_psycopg2",
            'USER' : "openmind", # change this to your PostgreSQL username
            'HOST' : "csc-sql.media.mit.edu", # or whatever server it's on
            'PORT' : "5432", # or whatever port it's on
            'SCHEMAS' : "public",
            'PASSWORD':db_password.PASSWORD,
            }
        }
DATABASE_ROUTERS = ['dbrouters.gamesRouter',]

MANAGERS = ADMINS

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bvc9l6e-%q_k7@i(k=x44+qje0l+37c&6me&@)b6(6265qb9^+'

helpful_message = """

Congratulations ! you need to fill in a local settings file.

Why? because there are configurations specific to your machine that 
dont work on other boxen.
for instance, the database key.

so, cp this to local_settings.py
and fill in the actual values that you need.

and delete this message from local_settings.py
but leave it in local_settings_template.py

thank you,
Andrew Farrell
"""
print helpful_message
assert False


