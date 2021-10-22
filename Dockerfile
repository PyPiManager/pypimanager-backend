FROM python:3.7.12-buster
MAINTAINER toddlerya <toddlerya@gmail.com>

ENV TIME_ZONE Asia/Shanghai

WORKDIR /home/pypimanager_backend

COPY . /home/pypimanager_backend

RUN pip install -U pip
RUN pip config set global.index-url http://pypi.douban.com/simple
RUN pip config set install.trusted-host pypi.douban.com

RUN pip install --no-cache-dir --upgrade -r /home/pypimanager_backend/requirements.txt

# CMD ["uvicorn", "pypimanager_backend.server:app", "--host", "0.0.0.0", "--port", "80"]

CMD ["python", "manager.py"]