FROM python:3.13-alpine
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && pip install --no-cache-dir .
COPY cozy/ .
EXPOSE 8000
# We set a long timeout for keep-alive connections to accommodate long-running requests.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "1800"]
