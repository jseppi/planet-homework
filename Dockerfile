FROM continuumio/miniconda3:4.10.3

RUN python --version

WORKDIR /work

COPY requirements.txt .

RUN conda create -n planet-homework python=3.8 && \
    conda install -y -n planet-homework -c conda-forge --file requirements.txt

COPY . /work/

EXPOSE 8000

CMD ["conda", "run", "--no-capture-output", "-n", "planet-homework", \
     "uvicorn", "--host", "0.0.0.0", "app:server"]
