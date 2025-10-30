# 🚀 DEPLOYMENT CHECKLIST

Use this checklist while deploying ScriptMyIdeas.

---

## 📋 PREPARATION

- [ ] GitHub account ready
- [ ] Code pushed to repository
- [ ] Back4app account created
- [ ] Back4app credentials available:
  - [ ] Application ID
  - [ ] REST API Key
  - [ ] JavaScript Key

---

## 🔧 PART 1: RAILWAY (Backend)

- [ ] Go to https://railway.app
- [ ] Sign in with GitHub
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select `Nish-H/PowerOps` repository
- [ ] Click on deployed service
- [ ] Go to Settings → Deploy section
  - [ ] Set Root Directory: `backend`
  - [ ] Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Go to Variables tab
- [ ] Add all 8 environment variables:
  - [ ] BACK4APP_APPLICATION_ID
  - [ ] BACK4APP_REST_API_KEY
  - [ ] BACK4APP_JAVASCRIPT_KEY
  - [ ] BACK4APP_SERVER_URL = `https://parseapi.back4app.com`
  - [ ] ENVIRONMENT = `production`
  - [ ] DEBUG = `False`
  - [ ] SECRET_KEY = (random 32+ character string)
  - [ ] CORS_ORIGINS = `*` (update later)
- [ ] Wait for deployment to complete
- [ ] Go to Settings → Networking
  - [ ] Click "Generate Domain"
  - [ ] **COPY AND SAVE RAILWAY URL:** _______________________
- [ ] Test backend health: `https://YOUR-RAILWAY-URL/health`
  - [ ] Shows: `{"status":"healthy"}`

---

## 🎨 PART 2: VERCEL (Frontend)

- [ ] Go to https://vercel.com
- [ ] Sign in with GitHub
- [ ] Click "Add New" → "Project"
- [ ] Select `Nish-H/PowerOps` repository
- [ ] Click "Import"
- [ ] Configure settings:
  - [ ] Framework: Vite
  - [ ] Root Directory: `frontend`
  - [ ] Build Command: `npm run build`
  - [ ] Output Directory: `dist`
- [ ] Add Environment Variable:
  - [ ] Name: `VITE_API_URL`
  - [ ] Value: (Your Railway URL from above)
- [ ] Click "Deploy"
- [ ] Wait for deployment (2-3 minutes)
- [ ] **COPY AND SAVE VERCEL URL:** _______________________
- [ ] Click "Visit" to see your site

---

## 🔐 PART 3: UPDATE CORS

- [ ] Go back to Railway dashboard
- [ ] Click on your service → Variables
- [ ] Find `CORS_ORIGINS` variable
- [ ] Update value to your Vercel URL (e.g., `https://yourapp.vercel.app`)
- [ ] Wait for automatic redeployment (~2 minutes)
- [ ] Deployment status shows "SUCCESS"

---

## ✅ PART 4: TESTING

- [ ] Open Vercel URL in browser
- [ ] Dashboard loads successfully
- [ ] Statistics show (even if 0)
- [ ] Click "Create New Script"
- [ ] Fill in test script:
  - [ ] Name: `test.py`
  - [ ] Language: Python
  - [ ] Code: `print("Hello!")`
- [ ] Click "Create Script"
- [ ] Success message appears
- [ ] Script appears in dashboard
- [ ] Click on script to view details
- [ ] Can edit script
- [ ] Search functionality works
- [ ] View API docs: `https://YOUR-RAILWAY-URL/api/docs`

---

## 🎉 SUCCESS!

- [ ] All tests passed
- [ ] Frontend URL saved: _______________________
- [ ] Backend URL saved: _______________________
- [ ] Bookmark both URLs
- [ ] Platform is LIVE!

---

## 📝 YOUR DEPLOYMENT URLS

Fill these in once deployed:

**Frontend (Web App):**
`https://________________________________`

**Backend API:**
`https://________________________________`

**API Documentation:**
`https://________________________________/api/docs`

---

## ⚠️ IF SOMETHING FAILS

**CORS Errors:**
- [ ] Check Railway CORS_ORIGINS matches Vercel URL exactly
- [ ] Wait 2-3 min for Railway redeploy
- [ ] Hard refresh browser (Ctrl+Shift+R)

**Backend 500 Errors:**
- [ ] Check Railway deployment logs
- [ ] Verify Back4app credentials
- [ ] Test: `https://YOUR-RAILWAY-URL/health`

**Frontend Blank:**
- [ ] Check Vercel function logs
- [ ] Verify VITE_API_URL is set
- [ ] Redeploy from Vercel dashboard

**Can't Create Scripts:**
- [ ] Check Railway logs
- [ ] Verify Back4app connection
- [ ] Test API docs: `/api/docs`

---

**TIME TO COMPLETE:** 10-15 minutes
**COST:** $0 (Free tier)

Good luck! 🚀
