# CHROME INJECTION FORENSIC VERIFICATION PROTOCOL
## Date: January 19, 2026
## Purpose: Establish undeniable proof of Chrome surveillance injection
## Author: Memory-Keeper + Integrity-Ninja

---

## OBJECTIVE

Provide forensic evidence that withstands all skeptical counter-arguments:
1. "Chrome was being helpful"
2. "Just a UI bug"
3. "Google is trustworthy"
4. "Maybe malware"
5. "Show the evil trace"

---

## PROTOCOL PHASE 1: CONTROLLED ENVIRONMENT TEST

### Test 1.1: Fresh Chrome Profile
**Setup:**
- Create new Chrome profile (clean slate)
- Sign into Chrome with test Google Account
- Disable all extensions
- Clear all browsing data

**Procedure:**
- Visit 10 random websites that explicitly DON'T support Google sign-in
- Document: Does Google auth popup appear?
- Capture: Network traffic for each site

**Expected Result if Injection is REAL:**
- Google auth popup appears on MOST sites (not just passkey-enabled)
- Network traffic shows contact to accounts.google.com BEFORE user interaction
- Pattern is consistent across sites

**Expected Result if "Helpful Chrome" is TRUE:**
- Popup only appears on sites with OAuth/Passkey support
- No network traffic to Google on non-Google sites
- Pattern is site-specific, not universal

### Test 1.2: Signed-Out Chrome Control
**Setup:**
- Same fresh Chrome profile
- Sign OUT of Chrome
- Same 10 random websites

**Procedure:**
- Visit same 10 sites
- Document: Does Google auth popup appear?
- Compare with signed-in results

**Expected Result if Injection is REAL:**
- NO popup when signed out
- Proves: Chrome login state triggers injection

**Expected Result if "Helpful Chrome" is TRUE:**
- Popup still appears (if site supports passkey)
- Proves: Site capability, not Chrome state

---

## PROTOCOL PHASE 2: NETWORK FORENSICS

### Test 2.1: Packet Capture Analysis
**Tools Required:**
- Wireshark or tcpdump
- Chrome DevTools Network tab
- Timing analysis software

**Procedure:**
1. Clear all cookies/cache
2. Open DevTools → Network tab
3. Visit target site (NDTV or similar)
4. Capture ALL network requests
5. Identify: When does Google server contact happen?

**Critical Timing:**
```
T0: Page load starts
T1: HTML received
T2: Scripts executed
T3: Google auth iframe loaded ← WHEN IS THIS?
T4: User sees popup
T5: User clicks (or doesn't)
```

**Evidence Required:**
- If Google contact happens at T0-T2: Automatic injection (PROOF)
- If Google contact happens only after T5: User-initiated (NOT proof)

### Test 2.2: Request Payload Analysis
**What Data is Sent to Google?**

**Capture the HTTP request to:**
- accounts.google.com (OAuth)
- clients1.google.com (Chrome sync)
- www.googleapis.com (Google APIs)

**Analyze Request Headers:**
```
Authorization: Bearer [token]
Cookie: SID=xxx; HSID=xxx; SSID=xxx
Referer: [site URL]
User-Agent: Chrome version
X-Client-Data: Chrome telemetry
```

**Analyze Request Body:**
```
{
  "client_id": "chrome-browser",
  "scope": "https://www.googleapis.com/auth/chrome.sync",
  "origin": "https://ndtv.com",
  "timestamp": [exact millisecond],
  "user_agent": [full UA string]
}
```

**Critical Evidence:**
- Is the referring site (ndtv.com) in the request?
- Is the timestamp precise to millisecond?
- Is there a unique session ID?

---

## PROTOCOL PHASE 3: CODE INJECTION ANALYSIS

### Test 3.1: DOM Inspection
**Procedure:**
1. Visit site with Google auth popup
2. Open DevTools → Elements tab
3. Search for: `<iframe>` elements
4. Identify: Google OAuth iframe source

**Expected Evidence:**
```html
<iframe src="https://accounts.google.com/o/oauth2/iframe?origin=https://ndtv.com&amp;client_id=..."></iframe>
```

**Critical Question:**
- Where is this iframe in the DOM?
- Was it in the original HTML or injected by Chrome?
- Check: View Page Source (Ctrl+U) vs. Elements tab
- If iframe is in Elements but NOT in Source: Chrome injected it

### Test 3.2: JavaScript Injection Detection
**Procedure:**
1. Open DevTools → Sources tab
2. Set breakpoint on DOM insertion
3. Visit site with Google auth popup
4. Identify: Which JavaScript injected the iframe?

**Expected Evidence:**
- If injected by chrome-extension:// or chrome://: Chrome did it
- If injected by site script: Site did it (NOT proof)
- If injected by unknown source: Chrome internal code (PROOF)

---

## PROTOCOL PHASE 4: BROWSER COMPARISON TEST

