# Design

## Theme
Dark, locked. Body oklch(14% 0.005 240) (#0e1012), raised surfaces #131619 and #191d21, hairlines
at 10 to 22 percent bone. One accent: hunter orange #e07f36 (hover #f0955a), used on the ampersand,
step numerals, the primary button and stars (#f2b64a). Text: bone #f2efe8, secondary #d6d2c9,
muted #9d988f.

## Typography
Display: Cinzel 700 (matches the serif caps on the shop's own signage), clamp(2.4rem, 5.4vw, 4.6rem)
for h2, hero h1 clamp(3.6rem, 9.2vw, 6rem). Body: IBM Plex Sans 400/500/600 at 17px, line height 1.6.
Kickers and specs: IBM Plex Mono 400/500 at 12.8px, letter spacing 0.14em, uppercase, used only for
"Posted <date>" and "In the case" labels. Fonts self hosted (variable woff2 in /fonts).

## Layout
Max width 1360px, gutters clamp(18px, 4.5vw, 56px). Editorial catalog: feature spreads (photo beside
copy, alternating) and rows of three or two, every photo box in the image's own aspect ratio.
Header 72px sticky with blur. Sticky Call / Directions bar on phones. Radius 2px everywhere.

## Motion
Ease cubic-bezier(.16,1,.3,1). Reveals 800ms fade and 22px rise on scroll, staggered 80ms. Hero copy
rises on load. Photos scale 1.035 on hover over 900ms. Buttons scale .985 on press. Marquee 46s linear,
paused on hover, static list under reduced motion.

## Components
Photo link (.ph) with hover "Enlarge" chip and lightbox. Feature (.feat), row (.trio, .duo), glossary
(dl with hairline rows), numbered steps, review cards in the Ace standard structure, hours table,
brand lockup band, brands marquee.
