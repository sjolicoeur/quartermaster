FROM    ubuntu:14.04

MAINTAINER Stephane Jolicoeur <s.jolicoeur+docker@gmail.com>

RUN     apt-get update && apt-get install -y apt-utils && apt-get install -y  \
            python-setuptools \
            build-essential \
            autoconf \
            libtool \
            python-dev \
            libffi-dev \
            libssl-dev \
            python-openssl \
            &&  easy_install pip \
            && pip install docker-py==1.0.0 \
			&& pip install ipython==2.4.1 \
			&& pip install python-etcd==0.3.2 \
			&& pip install requests==2.1.0 \
			&& pip install simplejson==3.6.5 \
            && apt-get -y autoremove \
            && apt-get clean && mkdir -p /opt/quartermaster

COPY    ./quartermaster/   /opt/quartermaster

RUN     cd /opt/quartermaster \
			&& ls /opt && ls /opt/quartermaster \
            && pip install -r requirements.txt 

CMD  ["python", "/opt/quartermaster/quartermaster.py"]
