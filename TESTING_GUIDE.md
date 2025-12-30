# 🧪 InstaIntelli Testing Guide

## 🚀 Quick Start Testing

### 1. **Seed Sample Posts (Like Instagram!)**

Run this to add fake posts to your feed:

```bash
# From project root
docker exec -it instaintelli_backend python -m scripts.seed_posts
```

Or if running locally:
```bash
cd backend
python -m scripts.seed_posts
```

**This will add 10 sample posts** with beautiful images from Unsplash, just like Instagram shows random posts to new users!

---

## 📋 **Complete Testing Checklist**

### ✅ **Authentication & User Management**

1. **Register New Account**
   - Go to: `http://localhost:3000/register`
   - Fill in: Username, Email, Password
   - Click "Sign Up"
   - ✅ Should redirect to `/feed`

2. **Login**
   - Go to: `http://localhost:3000/login`
   - Enter credentials
   - ✅ Should redirect to `/feed`

3. **Profile Page**
   - Click "Profile" in sidebar
   - ✅ Should see your profile info
   - ✅ Can update bio, profile image

4. **MFA Setup** (Optional)
   - Go to Profile → Security
   - Click "Enable MFA"
   - Scan QR code with Google Authenticator
   - ✅ MFA should be enabled

---

### ✅ **Feed & Posts**

1. **View Feed**
   - Go to: `http://localhost:3000/feed`
   - ✅ Should see posts (after seeding)
   - ✅ Posts should have images, captions, usernames

2. **Upload Post**
   - Click "Create" in sidebar or go to `/upload`
   - Select an image (JPG/PNG)
   - Add optional caption
   - Click "Upload"
   - ✅ Post should appear in feed

3. **View Post Details**
   - Click on any post
   - ✅ Should see full post details

---

### ✅ **Search & AI Features**

1. **Semantic Search**
   - Go to: `http://localhost:3000/search`
   - Type: "Show me posts about nature"
   - ✅ Should return relevant posts
   - ✅ Shows similarity scores

2. **AI Chat**
   - Go to: `http://localhost:3000/chat`
   - Ask: "What posts did I upload about travel?"
   - ✅ AI should respond with relevant posts
   - ✅ Shows referenced posts

---

### ✅ **UI/UX Features**

1. **Dark/Light Theme**
   - Click "Dark" toggle in sidebar
   - ✅ Theme should switch
   - ✅ Should persist on refresh

2. **Responsive Design**
   - Resize browser window
   - ✅ Layout should adapt
   - ✅ Mobile-friendly

3. **Animations**
   - Navigate between pages
   - ✅ Smooth transitions
   - ✅ Loading states

---

## 🎯 **Key Features to Test**

| Feature | How to Test | Expected Result |
|---------|-------------|------------------|
| **Registration** | Sign up with new account | Account created, redirected to feed |
| **Login** | Login with credentials | Successfully logged in |
| **Feed** | View `/feed` page | See posts (after seeding) |
| **Upload** | Upload image post | Post appears in feed |
| **Search** | Search for "nature posts" | Relevant results with AI matching |
| **Chat** | Ask AI about posts | Get intelligent responses |
| **Profile** | View/edit profile | Profile updates saved |
| **MFA** | Enable 2FA | QR code, TOTP working |
| **Theme** | Toggle dark/light | Theme switches smoothly |

---

## 🐛 **Troubleshooting**

### **Feed is Empty?**
```bash
# Seed sample posts
docker exec -it instaintelli_backend python -m scripts.seed_posts
```

### **Can't Upload Posts?**
- Check MinIO is running: `docker-compose ps minio`
- Check backend logs: `docker-compose logs backend`

### **Search Not Working?**
- Check OpenAI API key in `.env`
- Check backend logs for errors

### **Database Errors?**
- Check PostgreSQL is healthy: `docker-compose ps postgres`
- Restart services: `docker-compose restart`

---

## 📊 **API Testing**

### **Using Swagger UI**
1. Go to: `http://localhost:8000/docs`
2. Try endpoints:
   - `POST /api/v1/auth/register` - Register user
   - `POST /api/v1/auth/login` - Login
   - `GET /api/v1/posts/feed` - Get feed
   - `POST /api/v1/posts/upload` - Upload post

### **Using cURL**
```bash
# Get feed
curl http://localhost:8000/api/v1/posts/feed

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"test123"}'
```

---

## ✅ **Success Criteria**

Your app is working correctly if:
- ✅ Can register and login
- ✅ Feed shows posts (after seeding)
- ✅ Can upload new posts
- ✅ Search returns relevant results
- ✅ AI chat responds intelligently
- ✅ Profile page works
- ✅ Theme toggle works
- ✅ All pages load without errors

---

## 🎉 **Happy Testing!**

Enjoy exploring your InstaIntelli app! 🚀

