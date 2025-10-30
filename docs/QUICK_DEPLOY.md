# 🚀 Quick Deploy Guide - Get ScriptMyIdeas Live in 10 Minutes!

Follow these steps to get your ScriptMyIdeas platform live and accessible via a public URL.

## Prerequisites (2 minutes)

1. ✅ GitHub account (you already have this)
2. ✅ Code is already pushed to your repository
3. 📝 Back4app credentials from [BACK4APP_SETUP.md](./BACK4APP_SETUP.md)

## Step 1: Deploy Backend to Railway (5 minutes)

### 1.1 Sign Up for Railway
1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

### 1.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **`Nish-H/PowerOps`** (or your repo name)
4. Railway will automatically detect and start building

### 1.3 Configure Environment Variables
1. Click on your deployed service
2. Go to **"Variables"** tab
3. Click **"Add Variable"** and add these (one by one):

```
BACK4APP_APPLICATION_ID=your_application_id_here
BACK4APP_REST_API_KEY=your_rest_api_key_here
BACK4APP_JAVASCRIPT_KEY=your_javascript_key_here
BACK4APP_SERVER_URL=https://parseapi.back4app.com
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=use-a-long-random-string-min-32-characters-change-this
CORS_ORIGINS=*
```

**Note:** We'll update CORS_ORIGINS after deploying the frontend

### 1.4 Configure Deployment Settings
1. Go to **"Settings"** tab
2. Under **"Deploy"** section:
   - Root Directory: `/backend`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 1.5 Get Your Backend URL
1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy the URL (something like: `https://scriptmyideas-production-xxxx.up.railway.app`)
4. **SAVE THIS URL** - you'll need it for the frontend!

## Step 2: Deploy Frontend to Vercel (3 minutes)

### 2.1 Sign Up for Vercel
1. Go to https://vercel.com
2. Click **"Sign Up"** → **"Continue with GitHub"**
3. Authorize Vercel

### 2.2 Import Your Project
1. Click **"Add New..."** → **"Project"**
2. Find and select **`Nish-H/PowerOps`** (or your repo)
3. Click **"Import"**

### 2.3 Configure Build Settings
Configure these settings:
- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

### 2.4 Add Environment Variable
1. Expand **"Environment Variables"**
2. Add this variable:
   - **Name:** `VITE_API_URL`
   - **Value:** Your Railway backend URL from Step 1.5 (e.g., `https://scriptmyideas-production-xxxx.up.railway.app`)

### 2.5 Deploy!
1. Click **"Deploy"**
2. Wait 2-3 minutes for build to complete
3. Once done, click **"Visit"** to see your live site!
4. **COPY YOUR VERCEL URL** (e.g., `https://scriptmyideas.vercel.app`)

## Step 3: Update CORS Settings (1 minute)

Now that you have your frontend URL, update the backend to allow requests from it:

1. Go back to **Railway Dashboard**
2. Click on your service → **"Variables"**
3. Find `CORS_ORIGINS` and update it to your Vercel URL:
   ```
   CORS_ORIGINS=https://your-vercel-url.vercel.app
   ```
4. Railway will automatically redeploy (takes ~2 minutes)

## Step 4: Test Your Live App! 🎉

1. **Visit your Vercel URL:** `https://your-app.vercel.app`
2. **You should see the ScriptMyIdeas dashboard!**
3. **Test creating a script:**
   - Click "New Script"
   - Add some code
   - Save it
4. **Verify it's working:**
   - Check if the script appears in your dashboard
   - Try the search functionality

## Your Live URLs

After deployment, you'll have:

- **Frontend (Web App):** `https://your-project.vercel.app`
- **Backend API:** `https://your-project.up.railway.app`
- **API Documentation:** `https://your-project.up.railway.app/api/docs`

## Troubleshooting

### ❌ "Failed to fetch" or CORS errors
- **Solution:** Make sure you updated `CORS_ORIGINS` in Railway with your exact Vercel URL (including https://)
- Wait 2-3 minutes for Railway to redeploy

### ❌ Backend shows 500 errors
- **Solution:** Check Railway logs (Dashboard → Deployments → View Logs)
- Verify all Back4app credentials are correct
- Make sure Back4app is accessible (test at https://dashboard.back4app.com)

### ❌ Frontend shows blank page
- **Solution:** Check Vercel deployment logs
- Verify `VITE_API_URL` environment variable is set correctly
- Try redeploying: Vercel Dashboard → Deployments → ⋮ → Redeploy

### ❌ Can't create scripts
- **Solution:**
  - Check if backend is running: Visit `https://your-railway-url.up.railway.app/health`
  - Verify Back4app credentials in Railway
  - Check Railway logs for errors

## What's Next?

### Optional Improvements:

1. **Custom Domain:**
   - Vercel: Settings → Domains → Add Domain
   - Railway: Settings → Networking → Custom Domain

2. **Enable GitHub Auto-Deploy:**
   - Already configured! Any push to your `main` branch will auto-deploy

3. **Monitor Usage:**
   - Railway: Dashboard → Metrics
   - Vercel: Dashboard → Analytics

## Cost

Both services offer generous free tiers:
- **Vercel:** Free for personal projects
- **Railway:** $5 free credit per month (~550 hours)
- **Back4app:** 25k requests/month free

**You can run this completely FREE!** 🎉

## Need Help?

If you run into issues:
1. Check the full [DEPLOYMENT.md](./DEPLOYMENT.md) guide
2. Review Railway/Vercel logs
3. Verify all environment variables
4. Check Back4app dashboard for API limits

---

**Congratulations!** 🎊 Your ScriptMyIdeas platform is now live and accessible worldwide!

Share your URL: `https://your-app.vercel.app`
