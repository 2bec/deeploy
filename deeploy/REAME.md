# Deeploy

## Ambiente de desenvolvimento
Para iniciar o ambiente de desenvolvimento você precisa realizar algumas etapas de configuração do seu sistema.
Usamos nginx, docker, redis, mysql:

### Instalar nginx e configurar
Dentro da pasta raiz do projeto:

```
$ sudo apt-get update
$ sudo apt-get install nginx
$ sudo cp -n deeploy/nginx/brik.dev /etc/nginx/sites-available/brik.dev
$ sudo ln -s /etc/nginx/sites-available/brik.dev /etc/nginx/sites-enabled/brik.dev
$ sudo service nginx stop && service nginx start
```

### Intalar docker e configurar
(https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)[https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1]

#### Script
```
$ curl -fsSL get.docker.com -o get-docker.sh
```

Se o susuário ainda não  está no grupo do docker:
```
$ sudo usermod -aG docker your-user
```

Para instalar:
```
$ sudo sh get-docker.sh
$ sudo systemctl enable docker

```

#### Manualmente
```
$ sudo apt-get remove docker docker-engine docker.io
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
$ apt-cache madison docker-ce
$ sudo apt-get install docker-ce
```