// Model input stepper on /hatteras/model/ (markup in _includes/hatteras/model_steps.liquid): shows one step at a time
// with Back / Next, numbered dots and the arrow keys. Without this script every step is shown in turn.
(function () {
  "use strict";

  function Steps(root) {
    var steps = root.querySelectorAll(".hat-step"), nav = root.querySelector(".hat-steps-nav");
    var dots = root.querySelector(".hat-steps-dots"), prev = root.querySelector(".hat-steps-prev"), next = root.querySelector(".hat-steps-next");
    var i = 0;
    steps.forEach(function (s, k) {
      var d = document.createElement("button");
      d.type = "button";
      d.setAttribute("role", "tab");
      d.setAttribute("aria-label", "Step " + (k + 1) + ": " + s.querySelector("h3").lastChild.textContent.trim());
      d.textContent = k + 1;
      d.addEventListener("click", function () { show(k); });
      dots.appendChild(d);
    });
    function show(k) {
      i = Math.max(0, Math.min(steps.length - 1, k));
      steps.forEach(function (s, j) { s.hidden = j !== i; });
      dots.querySelectorAll("button").forEach(function (d, j) { d.classList.toggle("on", j === i); d.setAttribute("aria-selected", j === i); });
      prev.disabled = i === 0;
      next.disabled = i === steps.length - 1;
    }
    prev.addEventListener("click", function () { show(i - 1); });
    next.addEventListener("click", function () { show(i + 1); });
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { show(i + 1); e.preventDefault(); }
      if (e.key === "ArrowLeft") { show(i - 1); e.preventDefault(); }
    });
    root.tabIndex = 0;
    nav.hidden = false;
    show(0);
  }

  function start() { document.querySelectorAll(".hat-steps").forEach(function (r) { Steps(r); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
