# Back4app Database Setup Guide

This guide will help you set up the Back4app database for ScriptMyIdeas.

## Step 1: Create Back4app Account

1. Go to [https://www.back4app.com/](https://www.back4app.com/)
2. Sign up for a free account
3. Verify your email

## Step 2: Create a New App

1. Click "Build new app"
2. Choose "Backend as a Service"
3. Name your app "ScriptMyIdeas"
4. Select your preferred region
5. Click "Create"

## Step 3: Get API Credentials

1. Go to your app dashboard
2. Click on "App Settings" > "Security & Keys"
3. Copy the following credentials:
   - Application ID
   - REST API Key
   - JavaScript Key
   - Server URL (usually: `https://parseapi.back4app.com`)

## Step 4: Configure Backend

1. Copy `backend/.env.example` to `backend/.env`
2. Fill in the credentials:

```env
BACK4APP_APPLICATION_ID=your_application_id_here
BACK4APP_REST_API_KEY=your_rest_api_key_here
BACK4APP_JAVASCRIPT_KEY=your_javascript_key_here
BACK4APP_SERVER_URL=https://parseapi.back4app.com
```

## Step 5: Initialize Database Schema

The database schema will be created automatically when you first use the API endpoints. The following classes will be created:

### Script Class
- `name` (String)
- `description` (String)
- `language` (String)
- `content` (String)
- `version` (String)
- `category` (String)
- `tags` (Array)
- `createdBy` (String)
- `isLatest` (Boolean)
- `metadata` (Object)

### ScriptVersion Class
- `scriptId` (Pointer to Script)
- `versionNumber` (String)
- `content` (String)
- `changelog` (String)
- `createdBy` (String)
- `hash` (String)

### Artifact Class
- `scriptId` (Pointer to Script)
- `scriptVersion` (String)
- `name` (String)
- `type` (String)
- `content` (String)
- `fileUrl` (String)
- `size` (Number)
- `metadata` (Object)

## Step 6: Optional - Set Up Indexes

For better performance, add indexes in the Back4app dashboard:

1. Go to "Database" > "Browser"
2. For each class (Script, ScriptVersion, Artifact):
   - Click on the class
   - Go to "More" > "Add Index"
   - Add indexes on:
     - `createdAt` (descending)
     - `updatedAt` (descending)
     - For Script: `name`, `language`, `category`

## Step 7: Set Security Rules (Optional)

By default, Back4app allows read/write for all users. To secure your data:

1. Go to "Database" > "Browser"
2. Click on each class
3. Go to "Security" > "Class Level Permissions"
4. Configure as needed

## Testing the Connection

Once configured, start the backend server:

```bash
cd backend
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/api/docs` to test the API endpoints.

## Troubleshooting

### Connection Issues
- Verify your credentials are correct
- Check that the Server URL is `https://parseapi.back4app.com`
- Ensure your API keys haven't been regenerated

### CORS Errors
- Add your frontend URL to CORS settings in Back4app:
  - Go to "App Settings" > "Server Settings"
  - Add allowed origins: `http://localhost:3000`

### Rate Limiting
- Free tier has limits (30 requests/sec)
- Consider upgrading for production use

## Resources

- [Back4app Documentation](https://www.back4app.com/docs)
- [Parse Server REST API Guide](https://docs.parseplatform.org/rest/guide/)
- [Back4app Dashboard](https://dashboard.back4app.com/)
