# Qada Tracker

A free, simple app for making up missed prayers (qada), one day at a time.

**Open the app:** https://belalq1.github.io/qada-tracker/

Made as **sadaqah jariyah**. It's free, with no ads, no account and no tracking. Everything you enter stays on your own phone.

## What it does

- **Estimates what you owe.** You answer four quick questions: your age, the age you reached puberty, any years you prayed regularly, and your madhab. Hanafi counts Witr, because it is wajib in that school.
- **Gives you a daily checklist.** Pray your normal prayer, then its qada, then tick it off. Each prayer shows its full routine, for example *4 sunnah · 4 fard · 2 sunnah → 4 qada*.
- **Shows your progress:** prayers left, streaks, the last 14 days, an estimated finish date, and milestones.
- **Lets you back up and restore** your progress with a code, for when you change phones.
- **Works offline** once it's added to your home screen.

## Install it on your phone

- **iPhone:** open the link in Safari, tap **Share**, then **Add to Home Screen**.
- **Android:** open the link in Chrome, tap **⋮**, then **Install app** (or **Add to Home screen**).

## Host your own copy

This app is meant to outlive any one person or website. If the link above ever stops working, anyone can put it back online for free:

1. Download this repository (**Code → Download ZIP**).
2. Upload the `docs` folder to any static host. For example, drag the folder onto https://app.netlify.com/drop, or fork this repo and turn on GitHub Pages from the `docs` folder.

Progress is stored on each person's phone, so a new copy starts fresh. People can move across using the backup code in Settings.

## For developers

- `src/app.html` holds the whole app in one file.
- `python3 build.py` builds the installable site (manifest, offline service worker and icons) into `docs/`. It needs Pillow.

## A note on the rulings

The counts are an estimate to help people plan. The prayer guidance follows common Hanafi practice, with the other three madhabs supported for the count. For questions about your own situation, ask a trusted imam. Corrections from people of knowledge are very welcome. Please open an issue.

## Licence

MIT. Free to use, copy, change and share. Please keep it free.
