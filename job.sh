#!/bin/bash

cd /home/tty025/teste/Projetos/scriptDesbloqueio

if [ "$1" == "" ]; then true & exit; fi

/usr/local/bin/python3.6 /home/tty025/teste/Projetos/scriptDesbloqueio/script.py "$1" >> /home/tty025/teste/Projetos/scriptDesbloqueio/log.txt
