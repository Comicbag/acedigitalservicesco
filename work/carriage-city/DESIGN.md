# Design

## Visual theme

A playbill for a carriage house. The page is their slate navy (#2d4b62, sampled from carriagecitystudios.com) with their amber gold (#f2ac57) as the single accent, exactly as their crest uses them. Deliberately single theme: the brand is navy, so the page is navy in light and dark mode alike, and every colour is painted explicitly.

Colour strategy: Drenched. Navy is the surface; gold is for the crest, rules, key words and buttons.

## Palette

| Token | Value | Use |
|---|---|---|
| --navy | #2d4b62 | page ground (theirs) |
| --navy-deep | #1f3647 | bands, footer, panels |
| --navy-lift | #365a74 | raised panels, inputs |
| --gold | #f2ac57 | accent, buttons, crest (theirs) |
| --gold-deep | #d98f36 | hover |
| --ivory | #f7efe2 | headings and body on navy |
| --ivory-dim | #d9d3c7 | secondary text |
| --line | rgba(242,172,87,.28) | gold hairlines |

Contrast: ivory on navy 9.3:1; gold on navy 4.6:1; navy on gold 4.6:1 (button labels are bold, well above the large-text bar).

## Typography

Their own two families, kept: Libre Baskerville (display, 400 and 700, italic for "Follow The Noise") and Nunito Sans (body and UI). Small caps with letter-spacing for short labels, used rarely.

## Components

- Buttons: gold fill, navy text, square corners like their current buttons, 2px radius. Ghost: 1px gold border, ivory text.
- Frame: a thin double gold rule with corner ticks, echoing the crest border, used around the hero crest and the enquiry panel only.
- Forms: ivory labels above navy-lift inputs, gold focus ring, gold asterisk for required.
- Cards: navy-deep panels with a 1px gold hairline, 2px radius. Used for the three doors (Record, Events, Lessons and rentals) only.

## Layout

Wrap 1120px. Hero centres the crest (their logo is symmetrical and centred on their site; identity wins over anti-centre bias). Below it the page alternates left-aligned splits and full-width bands. Mobile stacks to one column.

## Motion

Reveal on scroll from a visible resting state, 500ms ease-out; buttons press to .97. Reduced motion: none.
