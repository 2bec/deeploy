# deeploy
python + fabric + django + apache + nginx + supervisor + git

## Requirements
```
pip install fabric
```

## Deploy anywhere
This file just make a easy way to deploy any project with a git repository in any environments. 
So this file contains: tasks, helpers, environments
You just set the environments configs and go.

## Usage
Put this file on our project git repository (/), set enrironments configs [hosts,port,user,branch,path,virtualpath] and run:
```
fab stage setup deploy
```

