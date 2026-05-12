# Oneiro — Live Greek Entertainment

Marketing site for Oneiro Music — Greek-American band based in Metro Detroit.

## What's here

- **`index.html`** — full single-page site: hero video, repertoire, crew, music, territory, events + booking form, follow links
- **`commission.html`** — sub-page for the studio commission service (the $3,700 / "name the song" form)
- **`images/`** — band portraits, group photo, album covers, hero poster frame
- **`video/hero.mp4`** — looped cinematic hero video (auto-plays muted)
- **`robots.txt` / `sitemap.xml`** — SEO

## Running locally

```bash
python3 -m http.server 5173 --bind 0.0.0.0
```

Then open <http://localhost:5173/>. The same server is reachable on the local network and via Tailscale (IP shown by `tailscale ip -4`).

## Dev tools

The bottom-right tweaks toolbar (palette / display font / Greek headline / motion) is hidden by default. Append `?dev=1` to any URL to reveal it.

## Deployment

The site is purely static — drop it on any web host that serves files:

- **Vercel / Netlify** — connect the GitHub repo, set the publish directory to `/`, no build command
- **GitHub Pages** — push to `main`, enable Pages from repo settings, source `/`
- **Cloudflare Pages** — same as Vercel/Netlify, static
- **Old-school FTP** — upload the whole folder

After deploy, update the `og:url` and `og:image` URLs in the `<head>` of `index.html` and `commission.html` to match the live domain if it isn't `oneiromusic.com`.

## Production TODOs (the parts I can't do for you)

1. **Wire up form submissions.** Both the booking form (`#booking` in `index.html`) and the commission form (`#remake` in `commission.html`) currently `preventDefault` and show a "Got it" confirmation but don't send anywhere. Easiest path:
   - **Formspree** (free tier OK for low volume): replace `<form id="booking" class="fm" data-form="booking">` with `<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST" class="fm" data-form="booking">` and remove the `preventDefault` in the script block
   - **Netlify Forms** (free if hosted on Netlify): add `netlify` attribute on the `<form>` and Netlify auto-captures
   - **Custom**: any backend that accepts a POST
2. **Replace placeholder images.** The four crew portraits + the group/hero photo were pulled from the band's existing Wix site; album art is from there too. If higher-resolution originals exist, swap them into `/images/` keeping the same filenames.
3. **Spotify URL.** The "Spotify ↗" links currently point to `#` — wire up the real Spotify artist URL once the catalog is on there.
4. **Verify the commission section content** with the band before publishing — the $3,700 fee + "daughter as trade" joke + the P.S. notes in the repertoire section (drummer joke, μουνί joke, joint-after-the-gig joke) are intentionally edgy and personal. Make sure everyone in the band is on board.
5. **Optional polish**:
   - Higher-res hero video (the current is 720p; if generating a 1080p replacement, drop it at `/video/hero.mp4`, keep the same filename)
   - A real press kit page at `/press` with photos, logo files, stage plot, tech rider
   - Email newsletter signup (currently no list)

## Tech

- Plain static HTML/CSS/JS — no build step, no dependencies
- Google Fonts: Big Shoulders Display, Geist, JetBrains Mono, Cormorant Garamond
- Apple Music embeds for the discography section
- Hero video generated via [KIE.ai](https://kie.ai) Veo 3 image-to-video
