FROM continuumio/anaconda:latest

ADD requirements.txt /
RUN conda update -n base conda
RUN conda install --yes openblas
RUN conda install --yes -c conda-forge pymc
RUN conda install --yes --file /requirements.txt
