FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY robot_simulator.py .
CMD ["python", "-u", "robot_simulator.py"]
