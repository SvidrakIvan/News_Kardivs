FROM jenkins/jenkins

ENV JENKINS_USER admin
ENV JENKINS_PASS admin


# Skip initial setup
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
COPY plugins.txt /usr/share/jenkins/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/plugins.txt
COPY config.xml /usr/share/jenkins/ref/jobs/Kursova/config.xml

USER root
# Create credentials
COPY --chown=jenkins:jenkins credentials.groovy /usr/share/jenkins/ref/init.groovy.d/credentials.groovy
COPY --chown=jenkins:jenkins startupTrigger.groovy /usr/share/jenkins/ref/init.groovy.d/startupTrigger.groovy
COPY credentials-telegram.groovy /usr/share/jenkins/ref/init.groovy.d/credentials-telegram.groovy

# Копіювання init.sh скрипта
COPY init.sh /usr/share/jenkins/init.sh
RUN chmod +x /usr/share/jenkins/init.sh

RUN apt-get update \
    && apt-get install -qqy apt-transport-https ca-certificates curl gnupg2 software-properties-common groovy
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"

RUN apt-get update -qq \
    && apt-get install docker-ce -y \
    && apt-get clean

RUN usermod -aG docker jenkins

RUN curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose

USER jenkins

# Запуск скрипта init.sh перед запуском Jenkins
ENTRYPOINT ["/bin/bash", "-c", "/usr/share/jenkins/init.sh && /usr/local/bin/jenkins.sh"]