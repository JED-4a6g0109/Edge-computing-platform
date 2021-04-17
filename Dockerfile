FROM python:3.7.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /Edge-computing-platform
WORKDIR /Edge-computing-platform
COPY . /Edge-computing-platform/
RUN pip install -r requirements.txt

