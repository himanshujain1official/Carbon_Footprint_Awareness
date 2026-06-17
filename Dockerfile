# Use the official Python 3.13 slim image for a lightweight footprint
FROM python:3.13-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies without caching to keep the image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 8080 as expected by Google Cloud Run
EXPOSE 8080

# Environment variables to optimize Streamlit for production
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Force Light Theme via Environment Variables for Cloud Run
ENV STREAMLIT_THEME_BASE=light
ENV STREAMLIT_THEME_PRIMARY_COLOR="#4285F4"
ENV STREAMLIT_THEME_BACKGROUND_COLOR="#FFFFFF"
ENV STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR="#F8F9FA"
ENV STREAMLIT_THEME_TEXT_COLOR="#202124"

# Run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
