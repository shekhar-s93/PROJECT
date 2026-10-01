# AWS EC2 Deployment Guide

## Goal
Deploy the complete application on an EC2 Linux server.

> Use the AWS account, region, instance size, and security rules approved by your instructor. AWS pricing/free-tier eligibility can change. Terminate classroom resources when finished.

## 1. Launch EC2
1. Open AWS Console → EC2 → Launch instance.
2. Use the Ubuntu AMI and small instance type approved for class.
3. Select/create the class-approved key pair.
4. Security group: allow SSH (22) only from the approved source and HTTP (80) from the intended users.
5. Launch.

## 2. Connect and install software
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx git
```

Copy/clone this project:
```bash
git clone YOUR_REPOSITORY_URL
cd student-performance-predictor
```

## 3. Install and train
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ml/train_model.py
```

## 4. Test Flask
```bash
python backend/app.py
```
The app listens on port 5000. For a temporary test, you can allow TCP/5000 in the security group and visit:
`http://EC2_PUBLIC_IP:5000`

Stop with Ctrl+C.

## 5. Recommended deployment: Gunicorn + Nginx
```bash
pip install gunicorn
gunicorn --bind 127.0.0.1:5000 backend.app:app
```
In another SSH session:
```bash
sudo nano /etc/nginx/sites-available/student-app
```
Paste:
```nginx
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Enable:
```bash
sudo ln -s /etc/nginx/sites-available/student-app /etc/nginx/sites-enabled/student-app
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```
Open `http://EC2_PUBLIC_IP`.

## 6. Keep it running after logout
Create:
```bash
sudo nano /etc/systemd/system/student-predictor.service
```
Use:
```ini
[Unit]
Description=Student Performance Predictor
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/student-performance-predictor
Environment="PATH=/home/ubuntu/student-performance-predictor/.venv/bin"
ExecStart=/home/ubuntu/student-performance-predictor/.venv/bin/gunicorn --bind 127.0.0.1:5000 backend.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```
If your username/path differs, change those values.

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now student-predictor
sudo systemctl status student-predictor
sudo systemctl status nginx
```

## Troubleshooting
**Cannot connect:** verify instance is running and HTTP/80 is allowed.
**502 Bad Gateway:** check `sudo systemctl status student-predictor` and `sudo journalctl -u student-predictor -n 50 --no-pager`.
**Nginx error:** run `sudo nginx -t`.

## Cleanup
Terminate the EC2 instance after class and remove unused resources created for the lab. Check the AWS billing/cost page if required.

## Teaching checkpoints
- Frontend: collects input.
- API: `/predict` receives JSON.
- Flask: calls the ML model.
- ML model: produces a prediction.
- EC2: runs the application.
- Nginx: receives web traffic and forwards it to Flask/Gunicorn.
