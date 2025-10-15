# Archon UI Authentication Testing Checklist

Date Created: 2025-10-15

## Pre-Testing Setup

- [ ] Backend server is running
- [ ] Backend has `/api/auth/validate` endpoint implemented
- [ ] You have a valid API key for testing
- [ ] Frontend dev server is running on http://localhost:3737
- [ ] Browser DevTools are open (F12)

## 1. Initial Access Tests

### Test 1.1: First Time Access
**Steps:**
1. Clear browser localStorage (DevTools > Application > Local Storage > Clear All)
2. Navigate to http://localhost:3737
3. Observe behavior

**Expected Results:**
- [ ] Automatically redirected to /login page
- [ ] Login page displays Archon logo
- [ ] API key input field is visible
- [ ] Login button is present
- [ ] No errors in console

**Actual Results:**
```
Notes:
```

### Test 1.2: Direct Protected Route Access
**Steps:**
1. Ensure logged out (clear localStorage)
2. Navigate directly to http://localhost:3737/knowledge
3. Observe behavior

**Expected Results:**
- [ ] Redirected to /login page
- [ ] No errors in console
- [ ] Original destination preserved in location state

**Actual Results:**
```
Notes:
```

## 2. Login Flow Tests

### Test 2.1: Empty API Key Submission
**Steps:**
1. On login page, leave API key field empty
2. Click "Login" button

**Expected Results:**
- [ ] Error message displays: "Please enter an API key"
- [ ] Remains on login page
- [ ] No API call made (check Network tab)

**Actual Results:**
```
Notes:
```

### Test 2.2: Invalid API Key
**Steps:**
1. Enter invalid API key: "test-invalid-key-12345"
2. Click "Login" button
3. Wait for response

**Expected Results:**
- [ ] Loading spinner shows during validation
- [ ] Error message displays: "Invalid API key..."
- [ ] Remains on login page
- [ ] API call to /api/auth/validate returns 401
- [ ] No key stored in localStorage

**Actual Results:**
```
Notes:
```

### Test 2.3: Valid API Key
**Steps:**
1. Enter valid API key
2. Click "Login" button
3. Wait for response

**Expected Results:**
- [ ] Loading spinner shows during validation
- [ ] Redirected to /knowledge page
- [ ] API key stored in localStorage (key: archon_api_key)
- [ ] No errors in console
- [ ] Navigation sidebar visible with logout button

**Actual Results:**
```
Notes:
```

### Test 2.4: Network Error During Login
**Steps:**
1. Stop backend server
2. Enter any API key
3. Click "Login" button

**Expected Results:**
- [ ] Error message displays indicating network issue
- [ ] Remains on login page
- [ ] No key stored in localStorage

**Actual Results:**
```
Notes:
```

## 3. Protected Routes Tests

### Test 3.1: Access Knowledge Base
**Steps:**
1. Ensure logged in
2. Navigate to /knowledge

**Expected Results:**
- [ ] Page loads successfully
- [ ] Content displays correctly
- [ ] No redirect to login
- [ ] Navigation active indicator on Knowledge Base icon

**Actual Results:**
```
Notes:
```

### Test 3.2: Access Settings
**Steps:**
1. Ensure logged in
2. Navigate to /settings

**Expected Results:**
- [ ] Page loads successfully
- [ ] Settings content displays
- [ ] No redirect to login

**Actual Results:**
```
Notes:
```

### Test 3.3: Access MCP
**Steps:**
1. Ensure logged in
2. Navigate to /mcp

**Expected Results:**
- [ ] Page loads successfully
- [ ] MCP content displays
- [ ] No redirect to login

**Actual Results:**
```
Notes:
```

### Test 3.4: Navigation Between Protected Routes
**Steps:**
1. Ensure logged in
2. Click through navigation items: Knowledge > Settings > MCP > Knowledge

**Expected Results:**
- [ ] All routes load correctly
- [ ] Active indicator moves with selection
- [ ] No redirects to login
- [ ] No console errors

**Actual Results:**
```
Notes:
```

## 4. API Authentication Tests

### Test 4.1: Authenticated API Call
**Steps:**
1. Ensure logged in
2. Open Network tab in DevTools
3. Navigate to a page that makes API calls (e.g., Knowledge Base)
4. Observe network requests

**Expected Results:**
- [ ] API requests include Authorization header
- [ ] Header format: "Authorization: Bearer <api-key>"
- [ ] Requests return 200 OK
- [ ] Data loads correctly

**Actual Results:**
```
Authorization Header Present: Yes/No
Header Value: Bearer [redacted]
Response Status:
Notes:
```

