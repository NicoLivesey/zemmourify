# pull official base image
FROM python:3.8-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLIT_ROOT_INSTALL=1
ENV PIP_FIND_LINKS=https://download.pytorch.org/whl/torch_stable.html
ENV PIP_NO_CACHE_DIR=1
WORKDIR /task

# Install build tools
RUN apt-get update && \
  apt-get install -y make && \
  pip install --upgrade pip && \
  pip install flit

ARG env="PROD"

# Install zsh inside docker for nicer development experiences
RUN if [ "$env" = "DEV" ]; then \
  apt-get install -y wget && \
  sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)" && \
  chsh -s $(which zsh); \
fi;

# Install dependencies
COPY ./pyproject.toml ./
COPY ./zemmourify/__init__.py ./zemmourify/__init__.py
RUN touch README.md

# ARG model_type
# flit install --deps production --symlink --extra ${model_type},demo;

RUN if [ "$env" = "PROD" ]; then \
  flit install --deps production --symlink; \
else \
  flit install --deps develop --symlink; \
fi;

# Add code
COPY ./zemmourify ./zemmourify

# Download model
# RUN if [ "$env" = "PROD" ]; then \
#   python zemmourify/download.py --save-as-pkl; \
# fi;

COPY ./Makefile .


# Reduce Docker size
RUN \
  cd /usr/local/lib/python3.8/site-packages; \
	du -sh .; \
	find . -type d -name "tests" -exec rm -rf {} +; \
	find . -type d -name "__pycache__" -exec rm -rf {} +; \
	rm -rf caffe2 wheel boto* aws* pipenv \
	rm -rf {*.egg-info,*.dist-info}; \
	find . -name \*.pyc -delete; \
	du -sh .; \
	rm -rf /root/.cache

ENTRYPOINT ["/bin/bash"]
# ENTRYPOINT ["uvicorn", "zemmourify.main:app", "--host", "0.0.0.0", "--port", "80"]
CMD []