(function () {
  document.querySelectorAll("img").forEach(function (img) {
    function hide() {
      var box = img.closest("figure, a.project");
      if (box) box.classList.add("is-missing");
      else img.hidden = true;
    }
    img.addEventListener("error", hide);
    if (img.complete && img.naturalWidth === 0) hide();
  });
})();

(function () {
  var dialog = document.querySelector("[data-lightbox]");
  if (!dialog) return;

  var img = dialog.querySelector("img");
  var closeBtn = dialog.querySelector("[data-close]");

  document.querySelectorAll("[data-full]").forEach(function (button) {
    button.addEventListener("click", function () {
      var source = button.querySelector("img");
      img.src = button.getAttribute("data-full");
      img.alt = source ? source.alt : "";
      dialog.showModal();
    });
  });

  closeBtn.addEventListener("click", function () {
    dialog.close();
  });

  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener("close", function () {
    img.removeAttribute("src");
    img.alt = "";
  });
})();

(function () {
  var video = document.querySelector("video[data-promo]");
  if (!video) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.removeAttribute("autoplay");
    video.pause();
  }
})();
