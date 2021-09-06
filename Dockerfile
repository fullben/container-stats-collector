FROM python:3.9-bullseye
WORKDIR /home/stats-collector
COPY container-stats-collector.py /home/stats-collector
RUN pip install docker
RUN pip install datetime
CMD [ "python", "container-stats-collector.py" ]
