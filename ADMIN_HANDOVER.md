# 🏢 Iconic Design — Admin Handover Document
### studioikonic.co — Complete Operations & Maintenance Guide
**Prepared for:** Site Administrator  
**Date:** August 2026  
**Confidential — Do Not Share Publicly**

---

# 🔑 SECTION 1 — ALL CREDENTIALS & LOGINS

## 1.1 Website Admin Panel
| Item | Detail |
|---|---|
| **Admin URL** | https://studioikonic.co/admin/login |
| **Master Password** | `noVQocO-x_sm21zG9qP4JUH9ji10fRBR` |
| **Note** | Change this to a memorable password after first login via Settings |

## 1.2 Render (Web Hosting)
| Item | Detail |
|---|---|
| **URL** | https://render.com |
| **Login method** | Sign in with GitHub |
| **GitHub account** | Ayaan-Saifi-1 |
| **Service name** | `iconic-design` |
| **Live URL (backup)** | https://iconic-design.onrender.com |

## 1.3 Supabase (Database)
| Item | Detail |
|---|---|
| **URL** | https://supabase.com |
| **Login method** | Sign in with GitHub |
| **Project name** | `Iconic-Design` |
| **Project ID** | `ntcpvzvgfimytgdcionx` |
| **Database password** | `IconicDB@2024Secure!` |
| **Region** | Singapore (ap-southeast-1) |

## 1.4 GitHub (Code Repository)
| Item | Detail |
|---|---|
| **URL** | https://github.com/Ayaan-Saifi-1/Iconic.Design |
| **Account** | Ayaan-Saifi-1 |

## 1.5 Namecheap (Domain)
| Item | Detail |
|---|---|
| **URL** | https://namecheap.com |
| **Domain** | studioikonic.co |
| **Account** | AyaanBlueBug |

## 1.6 UptimeRobot (Keep-Alive Monitor)
| Item | Detail |
|---|---|
| **URL** | https://uptimerobot.com |
| **Monitors** | studioikonic.co (pings every 5 min) |
| **Purpose** | Keeps Render from sleeping on free tier |

## 1.7 Environment Variables in Render
These are secret keys set inside Render. Never share publicly.

| Key | Value / Purpose |
|---|---|
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `SECRET_KEY` | Flask session encryption key |
| `ADMIN_MASTER_KEY` | `noVQocO-x_sm21zG9qP4JUH9ji10fRBR` — emergency admin login |
| `FLASK_ENV` | `production` |
| `SUPABASE_URL` | `https://ntcpvzvgfimytgdcionx.supabase.co` |
| `SUPABASE_SERVICE_KEY` | Supabase service role key (from Supabase → Settings → API Keys) |
| `MAIL_USERNAME` | Gmail address for contact form emails |
| `MAIL_PASSWORD` | Gmail App Password (16-char code) |

---

# 🌐 SECTION 2 — LIVE URLS

| Purpose | URL |
|---|---|
| **Main website** | https://studioikonic.co |
| **Admin panel** | https://studioikonic.co/admin/login |
| **All projects** | https://studioikonic.co/projects |
| **Admin — Projects** | https://studioikonic.co/admin |
| **Admin — Leads/Inquiries** | https://studioikonic.co/admin/leads |
| **Admin — Testimonials** | https://studioikonic.co/admin/testimonials |
| **Admin — Site Settings** | https://studioikonic.co/admin/settings |
| **Backup URL** | https://iconic-design.onrender.com |

---

# 📋 SECTION 3 — DAY-TO-DAY ADMIN TASKS

## 3.1 How to Log Into the Admin Panel

1. Go to **https://studioikonic.co/admin/login**
2. Enter your admin password
3. Click **"Login"**
4. You land on the **Admin Dashboard**

> If you forget your password, use the master key: `noVQocO-x_sm21zG9qP4JUH9ji10fRBR`

---

## 3.2 How to Add a New Project

