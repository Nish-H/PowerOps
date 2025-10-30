# 🚀 ScriptMyIdeas - Step-by-Step Deployment Guide

**Architecture:** Back4app (Database) + Railway (Backend API) + Vercel (Frontend)

**Time Required:** 10-15 minutes
**Cost:** $0 (Free tier on all services)

---

## ✅ Pre-Deployment Checklist

Before starting, make sure you have:
- [ ] GitHub account with access to `Nish-H/PowerOps` repository
- [ ] Back4app account created
- [ ] Back4app app created (follow [BACK4APP_SETUP.md](./BACK4APP_SETUP.md) if not done)
- [ ] Back4app credentials handy:
  - Application ID
  - REST API Key
  - JavaScript Key

---

## 🎯 PART 1: Deploy Backend to Railway (5 minutes)

### Step 1.1: Create Railway Account

1. Open https://railway.app in a new tab
2. Click **"Login"**
3. Select **"Login with GitHub"**
4. Click **"Authorize Railway"** when prompted
5. Complete the Railway signup

### Step 1.2: Deploy Your Repository

1. On Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. If prompted, click **"Configure GitHub App"**
   - Select **"Only select repositories"**
   - Choose **`Nish-H/PowerOps`**
   - Click **"Install & Authorize"**
4. Back on Railway, select **`Nish-H/PowerOps`** from the list
5. Railway will start building automatically

### Step 1.3: Configure Build Settings

1. Click on the deployed service card (should show "Building...")
2. Click **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Set these values:
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **"Save"**

### Step 1.4: Add Environment Variables

1. Click **"Variables"** tab
2. Click **"+ New Variable"**
3. Add these variables one by one (click "+ New Variable" for each):

```
BACK4APP_APPLICATION_ID
```
Enter your Back4app Application ID (from Back4app dashboard)

```
BACK4APP_REST_API_KEY
```
Enter your Back4app REST API Key

```
BACK4APP_JAVASCRIPT_KEY
```
Enter your Back4app JavaScript Key

```
BACK4APP_SERVER_URL
```
Enter: `https://parseapi.back4app.com`

```
ENVIRONMENT
```
Enter: `production`

```
DEBUG
```
Enter: `False`

```
SECRET_KEY
```
Enter a random string (min 32 characters). You can use: `scriptmyideas-2025-production-secret-key-change-this-to-something-random`

```
CORS_ORIGINS
```
Enter: `*` (we'll update this after deploying frontend)

4. After adding all variables, Railway will automatically redeploy

### Step 1.5: Get Your Backend URL

1. Go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy the generated URL (e.g., `scriptmyideas-production-abcd.up.railway.app`)
5. **IMPORTANT: Save this URL!** Write it down or paste it somewhere - you need it for Step 2.4

### Step 1.6: Verify Backend is Running

1. Open a new tab
2. Go to: `https://YOUR-RAILWAY-URL.up.railway.app/health`
   (Replace with your actual Railway URL)
3. You should see: `{"status":"healthy","service":"ScriptMyIdeas Backend"}`
4. ✅ If you see this, backend is working!

---

## 🎨 PART 2: Deploy Frontend to Vercel (5 minutes)

### Step 2.1: Create Vercel Account

1. Open https://vercel.com in a new tab
2. Click **"Sign Up"**
3. Select **"Continue with GitHub"**
4. Click **"Authorize Vercel"** when prompted

### Step 2.2: Import Your Project

1. On Vercel dashboard, click **"Add New..."** → **"Project"**
2. You'll see "Import Git Repository"
3. Find **`Nish-H/PowerOps`** in the list
   - If you don't see it, click **"Adjust GitHub App Permissions"** and grant access
4. Click **"Import"** next to `Nish-H/PowerOps`

### Step 2.3: Configure Project Settings

On the "Configure Project" page, set these:

**Build and Output Settings:**
- Framework Preset: **Vite**
- Root Directory: **`frontend`** (click "Edit" to change)
- Build Command: `npm run build` (should be auto-filled)
- Output Directory: `dist` (should be auto-filled)
- Install Command: `npm install` (should be auto-filled)

### Step 2.4: Add Environment Variable

1. Expand **"Environment Variables"** section
2. Add this variable:
   - **NAME:** `VITE_API_URL`
   - **VALUE:** Your Railway URL from Step 1.5 (e.g., `https://scriptmyideas-production-abcd.up.railway.app`)
   - Make sure to include `https://` and NO trailing slash
3. Leave it set to "Production, Preview, and Development"

### Step 2.5: Deploy!

1. Click **"Deploy"** button
2. Wait 2-3 minutes while Vercel builds and deploys
3. You'll see a progress screen with logs
4. Once done, you'll see "Congratulations!" with confetti 🎉

### Step 2.6: Get Your Frontend URL

1. Click **"Continue to Dashboard"**
2. You'll see your project with a URL like: `scriptmyideas.vercel.app`
3. Click **"Visit"** to open your live site!
4. **IMPORTANT: Copy this URL!** You need it for Step 3

---

## 🔐 PART 3: Update CORS Settings (2 minutes)

Now we need to tell the backend to accept requests from your frontend URL.

### Step 3.1: Update Railway Environment Variable

1. Go back to **Railway Dashboard**
2. Click on your service
3. Click **"Variables"** tab
4. Find the `CORS_ORIGINS` variable
5. Click on it to edit
6. Change the value from `*` to your Vercel URL
   - Example: `https://scriptmyideas.vercel.app`
   - Make sure to use `https://` and NO trailing slash
7. The variable will auto-save

### Step 3.2: Wait for Redeployment

1. Railway will automatically redeploy with new settings
2. Click **"Deployments"** tab to watch progress
3. Wait ~2 minutes for the new deployment to be live
4. Status should show "SUCCESS" with a green checkmark

---

## 🎉 PART 4: Test Your Live Application!

### Step 4.1: Open Your Frontend

1. Go to your Vercel URL: `https://your-app.vercel.app`
2. You should see the **ScriptMyIdeas** dashboard!
3. Check that the statistics load (may show 0 if database is empty)

### Step 4.2: Create Your First Script

1. Click **"Create New Script"** or **"Scripts"** → **"New Script"**
2. Fill in the form:
   - **Name:** `test_script.py`
   - **Language:** Python
   - **Category:** Testing
   - **Description:** My first script on ScriptMyIdeas
   - **Code:**
     ```python
     print("Hello from ScriptMyIdeas!")
     ```
3. Click **"Create Script"**
4. You should see a success message!
5. The script should appear in your dashboard

### Step 4.3: Verify Everything Works

Test these features:
- [ ] Dashboard loads without errors
- [ ] Can create a new script
- [ ] Can view script details
- [ ] Can edit a script
- [ ] Can search for scripts
- [ ] Statistics show correct counts

---

## ✅ SUCCESS! Your URLs

Congratulations! ScriptMyIdeas is now live:

### Your Live URLs:
- **🌐 Frontend (Web App):** `https://your-app.vercel.app`
- **🔧 Backend API:** `https://your-backend.up.railway.app`
- **📚 API Documentation:** `https://your-backend.up.railway.app/api/docs`

### Save These URLs!
Write them down or bookmark them - these are your permanent URLs!

---

## 🔧 Troubleshooting

### ❌ Problem: "Failed to fetch" or CORS errors

**Solution:**
1. Go to Railway → Variables
2. Check that `CORS_ORIGINS` matches your Vercel URL exactly
3. Make sure it includes `https://` and has NO trailing slash
4. Wait 2-3 minutes for Railway to redeploy
5. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)

