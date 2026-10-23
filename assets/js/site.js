// TARS site: theme toggle, mobile menu, scroll reveal, contact form (mailto, no backend).
(function () {
  const root = document.documentElement;
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  // theme: dark is the brand default; the choice is remembered per visitor
  const themeBtn = document.querySelector("[data-theme-toggle]");
  const paintIcon = () => {
    if (!themeBtn) return;
    const light = root.dataset.theme === "light";
    themeBtn.innerHTML = `<i class="ph ${light ? "ph-moon" : "ph-sun"}" aria-hidden="true"></i>`;
    themeBtn.setAttribute("aria-label", light ? "Switch to dark theme" : "Switch to light theme");
  };
  paintIcon();
  themeBtn && themeBtn.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    store.set("tars-theme", next);
    paintIcon();
  });

  // mobile menu
  const menuBtn = document.querySelector("[data-menu]");
  const links = document.querySelector(".nav-links");
  menuBtn && menuBtn.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.innerHTML = `<i class="ph ${open ? "ph-x" : "ph-list"}" aria-hidden="true"></i>`;
  });

  // reveal on scroll (IntersectionObserver, no scroll listeners)
  const items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach((el) => io.observe(el));
  } else {
    items.forEach((el) => el.classList.add("in"));
  }

  const year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  // contact form: validates, then opens the visitor's mail app with the message filled in
  const form = document.querySelector("form[data-mailto]");
  if (form) {
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      let ok = true;
      form.querySelectorAll("[required]").forEach((input) => {
        const field = input.closest(".field");
        const valid = input.type === "email" ? /\S+@\S+\.\S+/.test(input.value) : input.value.trim().length > 1;
        field.classList.toggle("invalid", !valid);
        if (!valid && ok) { input.focus(); ok = false; }
      });
      if (!ok) return;
      const v = (name) => (form.elements[name] ? form.elements[name].value.trim() : "");
      const subject = `TARS: ${v("topic") || "Hello"} from ${v("name")}${v("company") ? ", " + v("company") : ""}`;
      const body = `${v("message")}\n\n${v("name")}\n${v("email")}${v("company") ? "\n" + v("company") : ""}`;
      window.location.href = `mailto:${form.dataset.mailto}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      const note = form.querySelector("[data-sent]");
      if (note) note.hidden = false;
    });
  }
})();
