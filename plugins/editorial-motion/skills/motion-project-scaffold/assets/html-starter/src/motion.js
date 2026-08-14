(function () {
  "use strict";

  const params = new URLSearchParams(window.location.search);
  const supportedFormats = new Set(["vertical", "portrait", "square", "landscape"]);
  const requestedFormat = params.get("format");
  const format = supportedFormats.has(requestedFormat) ? requestedFormat : "landscape";
  const motion = params.get("motion") === "reduced" ? "reduced" : "full";

  document.body.dataset.format = format;
  document.body.dataset.motion = motion;
  window.__EDITORIAL_MOTION__ = Object.freeze({format, motion});
})();
