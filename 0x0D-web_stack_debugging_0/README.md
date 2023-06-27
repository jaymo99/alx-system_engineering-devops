# 0x0D. Web stack debugging #0

## Concepts
* [Network basics](https://intranet.alxswe.com/concepts/33)
* [Docker](https://intranet.alxswe.com/concepts/65)
* [Web stack debugging](https://intranet.alxswe.com/concepts/68)

## Background context
The Webstack debugging series is a training for the art of debugging. Being able to debug a webstack is essential for a Full-Stack software engineer, and it takes practice to be a master of it.
<br/>
In this series, broken/bugged webstacks are provided, the final goal is to come up with a bash script that once executed, will bring the webstack to a working state.
The bugged webstacks are provided in a `docker container`

## Tasks
0. In this first debugging project, you will need to get `Apache` to run on the container and to return a page containing `Hello Holberton` when querying the root of it.

Example
```bash
vagrant@vagrant:~$ docker run -p 8080:80 -d -it holbertonschool/265-0
47ca3994a4910bbc29d1d8925b1c70e1bdd799f5442040365a7cb9a0db218021
vagrant@vagrant:~$ docker ps
CONTAINER ID        IMAGE                   COMMAND             CREATED             STATUS              PORTS                  NAMES
47ca3994a491        holbertonschool/265-0   "/bin/bash"         3 seconds ago       Up 2 seconds        0.0.0.0:8080->80/tcp   vigilant_tesla
vagrant@vagrant:~$ curl 0:8080
curl: (52) Empty reply from server
vagrant@vagrant:~$
```

Here we can see that after starting the docker container, I `curl` the port `8080` mapped to the docker container port `80`, it does not return a page but an error message.

<br/>
The expected output after fixing the bug is shown below
```bash
vagrant@vagrant:~$ curl 0:8080
Hello Holberton
vagrant@vagrant:~$
```

This issue was fixed using script `0-give_me_a_page`
