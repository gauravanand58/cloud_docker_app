FROM python:3.7.1

LABEL Author="Gaurav Anand"
LABEL E-mail="gauravanand58@gmail.com"

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "services.py"]
