# OSINT Investigation Tool - Cloud Deployment Guide

## 🚀 Deploy to Heroku (24x7 Access)

### Step 1: Install Heroku CLI
Download and install Heroku CLI from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login to Heroku
```bash
heroku login
```

### Step 3: Create Heroku App
```bash
heroku create your-osint-tool-name
```
(Replace `your-osint-tool-name` with a unique name)

### Step 4: Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 5: Deploy to Heroku
```bash
git push heroku main
```

### Step 6: Open Your App
```bash
heroku open
```

## 📱 Alternative: Deploy to Railway

### Step 1: Go to Railway.app
Visit: https://railway.app

### Step 2: Connect GitHub Repository
- Create account and connect your GitHub repo
- Railway will automatically detect Flask app

### Step 3: Deploy
Railway will deploy automatically when you push to GitHub

## 🔧 Alternative: Deploy to Render

### Step 1: Go to Render.com
Visit: https://render.com

### Step 2: Create Web Service
- Connect your GitHub repository
- Select Python environment
- Set build command: `pip install -r requirements.txt`
- Set start command: `python web_app.py`

### Step 3: Deploy
Render will provide a permanent URL

## 📋 Files Created for Deployment:
- ✅ `Procfile` - Tells Heroku how to run the app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `.gitignore` - Excludes unnecessary files
- ✅ Modified `web_app.py` - Works with cloud environments

## 🌐 Your App URLs:
- **Local**: http://localhost:5000
- **Heroku**: https://your-app-name.herokuapp.com
- **Railway**: https://your-project-name.up.railway.app
- **Render**: https://your-service-name.onrender.com

## 📱 Mobile Access:
Once deployed, you can access your OSINT tool from any device:
- 📱 Mobile phones
- 💻 Tablets
- 🖥️ Any computer
- 🌐 Any web browser

## 🔒 Security Note:
The deployed app will be publicly accessible. Consider adding authentication if you need to restrict access.

## 🆘 Troubleshooting:
- If deployment fails, check Heroku logs: `heroku logs --tail`
- Make sure all dependencies are in `requirements.txt`
- Ensure `Procfile` and `runtime.txt` are correct

## 🎉 Success!
Your OSINT Investigation Tool is now available 24/7 from anywhere! 🚀