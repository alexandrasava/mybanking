# Dockerfile

FROM python:3.5.2
COPY . /docker_dir
WORKDIR /docker_dir
RUN pip install -r requirements.txt
RUN chmod +x /docker_dir/docker-entrypoint.sh
CMD ["/bin/bash", "/docker_dir/docker-entrypoint.sh"]
