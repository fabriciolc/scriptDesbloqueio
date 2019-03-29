#!/bin/bash

cd /home/tty025/teste/Projetos/scriptDesbloqueio

/usr/bin/git add .
/usr/bin/git commit -m 'Atualizacao da semana' >> git.log
/usr/bin/git push origin master >> git.log
