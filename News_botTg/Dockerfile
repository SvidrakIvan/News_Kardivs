FROM python:3.10-slim
WORKDIR /bot
# Install python requirements
RUN pip install requests beautifulsoup4 lxml "python-telegram-bot[job-queue]"
COPY bote.py /bot/bote.py
COPY subscriptions.json /bot/subscriptions.json
CMD ["python", "bote.py"]