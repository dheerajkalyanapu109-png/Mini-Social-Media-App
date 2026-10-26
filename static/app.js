// Like/unlike without reloading; falls back to a normal form post if fetch fails.
document.querySelectorAll("form[data-like]").forEach(form => {
  form.addEventListener("submit", async e => {
    e.preventDefault();
    try {
      const res = await fetch(form.action, {method: "POST", body: new FormData(form), headers: {"x-requested-with": "fetch"}});
      const data = await res.json();
      const btn = form.querySelector("button");
      btn.classList.toggle("on", data.liked);
      btn.setAttribute("aria-pressed", data.liked);
      btn.firstChild.textContent = data.liked ? "♥ " : "♡ ";
      btn.querySelector("span").textContent = data.count;
    } catch { form.submit(); }
  });
});
