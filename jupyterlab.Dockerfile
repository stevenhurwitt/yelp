FROM cluster-base

# -- Layer: JupyterLab

ARG spark_version=3.4.4
ARG jupyterlab_version=3.2.0

COPY ./requirements.txt /opt/workspace/requirements.txt
COPY ./creds.json /opt/workspace/creds.json
COPY . /opt/workspace/

RUN apt-get update -y && \
    apt-get install -y python3-venv && \
    apt-get install -y python3-pip && \
    apt-get install -y libpq-dev && \
    python3 -m venv venv && \
    pip3 install --upgrade pip && \
	pip3 install pypandoc==1.5 && \
    pip3 install pyspark==${spark_version} jupyterlab==${jupyterlab_version} && \
	pip3 install wget && \
    pip3 install numpy && pip3 install pandas==1.3.0 && pip3 install matplotlib && pip3 install psycopg2-binary && \
    pip3 install -r /opt/workspace/requirements.txt
    # rm -rf /var/lib/apt/lists/* && \
    # ln -s /usr/local/bin/python3 /usr/bin/python

RUN apt-get update && \
    apt-get install -y libbz2-dev && \
    apt-get install -y python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -- Runtime

EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=