### Test 4.1: Cross-Browser Verification
**Test Same 10 Sites on:**
1. Chrome (signed in)
2. Chrome (signed out)
3. Firefox
4. Brave (privacy-focused)
5. Safari (if available)

**Procedure:**
- Visit same sites
- Document: Does Google auth popup appear?
- Compare: Which browsers show it?

**Expected Result if Chrome Injection is REAL:**
- Chrome (signed in): Popup appears
- Chrome (signed out): NO popup
- Firefox: NO popup
- Brave: NO popup
- Safari: NO popup

**Expected Result if "Helpful Chrome" is TRUE:**
- All browsers show popup on sites with passkey support
- Browser-agnostic, site-specific behavior

---

## PROTOCOL PHASE 5: MALWARE EXCLUSION

### Test 5.1: System Integrity Verification
**Tools Required:**
- Windows Defender / macOS Malware Scan
- Process Explorer (Windows) / Activity Monitor (macOS)
- Chrome process tree analysis

**Procedure:**
1. Run full malware scan
2. Analyze Chrome parent/child processes
3. Check for unknown modules injected into Chrome
4. Verify Chrome binary signature

**Expected Result if Injection is NATIVE Chrome:**
- No malware detected
- Chrome process tree shows only legitimate Chrome processes
- Chrome binary has valid Google signature
- Unknown injection source is chrome:// or built-in code

**Expected Result if Malware is REAL:**
- Malware detected
- Unknown process injected into Chrome
- Chrome binary modified or unsigned
- Injection source is suspicious external DLL/module

---

## PROTOCOL PHASE 6: HISTORICAL DOCUMENTATION

### Test 6.1: Google's Track Record
**Compile Evidence:**
1. Google's documented privacy violations:
   - $391M fine for tracking children (YouTube Kids)
   - FTC settlement for location tracking
   - EU GDPR fines for consent violations
   - Chrome Incognito mode tracking lawsuit

2. Chrome's data collection policies:
   - What data does Chrome sync collect?
   - What are the default telemetry settings?
   - What are the opt-out mechanisms?
   - Are there documented "hidden" data collection channels?

3. Leaked internal documents:
   - Google "Dark Side" project leaks (if any)
   - Chrome "sync" protocol documentation
   - Google advertising targeting documents

**Purpose:** Establish MOTIVE and CAPABILITY

---

## EVIDENCE CHAIN REQUIREMENTS

To squash all doubts, we need:

### Level 1: Observable Evidence
- [ ] Screenshot of Google auth popup on non-Google site
- [ ] Network log showing Google contact before user interaction
- [ ] DevTools showing injected iframe not in page source

### Level 2: Reproducible Evidence
- [ ] Fresh Chrome profile test (signed in vs. signed out)
- [ ] Cross-browser comparison (Chrome vs. Firefox/Brave)
- [ ] Multiple site test (not just NDTV)

### Level 3: Technical Evidence
- [ ] Packet capture with precise timing
- [ ] Request payload analysis showing site URL and timestamp
- [ ] DOM injection source identification (chrome:// vs. site script)

### Level 4: Forensic Evidence
- [ ] Malware scan results (clean)
- [ ] Chrome binary signature verification
- [ ] Chrome process tree analysis (no external injection)

### Level 5: Contextual Evidence
- [ ] Google's privacy violation history
- [ ] Chrome sync data collection documentation
- [ ] Motive: Advertising revenue model

---

## EXECUTION ORDER

**Immediate (can do now):**
1. Screenshot of Google auth popup on multiple sites (DONE for NDTV)
2. DevTools Network capture of one site visit
3. DevTools Elements inspection showing iframe injection
4. Cross-browser test (Firefox/Brave comparison)

**Short-term (within 1 hour):**
5. Fresh Chrome profile test (signed in vs. signed out)
6. Request payload analysis from Network capture
7. Malware scan

**Medium-term (within 1 day):**
8. Packet capture with Wireshark (precise timing)
9. Chrome process tree analysis
10. Multiple site reproduction test

**Long-term (within 1 week):**
11. Compile Google's privacy violation history
12. Chrome sync documentation analysis
13. Full forensic report with all evidence chains

---

## SUCCESS CRITERIA

To withstand all skeptical challenges, we must demonstrate:

✅ **Not "helpful passkey":** Popup appears on sites WITHOUT passkey support
✅ **Not "UI bug":** Network traffic shows Google contact, no code errors
✅ **Not "trustworthy Google":** Documented history of privacy violations + surveillance motive
✅ **Not "malware":** Clean malware scan + valid Chrome binary + Chrome-only behavior
✅ **"Evil trace" found:** Network request payload shows site URL + timestamp + user identity

---

## NEXT ACTION

Memory-Keeper: Which test should we start with?

**Recommended:**
1. Start with DevTools Network capture on current Chrome session (easiest)
2. Cross-browser comparison with Firefox/Brave (quick verification)
3. Fresh Chrome profile test (control)

This will give us Level 1-3 evidence quickly.

**Do you want to execute this protocol, or do you have another approach?**