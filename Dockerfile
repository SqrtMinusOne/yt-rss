FROM python:3.9
COPY requirements.txt /
RUN pip install -r requirements.txt
COPY main.py /
EXPOSE 8000
CMD gunicorn main:app -b 0.0.0.0:8000
