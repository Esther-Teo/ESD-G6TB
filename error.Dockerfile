FROM python:3-slim
WORKDIR /usr/src/app
COPY amqp.txt ./
RUN pip install --no-cache-dir -r amqp.txt
COPY ./error.py ./amqp_setup.py ./
CMD [ "python", "./error.py" ]