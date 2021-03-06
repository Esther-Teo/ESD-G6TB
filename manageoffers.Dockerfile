FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r amqp.txt
COPY ./manageOffers.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./manageOffers.py" ]