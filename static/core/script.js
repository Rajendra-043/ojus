// OJAS 2026 — small progressive enhancement.
// Forms POST normally to Django; this adds fetch + live "What's New" refresh.
(function () {
  async function postForm(form, url) {
    const data = new FormData(form);
    const payload = Object.fromEntries(data.entries());
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return res.json();
  }
  function hook(id, url, okMsg) {
    const form = document.getElementById(id);
    if (!form) return;
    form.addEventListener("submit", async (e) => {
      if (!window.fetch) return; // let normal POST happen
      e.preventDefault();
      const note = document.createElement("div");
      note.className = "msg";
      note.textContent = "Sending...";
      form.prepend(note);
      try {
        const out = await postForm(form, url);
        note.textContent = out.ok ? okMsg : "Error: " + JSON.stringify(out.errors || out);
        if (out.ok) form.reset();
      } catch (err) {
        note.textContent = "Network error. Try normal submit.";
      }
    });
  }
  document.addEventListener("DOMContentLoaded", () => {
    hook("register-form", "/api/register/", "Registered! See you at OJAS 2026.");
    hook("feedback-form", "/api/feedback/", "Thanks for your feedback!");
    // Live refresh What's New cards if API has newer data
    const grid = document.getElementById("updates-grid");
    if (grid && window.fetch) {
      fetch("/api/updates/").then((r) => r.json()).then((d) => {
        if (!d.updates || !d.updates.length) return;
        grid.innerHTML = d.updates.map((u) =>
          `<div class="card"><h3>\u25a0 ${u.title}</h3><p>${u.description}</p></div>`
        ).join("");
      }).catch(() => {});
    }
  });
})();
