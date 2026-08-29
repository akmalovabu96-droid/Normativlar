#FROM ubuntu:latest
#LABEL authors="Akbarxon"
#
#ENTRYPOINT ["top", "-b"]

# 1. Grab a clean environment with Python 3.12 pre-installed
FROM python:3.12-slim

# 2. Create and switch to a folder named /app inside Docker
WORKDIR /app

# 3. Copy your project dependencies list
COPY requirements.txt /app/

# 4. Install those dependencies inside Docker
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your entire project (including db.sqlite3) into Docker
COPY . /app/

# 6. Start your Django server on port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
