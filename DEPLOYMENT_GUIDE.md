# Magazine Task Management System - Deployment Guide

## Table of Contents
1. [Replit Deployment (Recommended)](#replit-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Manual Deployment](#manual-deployment)
4. [Environment Variables](#environment-variables)
5. [Database Setup](#database-setup)

---

## Replit Deployment (Recommended)

This application is optimized for Replit deployment with autoscale capabilities.

###  Prerequisites
- Replit account
- PostgreSQL database (automatically provided by Replit)

### Deployment Steps

1. **Click the "Deploy" button** in Replit interface
   - The deployment target is set to `autoscale`
   - This means the app only runs when receiving requests (cost-effective)

2. **Environment Variables** (Set in Secrets tab)
   ```
   DATABASE_URL=<automatically set by Replit>
   SESSION_SECRET=<random secret string>
   ```

3. **Database Initialization**
   ```bash
   python seed_comprehensive_with_managers.py
   ```

4. **Access Your App**
   - Development: `https://<your-repl>.replit.dev`
   - Production: Custom domain can be configured

### Important Notes

- **Port 5000**: Application runs on port 5000 (configured for Replit)
- **Auto-restart**: Workflows restart automatically after deployment
- **Persistent Storage**: Database is persistent across deployments
- **File Uploads**: Stored in `app/static/uploads` (persistent)

---

## Docker Deployment

**Note**: Docker is NOT supported in Replit environment. Use this for deployment on other platforms.

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Quick Start with Docker Compose

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd magazine-task-management
   ```

2. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database**
   ```bash
   docker-compose exec web python seed_comprehensive_with_managers.py
   ```

5. **Access application**
   - URL: http://localhost:5000

### Docker Commands

```bash
# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Database backup
docker-compose exec db pg_dump -U magazine_user magazine_app > backup.sql
```

---

## Manual Deployment

For deployment on traditional servers (Linux/Ubuntu).

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- nginx (recommended)

### Installation Steps

1. **Install system dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3.11-venv python3-pip postgresql nginx
   ```

2. **Create application user**
   ```bash
   sudo useradd -m -s /bin/bash magazine_app
   sudo su - magazine_app
   ```

3. **Clone and setup**
   ```bash
   git clone <your-repo-url> ~/app
   cd ~/app
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE magazine_app;
   CREATE USER magazine_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE magazine_app TO magazine_user;
   \q
   ```

5. **Set environment variables**
   ```bash
   export DATABASE_URL="postgresql://magazine_user:your_password@localhost/magazine_app"
   export SESSION_SECRET="your-random-secret-key"
   ```

6. **Initialize database**
   ```bash
   python seed_comprehensive_with_managers.py
   ```

7. **Create systemd service**
   ```bash
   sudo nano /etc/systemd/system/magazine-app.service
   ```
   
   ```ini
   [Unit]
   Description=Magazine Task Management System
   After=network.target postgresql.service

   [Service]
   User=magazine_app
   WorkingDirectory=/home/magazine_app/app
   Environment="DATABASE_URL=postgresql://magazine_user:password@localhost/magazine_app"
   Environment="SESSION_SECRET=your-secret-key"
   ExecStart=/home/magazine_app/app/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable magazine-app
   sudo systemctl start magazine-app
   ```

9. **Configure nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/magazine-app
   ```
   
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           client_max_body_size 50M;
       }

       location /static {
           alias /home/magazine_app/app/app/static;
           expires 30d;
       }
   }
   ```

10. **Enable nginx site**
    ```bash
    sudo ln -s /etc/nginx/sites-available/magazine-app /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    ```

---

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SESSION_SECRET` | Secret key for sessions | `random-secret-key-change-in-production` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `production` |
| `MAX_CONTENT_LENGTH` | Max upload size (bytes) | `52428800` (50MB) |

---

## Database Setup

### Create Database Manually

```sql
CREATE DATABASE magazine_app;
```

### Run Migrations

```bash
# If using migrations
python -m flask db upgrade
```

### Seed Test Data

```bash
python seed_comprehensive_with_managers.py
```

This creates:
- 14 test users across all departments
- 5 brands with 30 editions
- 28 sample tasks
- 10 CXO articles

### Database Backup

```bash
# PostgreSQL backup
pg_dump -U magazine_user magazine_app > backup_$(date +%Y%m%d).sql

# Restore
psql -U magazine_user magazine_app < backup_20231121.sql
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

### Database Connection Error
- Verify DATABASE_URL is correct
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Test connection: `psql $DATABASE_URL`

### File Upload Errors
- Check permissions on `app/static/uploads`
- Ensure directory exists: `mkdir -p app/static/uploads`

### Application Won't Start
- Check logs: `journalctl -u magazine-app -f`
- Verify Python version: `python --version` (should be 3.11+)
- Check dependencies: `pip list`

---

## Security Checklist

- [ ] Change SESSION_SECRET from default value
- [ ] Use strong database password
- [ ] Enable HTTPS (use Let's Encrypt with nginx)
- [ ] Configure firewall (ufw/iptables)
- [ ] Regular database backups
- [ ] Keep dependencies updated
- [ ] Monitor application logs
- [ ] Restrict database access to localhost
- [ ] Use environment variables (never commit secrets)

---

## Performance Optimization

### For Production

1. **Use gunicorn workers**
   ```bash
   gunicorn --workers 4 --threads 2 --bind 0.0.0.0:5000 main:app
   ```

2. **Enable nginx caching**
   ```nginx
   proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;
   ```

3. **Database optimization**
   - Add indexes on frequently queried columns
   - Regular VACUUM and ANALYZE

4. **Static file serving**
   - Serve static files through nginx
   - Enable gzip compression

---

## Monitoring

### Application Logs
```bash
# Systemd service
journalctl -u magazine-app -f

# Docker
docker-compose logs -f web

# Direct output
tail -f /var/log/magazine-app/app.log
```

### Database Health
```sql
-- Connection count
SELECT count(*) FROM pg_stat_activity;

-- Slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

---

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx/HAProxy)
- Shared PostgreSQL database
- Shared file storage (S3/NFS) for uploads
- Session store (Redis) for multi-server setup

### Vertical Scaling
- Increase gunicorn workers
- Upgrade PostgreSQL resources
- Add database read replicas

---

## Support

For issues and questions:
- Check logs first
- Review this documentation
- Contact system administrator

---

**Last Updated**: November 2025
**Version**: 1.0.0
