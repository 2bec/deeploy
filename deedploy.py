##
## Fabfile deploy application
## Put your tinks on servers easily
##
## key words: virtualenv, python, django, wsgi, git, apache, supervisor, nginx
##
## created by: Carlos Berton [ berton.5b@gmail.com ]
##

from fabric.api import *

# globals
env.project_name = ''

# environments
def devel():
    """
    Use the development virtual server
    """

def stage():
    """
    Use the stage server
    """

def production():
    """
    Use the production server
    """

# Tasks
def setup():
    """
    Setup a virtualenv, create work three directories and run a full deploy
    """

def deploy():
    """
    Deploy, install any required third party, update and restart the latest version of the webapp 
    """

def rollback():
    """
    Rollback, back to any release
    """

# Helpers
def upload_tar_from_git():
    """
    Create a tar.gz file from git repository and put on server
    """
    
def install_requirements():
    """
    Install the required packages from the requirements file using pip
    """

def symlink_current_release():
    """
    Symlink our current release, configurations and statics and medias
    """

def migrate_db():
    """
    Update the database
    """

def collectstatic():
    """
    Deploy changes on static files - https://docs.djangoproject.com/en/1.9/howto/static-files/deployment/
    """
    
def restart_supervisor():
    """
    Restart the supervisor
    """
    
def restart_webserver():
    """
    Restart the web server
    """
    