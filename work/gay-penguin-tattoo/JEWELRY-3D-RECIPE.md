# Jewelry → 3D — LOCKED RECIPE (Gay Penguin piercing try-on)

The proven, best-settings pipeline for turning a faithful 2D piece image into a clean, accurate 3D model.
Validated on the bunny clicker + green navel (Corey-approved). Use this for every piece, current + future.

## Pipeline
faithful 2D piece  →  modeling-optimized view(s)  →  Meshy (meshy-6)  →  display in a bright three.js env

## 1. INPUT image(s) — build them FOR the engine
- ONE piece per image, **centered, FILLING the frame** (thin posts/prongs/spikes need pixels or they melt — do NOT pad).
- **Strong 3/4 angle** lead view (flat-front loses depth). Steeper angle for harder pieces. **EXCEPTION — thin open rings/hoops/clickers: use a near FACE-ON view (slight tilt only).** A steep angle shows the ring's near + far tube as two separate arcs and Meshy splays it into a multi-arc claw (black-hoop bug; the bunny clicker worked *because* it was face-on).
- **MATTE, evenly/diffusely lit** — NO harsh specular/glare. (Reflective metal is the #1 failure; baked glare becomes fake geometry. Matte the INPUT; restore shine at display via PBR.)
- **Tiny metal parts (prongs, claws, small balls): label them BRIGHT LIGHT SILVER explicitly** in the input + texture_prompt. Plain "matte" bakes small parts near-BLACK (the medusa-prong bug, fixed in one re-pass). Matte the big surfaces; keep small metal bright.
- Background: transparent PNG or solid white/neutral-grey, strong contrast for thin silver parts.
- Resolution: 1040px floor, **2048px+ ideal**. Sharp, no blur/text/particles. PNG ≤20MB.
- Keep our clean synthetic renders as-is (don't over-enhance).

## 2. MULTI-IMAGE = the biggest fidelity lever
Single-image hallucinates the unseen back/side → exactly what broke barbells / clickers / curved navels.
- Endpoint: `POST https://api.meshy.ai/openapi/v1/multi-image-to-3d`, Bearer `~/.openclaw/meshy-key.txt`.
- 2-4 **matched** views (front + back + left + right; top for tall pieces). >4 ignored. ALL views must share
  identical scale / matte even lighting / distance / one-object.
- We have one source per piece → generate consistent extra views via Gemini (reliable for simple/symmetric
  pieces; for ornate/asymmetric, prefer real multi-angle photos from Brian). Single-image is the fallback.

## 3. Meshy request body (max faithfulness)
```json
{
  "image_urls": ["<3/4 front matte>", "<side>", "<back/top>"],   // or "image_url" for single-image fallback
  "ai_model": "meshy-6",            // pin explicit (NOT "latest"); meshy-4 retired, meshy-5 a gen behind
  "should_remesh": true,            // REQUIRED on meshy-6 or topology/polycount are SILENTLY IGNORED
  "topology": "triangle",           // best for faceted gems + web GLB
  "target_polycount": 100000,       // 50k-100k; 200k for ornate clickers/spikes. Default 30k melts prongs/facets
  "should_texture": true,
  "enable_pbr": true,               // metallic/roughness/normal — lets steel+gems react to light
  "hd_texture": true,               // 4K base color (meshy-6) — captures facets, engraving, logo
  "texture_prompt": "<exact piece: metal finish + EXACT gem count + colors>",   // <=600 chars; gem count fixes duplication
  "target_formats": ["glb"]
}
```
Leave meshy-6 defaults ON: `remove_lighting=true` (strips baked glare). `image_enhancement=false` (clean renders).
DO NOT SEND: `symmetry_mode` (dead no-op since May 2026), `decimation_mode` (overrides polycount),
pose_mode/is_a_t_pose (characters), `texture_image_url` (mutually exclusive w/ texture_prompt).
Run strategy: **no refine button — each run varies, generate 2-4x and pick best.** Texture-only fix on a good
mesh → Retexture API (enable_pbr + remove_lighting + enable_original_uv), not a re-roll. CONFIRMED endpoint: `POST /openapi/v1/retexture` {input_task_id, ai_model:"meshy-6", text_style_prompt, enable_pbr:true, remove_lighting:true, enable_original_uv:true}. (Can misfire on simple pieces — for plain metal prefer the display override, precaution 14.)
QA: `multi_view_thumbnails=true` (front/right/back/left renders) to instantly verify back/side faithfulness.

## 4. DISPLAY (three.js / GLB) — makes silver read as silver
- `scene.environment` is **MANDATORY** — a metalness-1 surface with NO env map renders pure BLACK
  (this was our "black metal" bug). Default: `RoomEnvironment` via `PMREMGenerator`. Upgrade: 1k studio HDRI.
- `renderer.toneMapping = ACESFilmicToneMapping`, `toneMappingExposure = 1.0–1.2`.
- `outputColorSpace = SRGBColorSpace` (color management ON).
- `material.envMapIntensity = 1.5–2.5` on metal (push silver bright without blowing out gems).
- Trust Meshy PBR; only override metalness=1.0 / roughness=0.15–0.3 if metal reads dull.
- Bright viewer = `_brightview.html`; dim = `_mview.html`.

## 5. PRECAUTIONS (failure modes → fixes)
1. **Gem duplication/miscount** → exact gem count in texture_prompt + clean even-lit input + multi-image (NOT symmetry_mode, which is dead).
2. **Pin meshy-6 explicitly** (not "latest"; meshy-5 lacks hd_texture/remove_lighting).
3. **should_remesh MUST be true** on meshy-6 or polycount/topology are ignored.
4. Never send decimation_mode (overrides polycount).
5. **Melted thin parts** (posts/prongs/tips) → polycount 50k-100k+ AND fill the frame (don't pad).
6. **Reflective metal** → matte the INPUT; recover shine at display via PBR + env map, never baked highlights. **Specular HOTSPOTS / black dots / dark reflection spots in the input BAKE onto the model as real surface color** (Corey caught this on the horseshoe balls). INSPECT the optimized input and scrub any dark dots (even-matte re-pass) BEFORE Meshy — part of double-checking every input.
7. No refine pass → generate 2-4x, pick best; Retexture API for texture-only fixes.
8. image_enhancement OFF for clean renders (ON only for messy real photos).
9. texture_prompt XOR texture_image_url (prompt wins for jewelry).
10. Multi-image: one object/image, identical scale+lighting+distance; >4 ignored.
11. **Black render = display bug** (no scene.environment), NOT a bad mesh. Set RoomEnvironment first.
12. **Tiny parts bake dark** (prongs/claws/small balls) → label them BRIGHT LIGHT SILVER in the input + texture_prompt; "matte" alone is for large surfaces. (Medusa prongs fixed in one re-pass.)
13. **Rings/hoops splay into a multi-arc claw** at a steep angle → render them near FACE-ON (slight tilt), exactly the opposite of the steep-angle rule for everything else. (Black hoop failed at 3/4, fixed face-on.)
15. **Meshy bakes a faint RED/warm tint into the texture** of bright/gem pieces (its texturing AI invents it — verified: source, fed-in image, and viewer all neutral). For SILVER+CLEAR pieces, neutralize: extract the baseColorTexture from the GLB, desaturate to grey, re-apply as `.map` via `_retex.html?m=…&tex=…`. Confirmed on nostril CZ (mean red-bias +37 → 0).
14. **Plain-metal pieces (no gems) → OVERRIDE the material at display** to uniform silver/gold/black (`MeshStandardMaterial` metalness 1.0, roughness ~0.18, envMapIntensity ~1.7) via `_silver.html?m=…&c=hex`. The geometry is what matters; forcing the colour sidesteps baked-texture roulette — stray red/warm tints and black thin posts (the silver-ball fight: re-rolls + retexture all failed; override won instantly). Gem / multi-colour pieces still keep their baked texture.

## Keys
- Meshy: `~/.openclaw/meshy-key.txt` (msy_…)  · Gemini: `GEMINI_API_KEY` in `~/.openclaw/.env`  · fal/Rodin: `~/.openclaw/rodin-key.txt`
