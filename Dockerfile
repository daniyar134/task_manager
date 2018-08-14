FROM frolvlad/alpine-python3
ADD . /opt/task_manager/
WORKDIR /opt/task_manager/
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN python3 manage.py test
CMD ["/bin/bash", "./run.sh"]
