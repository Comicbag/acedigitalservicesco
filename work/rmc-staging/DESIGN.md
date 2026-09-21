# Design

## Visual theme

A rental yard's spec sheet, not an events agency brochure. Light page, one committed colour: the orange RMC Staging already uses on every button and heading of its current site (#fd5521, sampled from the live page 2026-09-20). Orange carries the brand the way a safety label does: solid blocks with near-black text on them, never white text on orange (that pair is 2.9:1 and fails AA). Charcoal bands hold the specs like the rating plate on the side of the truss. Photos are their real stage at real events.

Colour strategy: Committed. Orange on 30 to 40 percent of the surface (hero band, spec plates, the quote block), charcoal and off-white for the rest.

## Palette (light, default)

| Token | Value | Use |
|---|---|---|
| --paper | #f4f4f2 | page ground (chroma 0 off-white, not cream) |
| --panel | #ffffff | cards, form fields |
| --ink | #141410 | headings, body on light |
| --body | #2a2a26 | running text |
| --muted | #5c5c57 | captions, hints (AA on paper) |
| --line | #d8d8d4 | rules, borders |
| --charcoal | #1d1d19 | spec bands, footer |
| --charcoal-2 | #2a2a25 | raised surface inside charcoal bands |
| --orange | #fd5521 | brand, buttons, key numbers on dark |
| --orange-deep | #d8410f | hover, orange text on light where 3:1 large text allows |
| --on-orange | #141410 | text on orange |

## Palette (dark)

Same roles: --paper #141410, --panel #1d1d19, --ink #f2f2ee, --body #d6d6d0, --muted #a1a19a, --line #34342f, --charcoal #0d0d0b, --charcoal-2 #1a1a17, orange unchanged (orange on the dark ground is 6.9:1). Dark tokens are redefined under prefers-color-scheme and [data-theme], never defined only there.

## Typography

- Display: Big Shoulders Display 800/900. Condensed, industrial, Chicago signage lineage. Headlines and the big spec numbers. Letter-spacing no tighter than -0.02em. Hero clamp max 5.5rem.
- Body: Chivo 400/500/700. A sturdy grotesque with a wide stance, so it contrasts with the condensed display on the width axis. Running text at 1.05rem, 65ch max.
- No mono. Spec numbers use Chivo with tabular figures.
- Fonts load from Google Fonts with display=swap and system fallbacks (Impact-free: fallback for display is Arial Narrow / system condensed, then sans-serif).

## Components

- Buttons: one radius system, 4px everywhere (inputs, cards, buttons). Primary = orange fill, near-black text, 700 weight; hover = orange-deep; active scale(.97). Ghost = 1px ink border. One call to action wording site wide: "Get a quote".
- Spec plate: charcoal band, display numbers in orange, unit labels in muted. Used on Stage, Truss and Generator.
- Gear card: white panel, 4px radius, product image with its source marked ("manufacturer photo"), model name, quantity, one line of what it is for.
- Photo figure: full-bleed or split, 1px line, caption below the image, never overlaid.
- Nav: 68px, logo left, five items, orange "Get a quote" pill at the right. Collapses to a burger under 900px.
- Forms: label above input, 4px radius, orange focus ring, required marked with an orange asterisk, note at the top of the form.

## Layout

Wrap 1180px, side gutter clamp(18px, 4vw, 40px). Section rhythm alternates paper / charcoal / paper with clamp(56px, 8vw, 110px) vertical space. Hero is a real photo of the stage with a left-aligned headline block sitting on an orange plate. Spec sections are a two column split (photo, spec plate) that swaps sides once, then the page breaks the pattern with a full-width gear grid and a full-width use-case tile field. Mobile: everything stacks to one column, spec numbers stay large.

## Motion

Reveal on scroll from a visible resting state (opacity .001 to 1, 18px rise, 500ms, ease-out-quint), staggered inside a group by 40ms. Buttons scale to .97 on press over 140ms. Nothing loops. Everything under prefers-reduced-motion collapses to instant.

## Imagery rules

Their photos first (stage at Garwood Rocks, truss, band on stage). Manufacturer press images for gear they have no photo of, each labelled. No stock, no generated imagery, no illustrations. Logos: their own RMC Staging mark from the site header; partner logos as captured from their site, in a plain row with no captions.
