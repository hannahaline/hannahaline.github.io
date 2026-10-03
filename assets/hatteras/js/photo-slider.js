// Before/after sliders for photo pairs already lined up on one frame (markup in _includes/hatteras/photo_slider.liquid).
// The right-hand photo is clipped at the divider. Safe to load more than once on a page.
(function () {
  "use strict";
  if (window.hatPhotoSlider) return;
  window.hatPhotoSlider = true;

  function start() {
    document.querySelectorAll(".hat-photo-slider").forEach(function (root) {
      var after = root.querySelector("img.after"), divider = root.querySelector(".hat-compare-divider");
      root.querySelector(".hat-compare-range").addEventListener("input", function (e) {
        after.style.clipPath = "inset(0 0 0 " + e.target.value + "%)";
        divider.style.left = e.target.value + "%";
      });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
