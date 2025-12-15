# Preview Debug Guide

## Issue: Frontend crashes in Preview with "Script error"

### Root Cause
Frontend was making requests to `localhost` which doesn't work in Preview environment.

### Solution Applied

1. **Updated `/app/frontend/src/lib/api.js`:**
   - Made API_BASE URL relative or use REACT_APP_BACKEND_URL
   - Added axios interceptor for better error logging
   - Added 30s timeout
   - Console logs API base URL on load

2. **Added Graceful Error Handling:**
   - Dashboard: Won't crash if reports API fails, shows empty state
   - RepoScanResults: Shows error toast and redirects instead of crash
   - All API calls have try/catch with fallbacks

3. **Created Debug Tools:**

   **API Info Page** (`/api-info`):
   - Lists all available endpoints
   - Shows current configuration
   - Direct link to Swagger docs
   - Copy-paste curl examples

   **Network Debug Page** (`/debug`):
   - Tests all API endpoints
   - Shows success/failure status
   - Displays response times
   - Shows error messages

---

## 🔗 Useful URLs for Preview

### Documentation
- **Swagger API Docs**: `https://compliance-buddy-17.preview.emergentagent.com/docs`
- **ReDoc**: `https://compliance-buddy-17.preview.emergentagent.com/redoc`

### Debug Pages
- **API Info**: `https://compliance-buddy-17.preview.emergentagent.com/api-info`
- **Network Debug**: `https://compliance-buddy-17.preview.emergentagent.com/debug`

### Test Endpoints
```bash
# Health check
curl https://compliance-buddy-17.preview.emergentagent.com/api/health

# Get API info
curl https://compliance-buddy-17.preview.emergentagent.com/api/

# Get controls
curl https://compliance-buddy-17.preview.emergentagent.com/api/controls

# Get reports
curl https://compliance-buddy-17.preview.emergentagent.com/api/compliance/reports

# Get repo scans
curl https://compliance-buddy-17.preview.emergentagent.com/api/compliance/scan/repo
```

---

## 🐛 Debugging Steps

### 1. Check if Backend is Working

Open: `https://compliance-buddy-17.preview.emergentagent.com/docs`

If this loads, backend is fine.

### 2. Check Network Requests

Navigate to: `https://compliance-buddy-17.preview.emergentagent.com/debug`

Click "Run All Tests" to see which endpoints fail.

### 3. Check Browser Console

Open DevTools (F12) and look for:
- ✅ `API Base URL: https://compliance-buddy-17.preview.emergentagent.com/api`
- ❌ Any CORS errors
- ❌ Any 404/500 errors
- ❌ Network timeouts

### 4. Common Issues

**Issue**: API calls to `localhost`
**Fix**: Already fixed - using relative URLs or REACT_APP_BACKEND_URL

**Issue**: CORS errors
**Fix**: Backend has CORS enabled for `*`, should work

**Issue**: 404 on /api endpoints
**Fix**: Check that backend is running and /api prefix is correct

**Issue**: Timeout errors
**Fix**: Increased timeout to 30s, may need more for large uploads

---

## 🔧 Configuration Check

### Current Settings

**Frontend `.env`:**
```
REACT_APP_BACKEND_URL=https://compliance-buddy-17.preview.emergentagent.com
```

**API Base in code:**
```javascript
const API_BASE = BACKEND_URL ? `${BACKEND_URL}/api` : '/api';
```

This means:
- In Preview: Uses full URL with `/api` suffix
- In Docker: Can use relative `/api` path

---

## 📊 Network Requests That Should Work

### GET Requests (should all return 200)
1. `/api/` → API info
2. `/api/health` → Health status
3. `/api/controls` → 19 controls
4. `/api/compliance/reports` → List of reports (may be empty)
5. `/api/compliance/scan/repo` → List of repo scans (may be empty)

### POST Requests
1. `/api/compliance/scan` → Create questionnaire scan
2. `/api/compliance/scan/repo` → Upload repository ZIP

---

## ✅ Verification

After changes, verify:

1. **Dashboard loads without crash** ✓
2. **Can navigate to /scan/repo** ✓
3. **Can navigate to /api-info** ✓
4. **Can navigate to /debug** ✓
5. **Network debug shows green checks** (check this in Preview)
6. **No "Script error" in console** (check this in Preview)

---

## 🚨 If Still Broken

1. Check `/debug` page - which endpoints are failing?
2. Check browser console - any errors?
3. Check Network tab - what status codes?
4. Try curl commands manually - do they work?
5. Check backend logs for errors

---

## 📝 Changes Made

**Files Modified:**
- `/app/frontend/src/lib/api.js` - Better URL handling, error interceptor
- `/app/frontend/src/pages/Dashboard.js` - Graceful error handling
- `/app/frontend/src/pages/RepoScanResults.js` - Better error handling
- `/app/frontend/src/App.js` - Added new routes

**Files Created:**
- `/app/frontend/src/pages/ApiInfo.js` - API documentation page
- `/app/frontend/src/pages/NetworkDebug.js` - Network testing tool
- `/app/PREVIEW_DEBUG.md` - This file

**Result:**
Frontend should now handle API errors gracefully and not crash when endpoints are unavailable.