### Test 4.2: API Call Without Authentication
**Steps:**
1. In DevTools Console, manually make API call without auth:
```javascript
fetch('/api/knowledge/documents').then(r => r.json()).then(console.log)
```

**Expected Results:**
- [ ] Request returns 401 Unauthorized
- [ ] User automatically logged out
- [ ] Redirected to /login page
- [ ] localStorage cleared

**Actual Results:**
```
Notes:
```

## 5. Logout Tests

### Test 5.1: Manual Logout
**Steps:**
1. Ensure logged in and on any page
2. Click logout button (bottom of navigation)
3. Observe behavior

**Expected Results:**
- [ ] Redirected to /login page
- [ ] localStorage cleared (check archon_api_key)
- [ ] No errors in console

**Actual Results:**
```
Notes:
```

### Test 5.2: Post-Logout Navigation
**Steps:**
1. Logout as above
2. Try to navigate to /knowledge via URL

**Expected Results:**
- [ ] Redirected back to /login
- [ ] Protected route not accessible

**Actual Results:**
```
Notes:
```

### Test 5.3: Logout Tooltip
**Steps:**
1. Ensure logged in
2. Hover over logout button

**Expected Results:**
- [ ] Tooltip appears showing "Logout"
- [ ] Button highlights with red tint

**Actual Results:**
```
Notes:
```

## 6. Session Persistence Tests

### Test 6.1: Page Refresh
**Steps:**
1. Login successfully
2. Navigate to /settings
3. Refresh page (F5 or Cmd+R)

**Expected Results:**
- [ ] Brief loading screen shows
- [ ] Remains on /settings page
- [ ] Still authenticated (no redirect to login)
- [ ] API key still in localStorage

**Actual Results:**
```
Notes:
```

### Test 6.2: Browser Close/Reopen
**Steps:**
1. Login successfully
2. Close browser completely
3. Reopen browser
4. Navigate to http://localhost:3737

**Expected Results:**
- [ ] Brief loading screen shows
- [ ] Automatically authenticated
- [ ] Redirected to /knowledge (default route)
- [ ] API key still in localStorage

**Actual Results:**
```
Notes:
```

### Test 6.3: New Tab
**Steps:**
1. Login in one tab
2. Open new tab
3. Navigate to http://localhost:3737

**Expected Results:**
- [ ] New tab also authenticated
- [ ] Shares localStorage with first tab
- [ ] No need to login again

**Actual Results:**
```
Notes:
```

## 7. Deep Linking Tests

### Test 7.1: Deep Link While Logged Out
**Steps:**
1. Ensure logged out
2. Navigate directly to http://localhost:3737/settings
3. Login with valid API key

**Expected Results:**
- [ ] Redirected to /login first
- [ ] After successful login, redirected to /settings (original destination)
- [ ] Not redirected to /knowledge

**Actual Results:**
```
Notes:
```

### Test 7.2: Deep Link While Logged In
**Steps:**
1. Ensure logged in
2. Navigate directly to http://localhost:3737/mcp

**Expected Results:**
- [ ] Page loads immediately
- [ ] No redirect to login
- [ ] Content displays correctly

**Actual Results:**
```
Notes:
```

## 8. Error Handling Tests

### Test 8.1: Backend Unavailable During Validation
**Steps:**
1. Have valid key in localStorage
2. Stop backend server
3. Refresh page

**Expected Results:**
- [ ] Error handled gracefully
- [ ] Error message or toast displayed
- [ ] User can attempt to login again

**Actual Results:**
```
Notes:
```

### Test 8.2: 401 Response Mid-Session
**Steps:**
1. Login successfully
2. Have backend invalidate the API key (or simulate 401 response)
3. Make an API call

**Expected Results:**
- [ ] 401 detected automatically
- [ ] localStorage cleared
- [ ] Redirected to /login page
- [ ] Toast/error message displayed

**Actual Results:**
```
Notes:
```

### Test 8.3: Malformed API Key
**Steps:**
1. Manually set invalid data in localStorage:
```javascript
localStorage.setItem('archon_api_key', 'null')
```
2. Refresh page

**Expected Results:**
- [ ] Validation fails
- [ ] Redirected to /login
- [ ] Bad key cleared from localStorage

**Actual Results:**
```
Notes:
```

## 9. UI/UX Tests

### Test 9.1: Login Page Design
**Steps:**
1. Navigate to /login page
2. Observe visual design

**Expected Results:**
- [ ] Matches Archon's Apple-inspired design aesthetic
- [ ] Glassmorphic card effect visible
- [ ] Logo has subtle glow
- [ ] Clean, minimal layout
- [ ] Proper spacing and typography
- [ ] Responsive on mobile (test with DevTools)

**Actual Results:**
```
Notes:
```