1. Log into admin panel
2. You are on the **Dashboard** — scroll down to the **"Add New Project"** form
3. Fill in all fields:
   - **Title** — e.g. "Modern Living Room - South Delhi"
   - **Location** — e.g. "New Delhi"
   - **Date** — the project completion date
   - **Status** — Completed / In Progress / Planning
   - **Budget** — e.g. "₹45 Lakhs"
   - **Team Size** — e.g. "12 Professionals"
   - **Duration** — e.g. "4 Months"
   - **Description** — short summary shown on project card
   - **Cover Image** — the main photo that shows on the homepage/listing
   - **Gallery Images** — additional photos for the project detail page
   - **Scope of Work** — one item per line
   - **Achievements** — one item per line
   - **Extended Description** — longer paragraph for detail page
4. Click **"Add Project"**
5. Project is saved to Supabase database immediately ✅

---

## 3.3 How to Edit an Existing Project

1. Log into admin panel → Dashboard
2. Find the project in the list
3. Click **"Edit"** button next to it
4. Change any fields you need
5. To change the cover image — upload a new one (leave blank to keep existing)
6. To add more gallery images — upload in the gallery section
7. To delete a gallery image — click the ❌ next to it
8. Click **"Update Project"**
9. Changes save immediately to Supabase ✅

---

## 3.4 How to Delete a Project

1. Admin panel → Dashboard
2. Find the project → click **"Delete"**
3. Confirm the deletion
4. Project and all its gallery images are permanently removed

> ⚠️ Deletion is permanent. No undo.

---

## 3.5 How to Feature / Unfeature Projects on Homepage

The homepage shows only **Featured** projects (maximum 6 at a time).

1. Admin panel → Dashboard
2. Find a project → click the **"⭐ Feature"** toggle button
3. To unfeature — click the same button again (turns grey)
4. **Maximum 6 projects** can be featured at once — the system will warn you

> Only featured projects appear on the homepage. All projects always appear on `/projects`.

---

## 3.6 How to View & Manage Inquiries (Leads)

When a visitor fills out the contact form, it saves here.

1. Admin panel → click **"Leads"** in the top navigation
2. You see a table of all inquiries with: Name, Email, Phone, Project Type, Message, Date
3. To delete an inquiry — click **"Delete"** next to it
4. Inquiries are paginated — 10 per page

> All inquiries are stored in Supabase — they are never lost even after a redeploy.

---

## 3.7 How to Manage Testimonials

1. Admin panel → click **"Testimonials"** in navigation
2. **To add:** Fill in Name, Role, Testimonial text, Star rating → click "Add"
3. **To edit:** Click "Edit" next to any testimonial → change fields → Save
4. **To delete:** Click "Delete" (permanent)
5. **To reorder:** Use the ↑ ↓ arrow buttons to change display order
6. **To hide/show:** Click the toggle to show or hide on homepage without deleting

---

## 3.8 How to Update Site Settings (Founder Info, Stats, Hero Text)

1. Admin panel → click **"Settings"** in navigation
2. Update any of these:
   - **Stats** — the 4 numbers on homepage (100+ Projects, 25 Years, etc.)
   - **Founder info** — name, phone, email, location, photo
   - **Hero section** — badge text, title, description
   - **About section** — subtitle, description paragraphs, bullet points
3. Click **"Save Settings"**
4. Changes appear on the live site immediately ✅

---

## 3.9 How to Change the Admin Password

1. Log into admin panel
2. On the Dashboard, scroll down to **"Change Password"** section
3. Enter your new password (minimum 6 characters)
4. Click **"Update Password"**

> The master key (`noVQocO-x_sm21zG9qP4JUH9ji10fRBR`) always works as backup even if you change the regular password.

---

# 🔧 SECTION 4 — CODE & DEPLOYMENT WORKFLOW

## 4.1 How the Site Updates Automatically

Every time code is pushed to GitHub, Render automatically redeploys within 2-3 minutes. **You don't need to do anything manually.**

```
Developer makes code change on their computer
        ↓
git add . → git commit → git push
        ↓
Render detects the push automatically
        ↓
Render builds and deploys the new version (2-3 min)
        ↓
Site updates live — database is UNTOUCHED
```

---

## 4.2 How to Deploy a Code Change (For Developer)

