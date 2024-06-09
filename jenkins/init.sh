#!/bin/bash

# Виконання Groovy скрипта до запуску Jenkins
echo "Running pre-start Groovy script..."
groovy /usr/share/jenkins/ref/init.groovy.d/credentials-telegram.groovy