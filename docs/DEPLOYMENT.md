# Deployment Guide - AI Race Engineer Copilot

## Overview

This guide covers deploying the AI Race Engineer Copilot dashboard to various platforms.

## Deployment Options

### 1. Streamlit Cloud (Recommended)

**Pros:**
- Free tier available
- Easy deployment from GitHub
- Automatic HTTPS
- Built-in secrets management

**Steps:**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `frontend/app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In Streamlit Cloud dashboard, go to app settings
   - Add secrets in TOML format:
   ```toml
   [ibm]
   WATSONX_API_KEY = "your_api_key"
   WATSONX_PROJECT_ID = "your_project_id"
   WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
   GRANITE_MODEL_ID = "ibm/granite-13b-chat-v2"
   ```

4. **Access Your App**
   - Your app will be available at: `https://your-app-name.streamlit.app`

### 2. Heroku Deployment

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**

1. **Create Heroku App**
   ```bash
   heroku create ai-race-engineer-copilot
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set IBM_WATSONX_API_KEY=your_api_key
   heroku config:set IBM_WATSONX_PROJECT_ID=your_project_id
   heroku config:set IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
   heroku config:set GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

4. **Open App**
   ```bash
   heroku open
   ```

### 3. Docker Deployment

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**

```bash
# Build image
docker build -t ai-race-engineer .

# Run container
docker run -p 8501:8501 \
  -e IBM_WATSONX_API_KEY=your_key \
  -e IBM_WATSONX_PROJECT_ID=your_project \
  ai-race-engineer
```

**Docker Compose:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - IBM_WATSONX_API_KEY=${IBM_WATSONX_API_KEY}
      - IBM_WATSONX_PROJECT_ID=${IBM_WATSONX_PROJECT_ID}
      - IBM_WATSONX_URL=${IBM_WATSONX_URL}
      - GRANITE_MODEL_ID=${GRANITE_MODEL_ID}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 4. AWS EC2 Deployment

**Steps:**

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t2.medium or larger
   - Open port 8501 in security group

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Python
   sudo apt install python3.9 python3-pip -y
   
   # Clone repository
   git clone https://github.com/yourusername/ai-race-engineer-copilot.git
   cd ai-race-engineer-copilot
   
   # Install dependencies
   pip3 install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your credentials
   ```

4. **Run with systemd**
   
   Create `/etc/systemd/system/race-engineer.service`:
   ```ini
   [Unit]
   Description=AI Race Engineer Copilot
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai-race-engineer-copilot
   Environment="PATH=/home/ubuntu/.local/bin"
   ExecStart=/usr/bin/python3 -m streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable race-engineer
   sudo systemctl start race-engineer
   sudo systemctl status race-engineer
   ```

5. **Setup Nginx (Optional)**
   ```bash
   sudo apt install nginx -y
   ```
   
   Configure `/etc/nginx/sites-available/race-engineer`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

### 5. Google Cloud Run

**Steps:**

1. **Create Dockerfile** (see Docker section above)

2. **Build and Push**
   ```bash
   # Set project
   gcloud config set project your-project-id
   
   # Build image
   gcloud builds submit --tag gcr.io/your-project-id/race-engineer
   ```

3. **Deploy**
   ```bash
   gcloud run deploy race-engineer \
     --image gcr.io/your-project-id/race-engineer \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars IBM_WATSONX_API_KEY=your_key,IBM_WATSONX_PROJECT_ID=your_project
   ```

## Environment Variables

Required environment variables for all deployments:

```bash
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
GRANITE_MODEL_ID=ibm/granite-13b-chat-v2
```

Optional:
```bash
LANGFLOW_URL=http://localhost:7860
GRANITE_MAX_TOKENS=1024
GRANITE_TEMPERATURE=0.7
```

## Security Best Practices

1. **Never commit secrets**
   - Use `.gitignore` for `.env` and `secrets.toml`
   - Use platform-specific secrets management

2. **Use HTTPS**
   - Enable SSL/TLS for production
   - Use Let's Encrypt for free certificates

3. **Restrict Access**
   - Use authentication if needed
   - Implement rate limiting
   - Monitor API usage

4. **Regular Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Use automated security scanning

## Performance Optimization

1. **Caching**
   - Enable Streamlit caching
   - Cache AI responses
   - Use CDN for static assets

2. **Resource Limits**
   - Set appropriate memory limits
   - Configure timeout values
   - Monitor resource usage

3. **Scaling**
   - Use load balancer for multiple instances
   - Implement auto-scaling
   - Monitor performance metrics

## Monitoring

### Health Checks

Add health check endpoint:
```python
# In app.py
if st.query_params.get("health") == "check":
    st.write("OK")
    st.stop()
```

### Logging

Configure logging:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Metrics

Monitor:
- Response times
- Error rates
- API usage
- User sessions
- Resource utilization

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process
lsof -i :8501

# Kill process
kill -9 <PID>
```

**Memory Issues:**
```bash
# Increase memory limit
streamlit run frontend/app.py --server.maxUploadSize=200
```

**Slow Performance:**
- Enable caching
- Optimize queries
- Use connection pooling
- Implement lazy loading

## Rollback Strategy

1. **Keep Previous Version**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Quick Rollback**
   ```bash
   git revert HEAD
   git push origin main
   ```

3. **Platform-Specific**
   - Streamlit Cloud: Use version history
   - Heroku: `heroku rollback`
   - Docker: Keep previous images

## Cost Optimization

1. **Free Tiers**
   - Streamlit Cloud: Free for public apps
   - Heroku: Free dyno (with limitations)
   - AWS: Free tier for 12 months

2. **Resource Management**
   - Use appropriate instance sizes
   - Implement auto-shutdown for dev
   - Monitor and optimize API calls

3. **Caching Strategy**
   - Cache AI responses
   - Use CDN for static content
   - Implement request deduplication

## Support

For deployment issues:
1. Check logs
2. Review documentation
3. Contact platform support
4. Open GitHub issue

---

**Ready to deploy? Choose your platform and follow the steps above! 🚀**