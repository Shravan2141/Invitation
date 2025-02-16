# Gunicorn Configuration for Render Free Tier

# Server Socket
bind = "0.0.0.0:5000"

# Worker Processes (Minimal for free tier)
workers = 1
threads = 1

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stdout
loglevel = "info"

# Process Naming
proc_name = "techkshetra_face_detection"

# Timeout Settings
timeout = 120
keepalive = 5

# Performance Constraints
max_requests = 100
max_requests_jitter = 25
