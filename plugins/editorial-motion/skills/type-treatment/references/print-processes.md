# Print-process contracts

Use this reference after choosing the type's **register**. A register describes
the relationship to the surface; a process describes how the mark was made.

## Opt-in boundary

Start with the composition's regular typeface system. These classes do not
choose a font or replace ordinary typography; they are explicit feature
modifiers for selected display elements. Never apply `.tt-process`,
`.tt-tactile-surface` or `.tt-tactile-ink` through a global selector, shared
heading primitive or root wrapper. Without one of these classes, type renders
normally.

Use standard typography for the majority of a composition. `Clean print` is the
default inside this optional feature set, not a requirement for every text
element.

## Decision order

1. Resolve the regular typeface styling and hierarchy.
2. Choose `on`, `in`, `through` or `among` for the selected feature element.
3. Name the physical or reproduction process.
4. Apply one process class to that string only.
5. Add the composition's shared grain over the completed stack.
6. Check a still at delivery size and at 200px wide.

Do not use a textured process on body copy, source lines, chart labels or a hero
figure. Keep those in clean print. Do not stack process classes on one string.

## Tactile contact stack

Tactility is a material layer beneath and above the chosen process, not another
process to stack on the string. It needs three linked parts:

1. `.tt-tactile-surface` establishes the coloured stock.
2. `.tt-tactile-ink` uses the stock's matching luma matte to create pressure
   loss inside the ink.
3. The surface's generated fibre pass runs over the completed plate so the same
   material crosses ground, ink and annotations.

```html
<article class="tt-tactile-surface" style="--tt-stock:#9C54A8">
  <div class="tt-tactile-ink tt-tactile-ink--soft">
    <span class="tt-process tt-clean-print">TOUCH</span>
  </div>
</article>
```

The included `tactile-fibre.png` and `tactile-fibre-matte.png` are a matched,
seamless pair. Keep `--tt-fibre-size` identical on the surface and ink. Raise
`--tt-fibre-opacity` only for coarse stock or large display type. The
`tt-tactile-ink--soft` edge spread is for large porous-stock titles; never apply
it to body copy.

If a process already uses a mask, keep `.tt-tactile-ink` as its wrapper. Putting
the contact class on `.tt-halftone`, `.tt-stamp` or `.tt-photocopy` would replace
that process's own mask.

## Shared markup

Use `.tt-process` with exactly one process class:

```html
<span class="tt-process tt-halftone">PRINT</span>
```

Classes that reproduce the text in a pseudo-element need `data-text`. Keep the
real text in the element and add the same string as `aria-label`; this prevents
generated copies from being announced as repeated words.

```html
<span class="tt-process tt-misregister" data-text="OFFSET"
      aria-label="OFFSET">OFFSET</span>
```

## Processes

### Clean print

Use as the default within the optional print-process set. It integrates the ink
with the surface without inventing wear. Ordinary typography outside the
feature set needs no process class.

```html
<span class="tt-process tt-clean-print">EVIDENCE</span>
```

Set `--tt-process-blend: screen` when using light ink on a dark ground.

### Halftone

Use on one or two heavy words at display size. Keep the dot screen visible but
small enough that counters remain intact.

```html
<span class="tt-process tt-halftone"
      style="--tt-halftone-step:.08em;--tt-halftone-dot:42%">PRINT</span>
```

- Use roughly 72px and above.
- Increase `--tt-halftone-step` for a coarser screen.
- Reduce `--tt-halftone-dot` when counters begin to close.

### Dry stamp

Use a generated or scanned pressure mask with isolated failures. Avoid an even
percentage of missing ink, which reads as opacity rather than contact pressure.

```html
<span class="tt-process tt-stamp"
      style="--tt-stamp-mask:url(data:image/png;base64,...)">VERIFIED</span>
```

Use the same pressure mask scale across related words. Without a supplied mask,
the class falls back to a solid, readable impression.

### Ink bleed

Use for large type printed on porous stock. Set the three bleed colours from the
actual ink; do not leave warm-black defaults on coloured type.

```html
<span class="tt-process tt-bleed"
      style="--tt-bleed-1:rgba(111,29,24,.44);
             --tt-bleed-2:rgba(111,29,24,.24);
             --tt-bleed-3:rgba(111,29,24,.12)">ABSORBED</span>
```

Use roughly 100px and above. Below that size the spread resembles a shadow.

### Photocopy

Use toner dropout and one short directional drag. Retain the original text as a
solid core.

```html
<span class="tt-process tt-photocopy" data-text="REPRODUCED"
      aria-label="REPRODUCED">REPRODUCED</span>
```

Keep `--tt-copy-drag` close to its `.018em` default and below `.025em`. A larger
offset becomes a shadow or glitch.

### Misregistered print

Use two brand-compatible spot inks on one short display word. This is a pair of
separate impressions, not the analog-surface chromatic-fringe filter.

```html
<span class="tt-process tt-misregister" data-text="OFFSET" aria-label="OFFSET"
      style="--tt-register-a:#D9274E;--tt-register-b:#168C9E">OFFSET</span>
```

- Keep `--tt-register-shift` below `.025em`.
- Use `--tt-register-blend:screen` on dark grounds.
- Never use it on body copy, data marks or multiple competing words.

### Pattern fill

Use a quiet repeating line or hatch pattern inside heavy glyphs. Keep the
pattern abstract and calm; a busy photograph belongs to the `through` register.

```html
<span class="tt-process tt-pattern-fill"
      style="--tt-pattern-step:.085em">SYSTEM</span>
```

Override `--tt-pattern` and `--tt-pattern-size` together when a custom hatch is
required. Always preserve a solid-colour fallback.

### Paper collage

Use for a foreground label or caption object. It is a plate, so do not combine
it with a glyph process class.

```html
<span class="tt-paper-label tt-paper-label--dark"
      style="--tt-label-texture:url(data:image/png;base64,...)">FIELD NOTE</span>
```

Prefer a real paper texture. The built-in irregular edge is a no-asset fallback,
not a substitute for a hero torn-paper scan. Do not add a drop shadow.

Always pair paper and ink by contrast:

- `.tt-paper-label--dark` uses warm white ink on black or very dark paper.
- `.tt-paper-label--light` uses warm black ink on beige, cream or white paper.

Use the modifier that matches the actual stock. Do not rely on inherited text
colour, because a label can move between light and dark compositions.

## Failure checks

- The process has a material explanation, not merely a style name.
- The treatment is explicitly applied to selected elements, never the global type system.
- Only one process class is present on the string.
- The texture scales with the type, not with a fixed canvas pixel value.
- The original text remains present and readable if masks or clipping fail.
- Counters and thin joins remain open at 200px-wide preview size.
- Shared plate grain still runs over the type after the process treatment.
