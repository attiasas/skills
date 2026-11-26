const sections = [...document.querySelectorAll("main > section")];
const rail = document.querySelector(".rail");
const progress = document.querySelector(".progress");

// Right rail
sections.forEach(s => {
  const a = document.createElement("a");
  a.href = "#" + s.id;
  a.innerHTML = "<span>" + s.dataset.title + "</span>";
  rail.append(a);
});
const links = [...rail.children];
const mark = i => {
  links.forEach((l, j) => l.classList.toggle("active", j === i));
  progress.style.width = ((i + 1) / sections.length * 100) + "%";
};
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) mark(sections.indexOf(e.target)); });
}, { rootMargin: "-40% 0px -50% 0px" });
sections.forEach(s => observer.observe(s));
// Dot turns red when a section holds a fail or a gap pill
sections.forEach((s, i) => { if (s.querySelector(".pill.fail, .pill.gap")) links[i].classList.add("attn"); });

// Open every collapsed ancestor of a link target, then scroll to it
function reveal() {
  const t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
  if (!t) return;
  for (let d = t.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true;
  if (t.tagName === "DETAILS") t.open = true;
  t.scrollIntoView();
}
addEventListener("hashchange", reveal);
document.addEventListener("click", e => {
  const a = e.target.closest('a[href^="#"]');
  if (!a || a.getAttribute("href") === "#") return;
  const t = document.getElementById(a.getAttribute("href").slice(1));
  if (!t) return;
  e.preventDefault();
  history.replaceState(null, "", a.getAttribute("href"));
  reveal();
});
reveal();

// Copy buttons
document.querySelectorAll(".copy").forEach(b => b.addEventListener("click", async () => {
  try { await navigator.clipboard.writeText(b.previousElementSibling.innerText); b.textContent = "Copied"; }
  catch (err) { b.textContent = "Select"; }
  setTimeout(() => { b.textContent = "Copy"; }, 1500);
}));

// Step ticks, remembered in this browser
document.querySelectorAll(".mtest").forEach(test => {
  const boxes = [...test.querySelectorAll("input[type=checkbox]")];
  const key = "implement-spec-steps:" + document.title + ":" + test.id;
  const count = () => {
    test.querySelector(".done-count").textContent = boxes.filter(b => b.checked).length;
    test.querySelector(".step-total").textContent = boxes.length;
  };
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    boxes.forEach((b, i) => { b.checked = !!saved[i]; });
  } catch (err) {}
  boxes.forEach(b => b.addEventListener("change", () => {
    try { localStorage.setItem(key, JSON.stringify(boxes.map(x => x.checked))); } catch (err) {}
    count();
  }));
  count();
});
mark(0);
