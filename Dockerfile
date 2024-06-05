FROM python:3.12.3

WORKDIR /app

COPY fruit_shop/requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

