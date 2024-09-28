FROM continuumio/miniconda3:latest

LABEL name="mdine-explorer"

ENV ENV_NAME=mdine-explorer
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# Switch to non-root user if necessary (optional depending on base image)
# USER $NB_UID

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    g++ \
    make \
    libc-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ArnaudDroitLab/mdine_explorer.git /app

COPY environment.yml /tmp/environment.yml

# Create environment and install PyMC
RUN conda env create -f /tmp/environment.yml && \
    conda run -n mdine-explorer conda install -c conda-forge -y pymc && \
    conda clean --all -f -y

# Fix PkgResourcesDeprecationWarning
#RUN conda run -n dash-app pip install --upgrade setuptools==58.3.0

# Add conda environment to the PATH
#ENV PATH=/opt/conda/envs/dash-app/bin:$PATH

# Setup working folder
WORKDIR /app

# For running from jupyter notebook
EXPOSE 8080

# Run the application
CMD ["conda", "run", "--no-capture-output", "-n", "mdine-explorer", "python", "scripts/app.py"]

