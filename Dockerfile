FROM python:3.9-buster

WORKDIR /app
RUN git clone git@github.com:jangita/akili-grid.git . && pip install -r conf/requirements.txt

ENTRYPOINT ["/bin/bash"]
