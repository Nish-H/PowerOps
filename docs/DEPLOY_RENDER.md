# 🚀 Deploy to Render.com (Free Railway Alternative)

**Time Required:** 5-10 minutes
**Cost:** $0 (Free tier - 750 hours/month)

---

## Why Render?

- ✅ **750 hours/month FREE** - More than enough to run 24/7
- ✅ **No credit card required**
- ✅ **Same workflow as Railway**
- ✅ **Auto-deploys from GitHub**
- ✅ **Free HTTPS/SSL**

### Note on Free Tier:
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30-50 seconds to wake up
- Subsequent requests are instant
- **Perfect for development and personal projects!**

---

## 🎯 Step-by-Step Deployment

### Step 1: Create Render Account (2 minutes)

1. Go to https://render.com
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Click **"Authorize Render"** when prompted
5. Complete signup (no credit card needed!)

### Step 2: Create New Web Service (1 minute)

1. On Render Dashboard, click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect account"** to link GitHub (if not already connected)
4. Find and select **`Nish-H/PowerOps`** repository
5. Click **"Connect"**

### Step 3: Configure Service (3 minutes)

Fill in these settings on the configuration page:

**Basic Settings:**
- **Name:** `scriptmyideas-backend` (or your preferred name)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt, Singapore)
- **Branch:** `main` (or your default branch)
- **Root Directory:** `backend`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Plan:**
- Select **"Free"** plan (should be selected by default)

### Step 4: Add Environment Variables (3 minutes)

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**.

Add these variables one by one:

```
BACK4APP_APPLICATION_ID
```
Value: Your Back4app Application ID

```
BACK4APP_REST_API_KEY
```
Value: Your Back4app REST API Key

```
BACK4APP_JAVASCRIPT_KEY
```
Value: Your Back4app JavaScript Key

```
BACK4APP_SERVER_URL
```
Value: `https://parseapi.back4app.com`

```
ENVIRONMENT
```
Value: `production`

```
DEBUG
```
Value: `False`

```
SECRET_KEY
```
Value: Any random 32+ character string (e.g., `scriptmyideas-prod-secret-key-2025-change-me-to-random`)

```
CORS_ORIGINS
```
Value: `*` (we'll update this after deploying frontend)

```
PYTHON_VERSION
```
Value: `3.10.13`

### Step 5: Deploy! (2 minutes)

1. Click **"Create Web Service"** button at the bottom
2. Render will start building and deploying
3. Watch the build logs in real-time
4. Wait for status to show **"Live"** with green checkmark (2-3 minutes)

### Step 6: Get Your Backend URL

1. Once deployed, you'll see your service URL at the top
2. It will look like: `https://scriptmyideas-backend.onrender.com`
3. **COPY AND SAVE THIS URL** - you need it for Vercel!

### Step 7: Test Backend

1. Open a new tab
2. Go to: `https://your-service-name.onrender.com/health`
3. You should see: `{"status":"healthy","service":"ScriptMyIdeas Backend"}`
4. ✅ If you see this, backend is working!

**Note:** First request might take 30-50 seconds if service was sleeping. This is normal for free tier!

---

## 🎨 Now Deploy Frontend to Vercel

Follow the same Vercel steps from before, but use your **Render URL** instead:

### Quick Vercel Steps:

1. Go to https://vercel.com → Sign in with GitHub
2. **"Add New"** → **"Project"** → Import `Nish-H/PowerOps`
3. Settings:
   - Root Directory: `frontend`
   - Framework: Vite
4. Add Environment Variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-service-name.onrender.com` (your Render URL)
5. Click **"Deploy"**
6. Wait 2-3 minutes
7. **COPY YOUR VERCEL URL**

---

## 🔐 Update CORS Settings

After getting your Vercel URL:

1. Go back to **Render Dashboard**
2. Click on your web service
3. Go to **"Environment"** tab
4. Find `CORS_ORIGINS` variable
5. Click **"Edit"** (pencil icon)
6. Change value from `*` to your Vercel URL: `https://your-app.vercel.app`
7. Click **"Save Changes"**
8. Service will automatically redeploy (2-3 minutes)

---

## ✅ Test Your Live App!

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Dashboard should load
3. Create a test script
4. Success! 🎉

### If First Load is Slow:
- This is normal! Free tier services sleep after 15 min inactivity
- First request wakes up the service (~30-50 seconds)
- After wake-up, everything is fast!
- Consider using a service like [UptimeRobot](https://uptimerobot.com) (free) to ping your backend every 5 minutes to keep it awake

---

## 🎯 Your Live URLs

**Frontend:** `https://your-app.vercel.app`
**Backend:** `https://your-service.onrender.com`
**API Docs:** `https://your-service.onrender.com/api/docs`

---

## 🔧 Troubleshooting

### Service won't start?
- Check build logs in Render dashboard
- Verify all environment variables are set
- Check that `backend/requirements.txt` exists

### CORS errors?
- Verify `CORS_ORIGINS` matches your Vercel URL exactly
- Wait 2-3 minutes for service to redeploy
- Hard refresh browser (Ctrl+Shift+R)

### Slow to respond?
- Normal for free tier! Service sleeps after 15 min
- First request wakes it up (~30-50 sec)
- Use UptimeRobot to keep it awake if needed

### 500 errors?
- Check Render logs (Logs tab in dashboard)
- Verify Back4app credentials
- Test health endpoint first

---

## 💰 Render Free Tier Limits

- **750 hours/month** - Enough for 24/7 operation (720 hours)
- **512 MB RAM** - Sufficient for our app
- **100 GB bandwidth/month** - More than enough
- **Services sleep after 15 min** inactivity
- **No credit card required**

**Perfect for personal projects!** 🎉

---

## 🚀 Keeping Service Awake (Optional)

If you don't want the 30-second wake-up delay:

### Option 1: UptimeRobot (Free)
1. Sign up at https://uptimerobot.com
2. Add new monitor
3. URL: `https://your-service.onrender.com/health`
4. Check interval: 5 minutes
5. Your service stays awake!

### Option 2: Upgrade to Paid ($7/month)
- No sleeping
- Always instant
- More RAM
- Only if you need production reliability

---

## 📊 Advantages over Railway

| Feature | Render Free | Railway Free |
|---------|------------|--------------|
| Monthly hours | 750 | 500 |
| Credit required | ❌ No | ✅ Yes |
| Auto-sleep | ✅ Yes (15 min) | ❌ No |
| Build time | Fast | Fast |
| Deployment | Auto | Auto |

**Render is actually better for free tier!** 🎉

---

## ✨ Success!

Your ScriptMyIdeas platform is now running on **100% free infrastructure**:
- ✅ Render (Backend) - Free
- ✅ Vercel (Frontend) - Free
- ✅ Back4app (Database) - Free

**Total Cost: $0/month** 🎊
