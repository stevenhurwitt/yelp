FROM cluster-base

# -- Layer: JupyterLab

ARG spark_version=3.3.2
ARG jupyterlab_version=3.5.2

COPY ./notebooks/ ${SHARED_WORKSPACE}/
COPY ./creds.json ${SHARED_WORKSPACE}/notebooks/creds.json
COPY ./requirements.txt ${SHARED_WORKSPACE}/notebooks/requirements.txt

# base python
RUN apt-get update -y && \
    apt-get install -y python3-dev python3-distutils python3-setuptools python3-venv && \
    curl https://bootstrap.pypa.io./get-pip.py | python3 && \
    python3 -m pip install --upgrade pip

# virtualenv
RUN python3 -m venv /opt/workspace/yelp-env && \
    source /opt/workspace/yelp-env/bin/activate

# pyspark & jupyterlab
RUN pip3 install pyspark==${spark_version} jupyterlab==${jupyterlab_version}

# requirements
RUN pip3 install -r /opt/workspace/notebooks/requirements.txt --ignore-installed


# add kernel to jupyter
RUN python3 -m ipykernel install --user --name="yelp-env"
    
# aws
RUN rm -rf /var/lib/apt/lists/* && \
    mkdir root/.aws
    # aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID} && \
    # aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
    # ln -s /usr/local/bin/python3 /usr/bin/python

# deal w/ outdated pyspark guava jar for hadoop-aws (check maven repo for hadoop-common version)
# RUN cd /usr/local/lib/python3.7/dist-packages/pyspark/jars/ && \
#     rm guava-14.0.1.jar && \
#     wget https://repo1.maven.org/maven2/com/google/guava/guava/31.1-jre/guava-31.1-jre.jar


# -- Runtime

EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=easy --NotebookApp.password=easy --notebook-dir=${SHARED_WORKSPACE}