### Test 9.2: Loading States
**Steps:**
1. Observe loading states during:
   - Initial auth check on page load
   - Login button submission
   - Protected route access while validating

**Expected Results:**
- [ ] Loading spinner appears
- [ ] Appropriate loading text
- [ ] Smooth transitions
- [ ] No layout shift

**Actual Results:**
```
Notes:
```

### Test 9.3: Error Message Display
**Steps:**
1. Trigger various errors:
   - Invalid API key
   - Empty input
   - Network error

**Expected Results:**
- [ ] Error messages clearly visible
- [ ] Red color scheme for errors
- [ ] AlertCircle icon present
- [ ] Messages are user-friendly
- [ ] Messages clear when user retries

**Actual Results:**
```
Notes:
```

### Test 9.4: Navigation Integration
**Steps:**
1. Login successfully
2. Examine navigation sidebar

**Expected Results:**
- [ ] Logout button at bottom
- [ ] Separator line above logout
- [ ] Red hover state on logout
- [ ] Logout icon (door with arrow)
- [ ] Consistent with other navigation items
- [ ] Tooltip works

**Actual Results:**
```
Notes:
```

## 10. Accessibility Tests

### Test 10.1: Keyboard Navigation
**Steps:**
1. Navigate to /login using only keyboard
2. Tab through elements
3. Press Enter to submit

**Expected Results:**
- [ ] Can tab to API key input
- [ ] Can tab to Login button
- [ ] Can submit with Enter key
- [ ] Focus indicators visible
- [ ] Logical tab order

**Actual Results:**
```
Notes:
```

### Test 10.2: Screen Reader Support
**Steps:**
1. Enable screen reader (VoiceOver on Mac, NVDA on Windows)
2. Navigate login page

**Expected Results:**
- [ ] Input field properly labeled
- [ ] Button has accessible label
- [ ] Error messages announced
- [ ] Loading states announced

**Actual Results:**
```
Notes:
```

### Test 10.3: ARIA Attributes
**Steps:**
1. Inspect login page HTML
2. Check for proper ARIA attributes

**Expected Results:**
- [ ] aria-label on icon buttons
- [ ] aria-busy during loading
- [ ] aria-invalid on error state
- [ ] Proper role attributes

**Actual Results:**
```
Notes:
```

## 11. Security Tests

### Test 11.1: API Key Not Visible in URL
**Steps:**
1. Login with API key
2. Check browser URL bar
3. Check browser history

**Expected Results:**
- [ ] API key never appears in URL
- [ ] No sensitive data in query parameters
- [ ] History entries clean

**Actual Results:**
```
Notes:
```

### Test 11.2: API Key Input Masked
**Steps:**
1. Navigate to /login
2. Type in API key field

**Expected Results:**
- [ ] Input type is "password"
- [ ] Characters masked with bullets
- [ ] No visible key in DevTools Elements tab

**Actual Results:**
```
Notes:
```

### Test 11.3: Network Tab Shows Bearer Token
**Steps:**
1. Login and make API calls
2. Check Network tab for request details

**Expected Results:**
- [ ] Authorization header visible but expected
- [ ] Using HTTPS in production (check deployment)
- [ ] No keys logged to console

**Actual Results:**
```
Notes:
```

## 12. Cross-Browser Tests

### Test 12.1: Chrome/Chromium
**Steps:**
Run tests 1-11 in Chrome

**Expected Results:**
- [ ] All tests pass
- [ ] No browser-specific issues

**Actual Results:**
```
Notes:
```

### Test 12.2: Firefox
**Steps:**
Run tests 1-11 in Firefox

**Expected Results:**
- [ ] All tests pass
- [ ] localStorage works correctly
- [ ] No browser-specific issues

**Actual Results:**
```
Notes:
```

### Test 12.3: Safari
**Steps:**
Run tests 1-11 in Safari

**Expected Results:**
- [ ] All tests pass
- [ ] No browser-specific issues
- [ ] Webkit-specific CSS renders correctly

**Actual Results:**
```
Notes:
```

## Test Summary

**Date Tested:** _______________
**Tester Name:** _______________
**Environment:** Development / Staging / Production
**Backend Version:** _______________
**Frontend Version:** _______________

### Results Overview
- Total Tests: 60+
- Passed: ______
- Failed: ______
- Skipped: ______
- Blocked: ______

### Critical Issues Found
```
1.
2.
3.
```

### Minor Issues Found
```
1.
2.
3.
```

### Recommendations
```
1.
2.
3.
```

### Sign-off
- [ ] All critical functionality works
- [ ] No blocking issues found
- [ ] Ready for deployment

**Signed:** _______________
**Date:** _______________
