# Google OAuth Setup with Supabase

## Prerequisites

1. ✅ Supabase project created
2. ✅ Supabase credentials added to `.env`
3. ✅ Google OAuth configured in Supabase

## Step 1: Configure Google OAuth in Supabase

1. Go to your Supabase project dashboard
2. Navigate to **Authentication** → **Providers**
3. Find **Google** in the list
4. Click **Enable**
5. You'll need:
   - **Google Client ID**
   - **Google Client Secret**

### Getting Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen (if not done)
6. Application type: **Web application**
7. Authorized redirect URIs:
   ```
   https://YOUR_PROJECT_REF.supabase.co/auth/v1/callback
   ```
   Replace `YOUR_PROJECT_REF` with your Supabase project reference ID
8. Copy **Client ID** and **Client Secret**
9. Add them to Supabase Google provider settings

## Step 2: Update Environment Variables

Your `.env` file should already have:
```bash
SUPABASE_PROJECT_URL=https://mrnlqzxvlpjjrjnxngpk.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

## Step 3: Install Dependencies

The `supabase` Python package has been added to `requirements.txt`. Rebuild the backend:

```powershell
docker-compose build backend
docker-compose restart backend
```

## Step 4: Test Google OAuth

1. **Start the application:**
   ```powershell
   docker-compose up -d
   ```

2. **Visit the login page:**
   - Go to http://localhost:3000/login
   - Click **"Continue with Google"** button

3. **OAuth Flow:**
   - You'll be redirected to Google
   - Sign in with your Google account
   - Grant permissions
   - You'll be redirected back to `/auth/callback`
   - The app will automatically create your account and log you in

## How It Works

1. **User clicks "Continue with Google"**
   - Frontend calls `/api/v1/auth/oauth/google/url`
   - Backend generates OAuth URL using Supabase
   - User is redirected to Google

2. **Google OAuth**
   - User authenticates with Google
   - Google redirects to Supabase callback
   - Supabase exchanges code for session

3. **Callback Handling**
   - Frontend receives callback at `/auth/callback`
   - Calls `/api/v1/auth/oauth/google/callback` with code
   - Backend exchanges code for user info
   - Creates user in database (if new)
   - Returns JWT token

4. **User Logged In**
   - Token stored in localStorage
   - User redirected to `/feed`

## Troubleshooting

### Issue: "Google OAuth not configured"

**Solution:**
- Check Supabase credentials in `.env`
- Verify `SUPABASE_PROJECT_URL` and `SUPABASE_ANON_KEY` are set
- Restart backend: `docker-compose restart backend`

### Issue: "Invalid OAuth code"

**Solution:**
- Check redirect URI matches in Google Cloud Console
- Verify Supabase callback URL is correct
- Make sure Google provider is enabled in Supabase

### Issue: OAuth redirects but fails

**Solution:**
- Check browser console for errors
- Verify callback route is registered in `App.jsx`
- Check backend logs: `docker-compose logs backend`

## Security Notes

- ✅ OAuth tokens are handled securely by Supabase
- ✅ User passwords are not stored for OAuth users
- ✅ JWT tokens are used for session management
- ✅ OAuth users can still enable MFA if desired

## Next Steps

After setting up Google OAuth:
1. Test the flow end-to-end
2. Verify user creation in database
3. Test login with existing OAuth users
4. Consider adding other providers (GitHub, Facebook, etc.)
