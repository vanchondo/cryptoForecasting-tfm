FROM python:3.9

# ADD requirements.txt .
# ADD forecasters forecasters
# ADD main.py .
ADD . .
RUN pip install -r requirements.txt

CMD ["python", "./main.py"] 