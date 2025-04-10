# Use an official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ensure STATIC_ROOT is set in settings.py (You should also update this in your settings.py)
ENV DJANGO_SETTINGS_MODULE=cloudstorage.settings

# Collect static files (make sure STATIC_ROOT is set correctly in settings.py)
RUN mkdir -p /app/static
RUN python manage.py collectstatic --noinput || true

# Expose port 8000
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