### ❌ Problem: Backend shows 500 errors

**Solution:**
1. Go to Railway → Deployments → Click latest deployment → View Logs
2. Look for errors related to Back4app
3. Verify all Back4app credentials are correct
4. Test Back4app directly: https://dashboard.back4app.com

### ❌ Problem: Frontend shows blank page

**Solution:**
1. Go to Vercel → Project → Deployments → Click latest → View Function Logs
2. Check if `VITE_API_URL` is set correctly
3. Try redeploying: Deployments → ⋮ (three dots) → Redeploy

### ❌ Problem: Can't create scripts / Database errors

**Solution:**
1. Check Railway logs for database connection errors
2. Verify Back4app credentials in Railway Variables
3. Test Backend health: `https://your-railway-url.up.railway.app/health`
4. Test API docs: `https://your-railway-url.up.railway.app/api/docs`

### ❌ Problem: Railway deployment failed

**Solution:**
1. Check Railway deployment logs
2. Verify Root Directory is set to `backend`
3. Verify Start Command is: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Check that all environment variables are set

---

## 🎯 Next Steps

### Customize Your Deployment

1. **Custom Domain (Optional):**
   - Vercel: Settings → Domains → Add
   - Railway: Settings → Networking → Custom Domain

2. **Enable Auto-Deploy:**
   - Already configured! Push to GitHub and it auto-deploys
   - Vercel: Auto-deploys on push to main branch
   - Railway: Auto-deploys on push to main branch

3. **Monitor Your App:**
   - Railway: Metrics tab shows CPU, memory, network
   - Vercel: Analytics tab shows visitor stats

4. **View Logs:**
   - Railway: Deployments → View Logs
   - Vercel: Deployments → Function Logs

### Using the Auto-Save API

To automatically save scripts from Claude conversations:

```bash
curl -X POST "https://your-railway-url.up.railway.app/api/integration/auto-save" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_script.py",
    "content": "print(\"Hello World\")",
    "description": "A simple test script",
    "language": "python",
    "tags": ["test", "auto-saved"]
  }'
```

---

## 💰 Costs & Limits

All services are **FREE** for your use case:

**Vercel Free Tier:**
- Unlimited personal projects
- 100GB bandwidth/month
- Automatic HTTPS
- Custom domains

**Railway Free Tier:**
- $5 credit/month
- ~550 hours runtime (always on for 23 days)
- Perfect for this project

**Back4app Free Tier:**
- 25,000 requests/month
- 1GB database storage
- 1GB file storage
- More than enough for personal use

**Total Cost: $0/month** 🎉

---

## 📞 Need Help?

If you get stuck:
1. Check the troubleshooting section above
2. Review Railway/Vercel deployment logs
3. Verify all environment variables are correct
4. Test each service independently (health endpoints)

---

## 🎊 Congratulations!

Your ScriptMyIdeas platform is now **LIVE** and accessible from anywhere in the world!

Share your creation: `https://your-app.vercel.app`

Happy scripting! 🚀
