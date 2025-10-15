# Test Plan - After Deployment

Created: 2025-10-15 | Timestamp: 11:20:00

## Pre-Deployment Checklist

- [x] Auth code verified in source
- [x] Production build completed
- [x] Build verified (1.4 MB bundle)
- [x] Deployment scripts created
- [ ] Files deployed to server
- [ ] Container restarted

## Post-Deployment Test Checklist

### Phase 1: Login Flow

#### Test 1.1: Redirect to Login
```
Action: Open https://archon.nexorithm.io in browser
Expected: Immediately redirected to https://archon.nexorithm.io/login
Status: [ ]
```

#### Test 1.2: Login Page Displays
```
Action: View /login page
Expected:
  - Clean UI with login form
  - API key input field visible
  - Submit button present
  - No console errors
Status: [ ]
```

#### Test 1.3: Invalid API Key
```
Action: Enter invalid key (e.g., "test123")
Expected:
  - Error message displayed
  - Still on /login page
  - No redirect
Status: [ ]
```

#### Test 1.4: Valid API Key Login
```
Action: Enter valid key: ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI
Expected:
  - Success message or immediate redirect
  - Redirected to /knowledge
  - No console errors
Status: [ ]
```

### Phase 2: Authenticated Access

#### Test 2.1: Knowledge Base Access
```
Action: View /knowledge after login
Expected:
  - Knowledge base page loads
  - Data displays (or "no items" if empty)
  - No 401 errors in console
  - API calls include Authorization header
Status: [ ]
```

#### Test 2.2: Settings Access
```
Action: Navigate to /settings
Expected:
  - Settings page loads
  - All settings visible
  - No authentication errors
Status: [ ]
```

#### Test 2.3: MCP Server Access
```
Action: Navigate to /mcp
Expected:
  - MCP page loads
  - Configuration visible
  - No authentication errors
Status: [ ]
```

#### Test 2.4: Projects Access (if enabled)
```
Action: Navigate to /projects
Expected:
  - Projects page loads
  - Projects list visible
  - No authentication errors
Status: [ ]
```

### Phase 3: Authorization Headers

#### Test 3.1: Network Tab Verification
```
Action: Open browser DevTools > Network tab, reload /knowledge
Expected:
  - All API calls to /api/* include Authorization header
  - Header format: "Bearer ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
  - No 401 responses
Status: [ ]
```

#### Test 3.2: localStorage Check
```
Action: Open browser DevTools > Console, run: localStorage.getItem('archon_api_key')
Expected:
  - Returns the API key
  - Format: "ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI"
Status: [ ]
```

### Phase 4: Logout Flow

#### Test 4.1: Logout Button
```
Action: Click logout button in navigation
Expected:
  - Redirected to /login
  - localStorage cleared
  - No longer authenticated
Status: [ ]
```

#### Test 4.2: Post-Logout Access Attempt
```
Action: Try to navigate to /knowledge after logout
Expected:
  - Immediately redirected to /login
  - Cannot access protected routes
Status: [ ]
```

### Phase 5: Browser Console Verification

#### Test 5.1: No Vite Dev Server Messages
```
Action: Open /login, check console
Expected:
  - No "[vite] connecting..." messages
  - No WebSocket errors
  - No "localhost:3737" references
Status: [ ]
```

#### Test 5.2: No Unnecessary Errors
```
Action: Navigate through app, monitor console
Expected:
  - No 401 errors (except during logout)
  - No authentication failures
  - Clean console output
Status: [ ]
```

### Phase 6: Direct URL Access

#### Test 6.1: Direct Knowledge URL (Unauthenticated)
```
Action: Clear localStorage, navigate to /knowledge
Expected:
  - Redirected to /login
  - Cannot access page
Status: [ ]
```

#### Test 6.2: Direct Settings URL (Unauthenticated)
```
Action: While unauthenticated, navigate to /settings
Expected:
  - Redirected to /login
  - Cannot access page
Status: [ ]
```

#### Test 6.3: Login URL (Already Authenticated)
```
Action: While authenticated, navigate to /login
Expected:
  - Either shows login page or redirects to /knowledge
  - (Implementation-dependent behavior)
Status: [ ]
```

### Phase 7: Session Persistence

#### Test 7.1: Page Reload
```
Action: Login, then reload page
Expected:
  - Stays authenticated
  - No redirect to /login
  - Data loads normally
Status: [ ]
```

#### Test 7.2: New Tab
```
Action: Login in one tab, open new tab to same domain
Expected:
  - New tab is also authenticated
  - No login required
Status: [ ]
```

#### Test 7.3: Browser Restart
```
Action: Login, close browser, reopen to same URL
Expected:
  - Still authenticated (if localStorage persists)
  - OR redirected to login (acceptable)
Status: [ ]
```

### Phase 8: Error Handling

#### Test 8.1: Network Error During Login
```
Action: Disable network, try to login
Expected:
  - Error message displayed
  - User informed of network issue
  - No crash or blank screen
Status: [ ]
```

#### Test 8.2: Invalid Token (Expired/Revoked)
```
Action: Manually set invalid token in localStorage, reload
Expected:
  - Redirected to /login
  - Token cleared from localStorage
  - User can re-authenticate
Status: [ ]
```

## Netzwächter-Specific Tests

### Test N.1: Netzwächter Knowledge Base
```
Action: Login, navigate to /knowledge, filter/search for Netzwächter items
Expected:
  - Netzwächter-specific knowledge items visible
  - Data loads correctly
  - No unauthorized access warnings
Status: [ ]
```

### Test N.2: Netzwächter Data Security
```
Action: Check that unauthenticated users cannot see Netzwächter data
Expected:
  - Without auth, redirected before any data loads
  - API returns 401 for unauthenticated requests
  - No data leakage in network responses
Status: [ ]
```

## Success Criteria

All tests must pass:
- [ ] All Phase 1 tests passed (Login Flow)
- [ ] All Phase 2 tests passed (Authenticated Access)
- [ ] All Phase 3 tests passed (Authorization Headers)
- [ ] All Phase 4 tests passed (Logout Flow)
- [ ] All Phase 5 tests passed (Console Verification)
- [ ] All Phase 6 tests passed (Direct URL Access)
- [ ] All Phase 7 tests passed (Session Persistence)
- [ ] All Phase 8 tests passed (Error Handling)
- [ ] All Netzwächter tests passed

## Rollback Plan

If tests fail:
```bash
# Rollback to previous version
ssh root@91.98.156.158 "cd /opt/archon/archon-ui-main && git checkout HEAD~1 && npm run build && docker compose restart archon-ui"
```

## Documentation After Testing

After all tests pass:
1. Update main README with authentication instructions
2. Document API key management process
3. Create user guide for Netzwächter client
4. Archive this test plan as evidence

## Test API Key

```
Valid Key: ak_597A_U6Z6POYpv8Sae-LxSNj2qe5dFXE6qzBjXe0tikQHqkI
Invalid Key: test123 (for testing error handling)
```

## Notes

- Test in multiple browsers: Chrome, Firefox, Safari
- Test in incognito mode to simulate fresh user
- Test with browser DevTools open to catch any hidden errors
- Take screenshots of successful login flow for documentation

Created: 2025-10-15 | Timestamp: 11:20:00
