## Fabfile deploy application
## Put your thinks on servers easily
##
## key words: virtualenv, python, django, wsgi, git, apache, supervisor, nginx
## Carlos Berton [ berton.5b@gmail.com ]

from fabric.api import *
from fabric.contrib.files import exists

# globals
env.project_name = ''

# environments
def devel():
    """
    Use the development virtual server
    """
    env.hosts = ['']
    #env.port = '' # port to connect
    env.user = '' # create a diferente user like deploy
    env.branch = '' # branch to work
    env.path = '' # complete path to project 
    env.virtualhost_path = '' # complete path to virtualenv

def stage():
    """
    Use the stage server
    """
    env.hosts = ['']
    env.port = '' # port to connect
    env.user = '' # create a diferente user like deploy
    env.branch = '' # branch to work
    env.path = '' # complete path to project 
    env.virtualhost_path = '' # complete path to virtualenv

def production():
    """
    Use the production server
    """
    env.hosts = ['']
    env.port = '' # port to connect
    env.user = '' # create a diferente user like deploy
    env.branch = '' # branch to work
    env.path = '' # complete path to project
    env.virtualhost_path = '' # complete path to virtualenv

# Tasks
def setup():
    """
    Setup a virtualenv, create work three directories and run a full deploy
    """
    if not exists(env.path):
        run('mkdir -p %(path)s;' % env)
    with cd(env.virtualhost_path):
        # create a virtualenv for project
        run('virtualenv %(project_name)s;' % env)
    with cd(env.path):
        # create work's directories, see documentation for more details
        if not exists('logs'):
            run('mkdir logs;chmod a+w logs;')
        if not exists('releases'):
            run('mkdir releases;')
        if not exists('packages'):
            run('mkdir packages;')
        if not exists('backups'):
            run('mkdir backups;')
        if not exists('configs'):
            run('mkdir configs;')
        if not exists('statics'):
            run('mkdir statics')
        # make easy your life, add symbolic links
        if not exists('releases/current'):
            run('cd releases; ln -s . current;')
        if not exists('releases/previous'):
            run('ln -s . previous;')
    # launch your code
    deploy()

def deploy():
    """
    Deploy, install any required third party, update and restart the latest version of the webapp 
    """
    # Release use time
    import time
    env.release = time.strftime('%(project_name)s_%d%m%Y%H%M%S') % env
    upload_tar_from_git()
    install_requirements()
    symlink_current_release()
    # don't used
    # collectstatic()
    migrate()
    touch_webserver()

def rollback():
    """
    Rollback, back to any release
    """
    pass

# Helpers
def upload_tar_from_git():
    """
    Create a tar.gz file from git repository and put on server
    """
    require('release', provided_by=[deploy])
    local('git checkout %(branch)s' % env)
    local('git pull origin %(branch)s' % env)
    local('git archive --format=tar %(branch)s | gzip > %(release)s.tar.gz' % env)
    run('mkdir -p %(path)s/releases/%(release)s' % env, pty=True)
    put('%(release)s.tar.gz' % env, '%(path)s/packages/' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../../packages/%(release)s.tar.gz' % env, pty=True)
    local('rm %(release)s.tar.gz' % env)
    
def install_requirements():
    """
    Install the required packages from the requirements file using pip
    """
    require('release', provided_by=[deploy])
    with prefix('source  %(virtualhost_path)s/bin/activate' % env):
        run('cd %(path)s; pip install -r releases/%(release)s/requirements.txt' % env, pty=True)

def symlink_current_release():
    """
    Symlink our current release, configurations and statics and medias
    """
    require('release', provided_by=[deploy])
    with cd(env.path):
        run('rm releases/previous; mv releases/current releases/previous;')
        run('ln -s %(release)s releases/current' % env)
        run('rm releases/current/%(project_name)s/settings.py;') # fim me: check if exist
        run('ln -s %(path)s/configs/settings_%(project_name)s.py releases/current/%(project_name)s/settings.py' % env)
        run('rm -rf releases/current/%(project_name)s/static;') # fix me: check if exist
        run('ln -s %(path)s/statics/%(project_name)s_static releases/current/%(project_name)s/static' % env)
        run('rm -rf releases/current/%(project_name)s/media;') # fix me: check if exist
        run('ln -s %(path)s/statics/%(project_name)s_static/media releases/current/%(project_name)s/media' % env)

def migrate_db():
    """
    Update the database
    """
    pass

def collectstatic():
    """
    Deploy changes on static files - https://docs.djangoproject.com/en/dev/howto/static-files/deployment/
    """
    with prefix('source  %(virtualhost_path)s/bin/activate' % env):
        run('cd %(path)s/releases/current; %(virtualhost_path)s/bin/python manage.py collectstatic -v0 --noinput' % env, pty=True)

    
def restart_supervisor():
    """
    Restart the supervisor
    """
    run('supervisorctl restart %(project_name)s' % env, pty=True)

def restart_nginx():
    """
    Restart the nginx
    """
    run('service nginx restart', pty=True)

def restart_apache():
    """
    Restart the apache
    """
    run('service apache restart', pty=True)

def touch_webserver():
    """
    Touch to restart new configurations
    """
    run('touch %(path)s/%(project_name)s.wsgi' % env, pty=True)
    