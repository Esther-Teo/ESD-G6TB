FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt paymentreq.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r paymentreq.txt
COPY ./payment.py .
CMD [ "python", "./payment.py" ]