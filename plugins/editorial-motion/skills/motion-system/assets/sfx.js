/* ============================================================
   sfx.js — procedural sound design for generated artifacts

   The reference set's sound grammar IS its timing grammar (sources.md
   §14, §15). This encodes the grammar, not just the sounds:

     ONE ACCENT     exactly one impact per scene, spent on the single
                    most important moment. Everything else is quiet.
     J-CUT          sound leads picture by ~100-150ms — "it helps
                    people's brains prep for the scene".
     DESYNC         cues land a frame or so off the visual on purpose.
                    Everything hitting one frame is a tell.
     LEVELS         SFX -20..-10 dBFS, bed -20 dBFS. Enforced, not
                    advisory.
     STACK          a movement is gesture + substance — whoosh plus
                    the material it moves through.

   Everything is synthesised with Web Audio. No sample library, no
   licensing, nothing to download, ~6KB.

   MUTED BY DEFAULT. Audio that starts on its own is hostile, and
   browsers block it anyway. Call enable() from a real click.

   Usage
   -----
     const sfx = AnalogSFX();
     sfx.attachToggle(document.querySelector('#sound'));

     sfx.play('whoosh');
     sfx.play('paper', { gain: -18 });

     sfx.scene([
       { at: 0,    sound: 'tick' },
       { at: 220,  sound: 'paper' },
       { at: 900,  sound: 'impact', accent: true },  // only one allowed
     ]);
   ============================================================ */

