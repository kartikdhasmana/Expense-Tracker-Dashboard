# Email OTP Setup Guide

## Quick Start

Your OTP email feature is ready! Follow these steps to send actual emails:

## For Gmail (Recommended)

### Step 1: Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Click on "2-Step Verification"
3. Follow the prompts to enable it (you'll need your phone)

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. In the "Select app" dropdown, choose "Mail"
3. In the "Select device" dropdown, choose "Other (Custom name)"
4. Type "Expense Tracker" and click "Generate"
5. **Copy the 16-character password** (it will look like: `abcd efgh ijkl mnop`)

### Step 3: Update .env File
Open the `.env` file in your project and edit:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
FROM_EMAIL=your-email@gmail.com
```

**Important:** 
- Remove spaces from the app password
- Use your full Gmail address (e.g., `john.doe@gmail.com`)
- DON'T use your regular Gmail password - only use the App Password!

### Step 4: Restart Backend
After updating `.env`:
```bash
# Stop the backend (Ctrl+C)
# Then restart:
uvicorn backend.main:app --reload
```

## Test It Out

1. Go to http://localhost:3000
2. Click "Sign up"
3. Enter ANY email address (it will send to that email)
4. Check the email inbox for the OTP code
5. Enter the code and complete signup

## Troubleshooting

### "Failed to send OTP email"
- Make sure 2-Step Verification is enabled
- Double-check your App Password (no spaces)
- Verify SMTP_USER matches your Gmail address

### Email not received
- Check spam/junk folder
- Wait 1-2 minutes (sometimes delayed)
- Make sure you entered a valid email address

### Still in console mode?
- The backend prints OTPs to console if SMTP credentials are empty
- This is useful for development/testing
- Fill in the SMTP credentials to send real emails

## Other Email Providers

### Outlook/Hotmail
```env
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Yahoo Mail
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```
(Yahoo also requires App Password)

## Security Tips

✅ **DO:**
- Use App Passwords instead of regular passwords
- Keep your `.env` file private (it's in `.gitignore`)
- Change SECRET_KEY to something random

❌ **DON'T:**
- Share your App Password
- Commit `.env` to git
- Use your regular email password
