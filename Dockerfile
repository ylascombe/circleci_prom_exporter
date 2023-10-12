FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ENV GITHUB_USER
# ENV GITHUB_TOKEN
# ENV CIRCLECI_CONTAINER_NAMESPACE
# ENV CIRCLECI_TOKEN
# ENV GITHUB_ORGANIZATIONS

EXPOSE 8000
CMD ["python", "app.py"]