function AnalogSFX(options) {
  const opt = Object.assign({
    fps: 12,              // house posterize rate; desync is measured in frames
    desyncFrames: 1,      // +/- this many frames of deliberate slop
    jcutMs: 120,          // how far sound leads picture
    seed: 1,              // deterministic variation
    muted: true,
    bedGain: -20,         // dBFS, per the reference mix
    sfxRange: [-20, -10], // dBFS floor/ceiling for one-shots
  }, options || {});

  let ctx = null, master = null, bedNode = null;
  let muted = opt.muted;
  let seed = opt.seed >>> 0;

  /* Deterministic RNG. Variation must be reproducible or the same artifact
     sounds different on every load, and a rendered video will not match a
     preview. */
  function rnd() {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 4294967296;
  }
  const between = (lo, hi) => lo + (hi - lo) * rnd();
  const dbToGain = db => Math.pow(10, db / 20);

  /* Per-voice calibration, in dB.

     A gain value is not an output level. Each voice runs through filters that
     attenuate it by a different amount — tick's high-Q band-pass throws away
     most of a noise burst, impact's two layers sum — so an identical requested
     gain came out anywhere from -27 to -14 dBFS. Measured with sfx-test.html
     and corrected here, so `gain: -14` means -14 dBFS at the output for every
     voice. Re-measure if a voice's filter chain changes. */
  const TRIM = { whoosh: 6.5, paper: 4.7, tick: 13.4, tech: 4.6, impact: -0.6 };
  const clampDb = db => Math.min(opt.sfxRange[1],
                                 Math.max(opt.sfxRange[0], db));

  function ensure() {
    if (ctx) return ctx;
    const AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) return null;
    ctx = new AC();
    master = ctx.createGain();
    master.gain.value = muted ? 0 : 1;
    // Safety net, not a sound-design choice: stops a stack of simultaneous
    // cues from clipping if a scene is denser than it should be.
    const limiter = ctx.createDynamicsCompressor();
    limiter.threshold.value = -6;
    limiter.ratio.value = 12;
    limiter.attack.value = 0.002;
    limiter.release.value = 0.12;
    master.connect(limiter).connect(ctx.destination);
    return ctx;
  }

  function noiseBuffer(dur) {
    const n = Math.max(1, Math.floor(ctx.sampleRate * dur));
    const buf = ctx.createBuffer(1, n, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < n; i++) d[i] = rnd() * 2 - 1;
    return buf;
  }

  function env(node, t0, dur, peak, attack) {
    const g = node.gain;
    g.setValueAtTime(0.0001, t0);
    g.exponentialRampToValueAtTime(Math.max(0.0002, peak), t0 + attack);
    g.exponentialRampToValueAtTime(0.0001, t0 + dur);
  }

  /* ---------- the six folders ---------- */

  const VOICES = {
    /* whooshes — any movement. Noise through a swept band-pass. */
    whoosh(t0, db) {
      const dur = between(0.26, 0.4);
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(dur);
      const bp = ctx.createBiquadFilter();
      bp.type = 'bandpass';
      bp.Q.value = between(0.7, 1.2);
      const lo = between(260, 380), hi = between(2000, 2900);
      bp.frequency.setValueAtTime(lo, t0);
      bp.frequency.exponentialRampToValueAtTime(hi, t0 + dur * 0.45);
      bp.frequency.exponentialRampToValueAtTime(lo * 1.2, t0 + dur);
      const g = ctx.createGain();
      env(g, t0, dur, dbToGain(db), dur * 0.3);
      src.connect(bp).connect(g).connect(master);
      src.start(t0); src.stop(t0 + dur + 0.02);
    },

    /* tactile — paper, cloth. Short bright noise burst, fast decay. */
    paper(t0, db) {
      const dur = between(0.09, 0.16);
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(dur);
      const bp = ctx.createBiquadFilter();
      bp.type = 'bandpass';
      bp.frequency.value = between(2200, 5200);
      bp.Q.value = between(0.6, 1.1);
      const hp = ctx.createBiquadFilter();
      hp.type = 'highpass'; hp.frequency.value = 900;
      const g = ctx.createGain();
      env(g, t0, dur, dbToGain(db), 0.004);
      src.connect(bp).connect(hp).connect(g).connect(master);
      src.start(t0); src.stop(t0 + dur + 0.02);
    },

    /* mechanical — ticks, clicks, marker, stopwatch. */
    tick(t0, db) {
      const dur = between(0.025, 0.045);
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(dur);
      const bp = ctx.createBiquadFilter();
      bp.type = 'bandpass';
      bp.frequency.value = between(1400, 3000);
      bp.Q.value = between(4, 6);   // narrow range: high Q swings the peak hard
      const g = ctx.createGain();
      env(g, t0, dur, dbToGain(db), 0.001);
      src.connect(bp).connect(g).connect(master);
      src.start(t0); src.stop(t0 + dur + 0.02);
    },

    /* tech — UI blip, digital. */
    tech(t0, db) {
      const dur = between(0.05, 0.085);
      const osc = ctx.createOscillator();
      osc.type = 'square';
      const f = between(620, 1050);
      osc.frequency.setValueAtTime(f, t0);
      osc.frequency.exponentialRampToValueAtTime(f * 0.6, t0 + dur);
      const lp = ctx.createBiquadFilter();
      lp.type = 'lowpass'; lp.frequency.value = 4200;
      const g = ctx.createGain();
      env(g, t0, dur, dbToGain(db) * 0.5, 0.003);
      osc.connect(lp).connect(g).connect(master);
      osc.start(t0); osc.stop(t0 + dur + 0.02);
    },

    /* the accent. One per scene, on the single most important moment. */
    impact(t0, db) {
      const dur = between(0.38, 0.5);
      const osc = ctx.createOscillator();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(between(90, 120), t0);
      osc.frequency.exponentialRampToValueAtTime(38, t0 + dur);
      const og = ctx.createGain();
      env(og, t0, dur, dbToGain(db), 0.006);
      osc.connect(og).connect(master);
      osc.start(t0); osc.stop(t0 + dur + 0.02);

      const src = ctx.createBufferSource();       // transient on top
      src.buffer = noiseBuffer(0.06);
      const bp = ctx.createBiquadFilter();
      bp.type = 'bandpass'; bp.frequency.value = between(1600, 2600);
      const ng = ctx.createGain();
      env(ng, t0, 0.06, dbToGain(db) * 0.4, 0.002);
      src.connect(bp).connect(ng).connect(master);
      src.start(t0); src.stop(t0 + 0.09);
    },
  };

  /* ---------- scheduling ---------- */

  function desyncMs() {
    if (!opt.desyncFrames) return 0;
    const frame = 1000 / opt.fps;
    return between(-opt.desyncFrames, opt.desyncFrames) * frame;
  }

  /* Every cue is logged whether or not it sounds. An offline render has no
     user gesture, so audio is always muted there — logging after the mute
     guard would mean a rendered video comes out silent with nothing to say
     why. render.py reads this log to mux the real thing. Because the desync
     comes from the seeded RNG, the log and a live playback of the same
     artifact agree on where the cue lands. */
  function cueLog() {
    if (typeof window === 'undefined') return [];
    return (window.__analogSFXCues = window.__analogSFXCues || []);
  }

  function play(name, o) {
    o = o || {};
    const voice = VOICES[name];
    if (!voice) { console.warn(`AnalogSFX: no voice "${name}"`); return false; }

    const slop = o.exact ? 0 : desyncMs();
    const lead = o.jcut ? -opt.jcutMs : 0;
    const at = Math.max(0, (o.at || 0) + slop + lead);
    const gain = o.gain === undefined ? -14 : o.gain;
    /* The requested gain, before clamp and per-voice trim — those belong to
       the voice and get applied again at render time. Logging the trimmed
       value would apply the trim twice. */
    cueLog().push({ sound: name, at: at, gain_db: gain, accent: !!o.accent });

    if (!ensure() || muted) return false;
    if (ctx.state === 'suspended') ctx.resume();
    voice(ctx.currentTime + at / 1000, clampDb(gain) + (TRIM[name] || 0));
    return true;
  }

  /* A scene, with the one-accent rule enforced rather than documented.
     Extra accents are demoted, not dropped — silence where a designer
     expected a hit is more confusing than a quieter hit. */
  function scene(cues) {
    let accentUsed = false;
    const warnings = [];
    (cues || []).forEach((c, i) => {
      let gain = c.gain;
      if (c.accent) {
        if (accentUsed) {
          warnings.push(`cue ${i} ("${c.sound}") is a second accent — `
                      + `demoted. One accent per scene.`);
          gain = gain === undefined ? -18 : gain;
        } else {
          accentUsed = true;
          gain = gain === undefined ? -10 : gain;
        }
      }
      play(c.sound, { at: c.at, gain: gain, jcut: c.jcut, exact: c.exact,
                      accent: !!c.accent });
    });
    warnings.forEach(w => console.warn('AnalogSFX: ' + w));
    return warnings;
  }

  function bed(on) {
    if (!ensure()) return;
    if (on && !bedNode) {
      const src = ctx.createBufferSource();
      src.buffer = noiseBuffer(2.0);
      src.loop = true;
      const lp = ctx.createBiquadFilter();
      lp.type = 'lowpass'; lp.frequency.value = 620;
      const g = ctx.createGain();
      g.gain.value = dbToGain(opt.bedGain);
      src.connect(lp).connect(g).connect(master);
      src.start();
      bedNode = { src, g };
    } else if (!on && bedNode) {
      bedNode.src.stop();
      bedNode = null;
    }
  }

  function setMuted(m) {
    muted = !!m;
    if (master) master.gain.value = muted ? 0 : 1;
    if (!muted && ctx && ctx.state === 'suspended') ctx.resume();
    return muted;
  }

  function attachToggle(el) {
    if (!el) return;
    const paint = () => {
      el.setAttribute('aria-pressed', String(!muted));
      el.textContent = muted ? 'Sound off' : 'Sound on';
    };
    el.addEventListener('click', () => { ensure(); setMuted(!muted); paint(); });
    paint();
  }

  const api = {
    play, scene, bed, attachToggle,
    enable: () => { ensure(); return setMuted(false); },
    disable: () => setMuted(true),
    get muted() { return muted; },
    get context() { return ctx; },
    voices: Object.keys(VOICES),
    _internals: { VOICES, dbToGain, clampDb, ensure: () => ctx },
    /* Render one voice into an OfflineAudioContext and hand back the buffer.
       Used by the level test — see sfx-test.html. */
    render(name, db, seconds) {
      const OAC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      const off = new OAC(1, Math.ceil(44100 * (seconds || 1)), 44100);
      const saveCtx = ctx, saveMaster = master, saveMuted = muted;
      ctx = off;
      master = off.createGain();
      master.gain.value = 1;
      master.connect(off.destination);
      muted = false;
      VOICES[name](0, clampDb(db === undefined ? -14 : db) + (TRIM[name] || 0));
      const done = off.startRendering();
      ctx = saveCtx; master = saveMaster; muted = saveMuted;
      return done;
    },

    /* The same render, encoded as a base64 16-bit WAV. render.py pulls voices
       out this way and hands the files to mix_sfx.py: the levels stay here,
       where the -20..-10 dBFS window and the per-voice trim are decided, and
       the placement stays in the mixer. Nothing has to agree about gain twice. */
    renderWav(name, db, seconds) {
      return this.render(name, db, seconds).then(function (buf) {
        const n = buf.length, data = buf.getChannelData(0);
        const bytes = new ArrayBuffer(44 + n * 2), view = new DataView(bytes);
        const ascii = (off, s) => {
          for (let i = 0; i < s.length; i++) view.setUint8(off + i, s.charCodeAt(i));
        };
        ascii(0, 'RIFF'); view.setUint32(4, 36 + n * 2, true); ascii(8, 'WAVE');
        ascii(12, 'fmt '); view.setUint32(16, 16, true);
        view.setUint16(20, 1, true); view.setUint16(22, 1, true);
        view.setUint32(24, buf.sampleRate, true);
        view.setUint32(28, buf.sampleRate * 2, true);
        view.setUint16(32, 2, true); view.setUint16(34, 16, true);
        ascii(36, 'data'); view.setUint32(40, n * 2, true);
        for (let i = 0; i < n; i++) {
          const s = Math.max(-1, Math.min(1, data[i]));
          view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
        }
        let bin = '';
        const raw = new Uint8Array(bytes);
        for (let i = 0; i < raw.length; i += 0x8000) {
          bin += String.fromCharCode.apply(null, raw.subarray(i, i + 0x8000));
        }
        return btoa(bin);
      });
    },
  };

  /* Last instance wins. render.py needs a handle to reach renderWav, and
     artifacts keep their instance in a local const. */
  if (typeof window !== 'undefined') window.__analogSFX = api;
  return api;
}

if (typeof module !== 'undefined' && module.exports) module.exports = AnalogSFX;