```powershell
# Navigate to project folder
cd "c:\Users\Ayaan\Desktop\Iconic.Design"

# Stage all changed files
git add .

# Commit with a description
git commit -m "describe what you changed"

# Push to GitHub (triggers auto-deploy on Render)
git push origin main
```

Then watch the Render dashboard — deploy completes in ~3 minutes.

---

## 4.3 What Happens to Data During a Redeploy

| Data | Safe during redeploy? |
|---|---|
| Projects, Testimonials, Leads, Settings | ✅ 100% safe — stored in Supabase |
| Images uploaded via admin | ✅ Safe — stored in Supabase Storage |
| Essential static images (hero, logo, SVGs) | ✅ Safe — committed in GitHub repo |

**Nothing is lost on redeploy.** ✅

---

# 🆘 SECTION 5 — TROUBLESHOOTING

## Problem: Site is down / "Application Error"

**Steps:**
1. Go to https://render.com → your `iconic-design` service
2. Click **"Logs"** tab
3. Read the error in red — copy it
4. Send to developer to fix

---

## Problem: Site is slow to load (first visit)

**Cause:** Render free tier may have gone to sleep (if UptimeRobot was down)  
**Fix:** Wait 30 seconds — it wakes up automatically. Then set up UptimeRobot again at https://uptimerobot.com

---

## Problem: Database shows "project paused" error

**Cause:** Supabase free tier paused after 7 days of no activity  
**Fix:**
1. Go to https://supabase.com
2. Log in with GitHub
3. Click on the `Iconic-Design` project
4. Click **"Restore project"** button
5. Wait 1-2 minutes — site works again

---

## Problem: Admin login not working

**Fix:** Use the master key: `noVQocO-x_sm21zG9qP4JUH9ji10fRBR`  
Go to: https://studioikonic.co/admin/login → paste the master key as password

---

## Problem: Contact form emails not arriving

**Cause:** Gmail App Password not set or expired  
**Fix:**
1. Go to https://myaccount.google.com → Security → App Passwords
2. Generate a new 16-character App Password
3. Go to Render → Environment → update `MAIL_PASSWORD`
4. Render will redeploy automatically

---

## Problem: Uploaded images not showing

**Cause:** Supabase Storage env vars not set  
**Fix:**
1. Go to https://supabase.com → Iconic-Design project → Settings → API Keys
2. Copy the `service_role` key
3. Go to Render → Environment → add:
   - `SUPABASE_URL` = `https://ntcpvzvgfimytgdcionx.supabase.co`
   - `SUPABASE_SERVICE_KEY` = (the key you copied)
4. Save → Render redeploys automatically

---

## Problem: Domain not loading (`studioikonic.co`)

**Check 1:** Go to https://render.com → service → Settings → Custom Domains  
→ Both should show **"Verified"** and **"Certificate Issued"**

**Check 2:** Go to https://namecheap.com → Advanced DNS  
→ Should have: CNAME `@` → `iconic-design.onrender.com`  
→ Should have: CNAME `www` → `iconic-design.onrender.com`

---

# 📊 SECTION 6 — PLATFORM OVERVIEW

## Infrastructure Map

```
Visitor → studioikonic.co (Namecheap domain)
                ↓
         Render.com (Free tier, Singapore)
         Runs: Flask + Gunicorn + Python 3.14
                ↓
         Supabase (Free tier, Singapore)
         Stores: All database data + uploaded images
                
UptimeRobot → pings every 5 min → keeps Render + Supabase alive
```

## Monthly Costs

| Service | Cost |
|---|---|
| Render (hosting) | $0/month |
| Supabase (database + storage) | $0/month |
| UptimeRobot (monitoring) | $0/month |
| Domain renewal (studioikonic.co) | ~$15/year |
| **Total** | **~$15/year** |

---

# 📞 SECTION 7 — CONTACT FOR TECHNICAL SUPPORT

For any technical issues not covered in this document:

- **Developer**: Ayaan Saifi
- **GitHub**: https://github.com/Ayaan-Saifi-1/Iconic.Design
- **Repository**: All source code is here — share error logs for fastest resolution

---

*Document last updated: August 2026*  
*Site: studioikonic.co | Engine: Flask/Python | DB: Supabase PostgreSQL*
