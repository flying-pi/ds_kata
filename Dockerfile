FROM jupyter/tensorflow-notebook

ENV JUPYTER_ENABLE_LAB yes
ENV PYTHONHASHSEED 0

WORKDIR /home/jovyan/work/

ENV PYTHONPATH $PYTHONPATH:/home/jovyan/work/src

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN node /opt/conda/lib/python3.6/site-packages/jupyterlab/staging/yarn.js install


