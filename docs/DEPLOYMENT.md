# Deployment Guide - ScriptMyIdeas

This guide will help you deploy ScriptMyIdeas to production with Vercel (frontend) and Railway (backend).

## Prerequisites

1. **GitHub Account** - Your code is already pushed
2. **Vercel Account** - Sign up at https://vercel.com (free tier available)
3. **Railway Account** - Sign up at https://railway.app (free tier available)
4. **Back4app Account** - Already set up from BACK4APP_SETUP.md

## Deployment Steps

### Step 1: Deploy Backend to Railway

#### Option A: Using Railway Dashboard (Recommended)

1. **Go to Railway**: https://railway.app
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Connect your GitHub account** if not already connected
5. **Select repository**: `Nish-H/PowerOps` (or ScriptMyIdeas)
6. **Railway will detect the project automatically**

7. **Configure Environment Variables**:
   Click on your service → Variables → Add variables:
   ```
   BACK4APP_APPLICATION_ID=your_application_id
   BACK4APP_REST_API_KEY=your_rest_api_key
   BACK4APP_JAVASCRIPT_KEY=your_javascript_key
   BACK4APP_SERVER_URL=https://parseapi.back4app.com
   ENVIRONMENT=production
   DEBUG=False
   SECRET_KEY=generate-a-strong-random-key-here
   CORS_ORIGINS=https://your-app.vercel.app
   ```

8. **Configure Start Command**:
   - Go to Settings → Deploy
   - Root Directory: `/backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

9. **Deploy**: Click "Deploy" and wait for deployment to complete

10. **Get Backend URL**: Copy the Railway URL (e.g., `https://scriptmyideas-production.up.railway.app`)

#### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Add environment variables
railway variables set BACK4APP_APPLICATION_ID=your_app_id
railway variables set BACK4APP_REST_API_KEY=your_api_key
# ... add all other variables

# Deploy
railway up
```

### Step 2: Deploy Frontend to Vercel

#### Option A: Using Vercel Dashboard (Easiest)

1. **Go to Vercel**: https://vercel.com/dashboard
2. **Click "Add New" → "Project"**
3. **Import Git Repository**:
   - Connect GitHub if not connected
   - Select `Nish-H/PowerOps` repository
   - Click "Import"

4. **Configure Project**:
   - Framework Preset: **Vite**
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

5. **Add Environment Variables**:
   Click "Environment Variables" and add:
   ```
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   ```
   (Use the Railway URL from Step 1)

6. **Deploy**: Click "Deploy"

7. **Get Frontend URL**: After deployment, copy your Vercel URL (e.g., `https://scriptmyideas.vercel.app`)

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod

# Set environment variable
vercel env add VITE_API_URL
# Enter: https://your-railway-backend-url.up.railway.app
# Select: Production

# Redeploy to use new env variable
vercel --prod
```

### Step 3: Update Backend CORS Settings

After getting your Vercel URL, update the Railway backend environment variables:

1. Go to Railway → Your Service → Variables
2. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://www.your-app.vercel.app
   ```
3. Railway will automatically redeploy

### Step 4: Test Your Deployment

1. **Visit your Vercel URL**: `https://your-app.vercel.app`
2. **Test the dashboard** - Should load without errors
3. **Create a test script** - Verify backend connectivity
4. **Check API docs**: `https://your-railway-url.up.railway.app/api/docs`

## Quick Deploy Commands

### One-Click Deploy to Vercel (Frontend)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Nish-H/PowerOps&root-directory=frontend&env=VITE_API_URL&envDescription=Backend%20API%20URL&project-name=scriptmyideas&repository-name=scriptmyideas)

### One-Click Deploy to Railway (Backend)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/scriptmyideas?referralCode=YOUR_CODE)

## Custom Domain Setup

### For Vercel (Frontend):
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

### For Railway (Backend):
1. Go to Service Settings → Networking
2. Click "Generate Domain" or add custom domain
3. Update frontend `VITE_API_URL` with new domain

## Environment Variables Summary

### Backend (Railway)
```env
BACK4APP_APPLICATION_ID=xxx
BACK4APP_REST_API_KEY=xxx
BACK4APP_JAVASCRIPT_KEY=xxx
BACK4APP_SERVER_URL=https://parseapi.back4app.com
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-secret-key-min-32-chars
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

### Frontend (Vercel)
```env
VITE_API_URL=https://your-railway-backend.up.railway.app
```

## Monitoring & Logs

### Railway (Backend Logs)
- Dashboard → Service → Deployments → View Logs
- Or use: `railway logs`

### Vercel (Frontend Logs)
- Dashboard → Project → Deployments → Function Logs

## Troubleshooting

### CORS Errors
- Ensure backend `CORS_ORIGINS` includes your Vercel URL
- Check Railway logs for detailed error messages

### API Connection Failed
- Verify `VITE_API_URL` in Vercel environment variables
- Test backend directly: `https://your-railway-url.up.railway.app/health`

### Build Failures
- Check build logs in Vercel/Railway dashboard
- Verify all dependencies are in package.json/requirements.txt

## Cost Estimation

### Free Tier Limits:
- **Vercel**: Unlimited personal projects, 100GB bandwidth
- **Railway**: $5 free credit monthly, ~550 hours runtime
- **Back4app**: 25k requests/month, 1GB storage

For most use cases, this will be **completely free**!

## Updating Your Deployment

### Automatic Deployments:
Both Vercel and Railway will automatically redeploy when you push to your main branch on GitHub.

### Manual Redeployment:
```bash
# Frontend
cd frontend && vercel --prod

# Backend
railway up
```

## Next Steps

After deployment:
1. Set up custom domain (optional)
2. Configure authentication (optional)
3. Set up monitoring/alerts
4. Add analytics (optional)

## Support

- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- Back4app: https://www.back4app.com/docs

Your live URLs will be:
- **Frontend**: `https://your-project-name.vercel.app`
- **Backend**: `https://your-project-name.up.railway.app`
- **API Docs**: `https://your-project-name.up.railway.app/api/docs`
