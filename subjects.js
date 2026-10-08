/* 科目切換：插入到每一科講義側邊欄最上方 */
(function () {
  var SUBJECTS = [
    { dir: "chemistry", name: "選修化學 II" },
    { dir: "physics", name: "選修物理" },
    { dir: "biology", name: "生物" },
    { dir: "earth", name: "地球科學" }
  ];
  var parts = location.pathname.split("/");
  var cur = parts[parts.length - 2];
  var wrap = document.createElement("div");
  wrap.className = "subj-switch";
  wrap.innerHTML =
    '<a href="../index.html" title="回科目首頁">⌂ 科目</a><select aria-label="切換科目">' +
    SUBJECTS.map(function (s) {
      return '<option value="' + s.dir + '"' + (s.dir === cur ? " selected" : "") + ">" + s.name + "</option>";
    }).join("") + "</select>";
  wrap.querySelector("select").addEventListener("change", function () {
    location.href = "../" + this.value + "/index.html";
  });
  var css = document.createElement("style");
  css.textContent =
    ".subj-switch{display:flex;gap:8px;align-items:center;margin:0 6px 14px;font-size:14px}" +
    ".subj-switch a{color:var(--muted,#6b7280);text-decoration:none;white-space:nowrap}" +
    ".subj-switch a:hover{color:var(--accent,#0f7c7a)}" +
    ".subj-switch select{flex:1;min-width:0;font:inherit;padding:5px 8px;border-radius:8px;" +
    "border:1px solid var(--line,#e4dfd4);background:var(--paper,#fff);color:var(--ink,#23272e)}" +
    ".subj-switch.float{position:fixed;top:10px;right:12px;z-index:60;background:var(--paper,#fff);" +
    "padding:6px 10px;border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.15);margin:0}";
  document.head.appendChild(css);
  var side = document.querySelector(".side");
  if (side) side.insertBefore(wrap, side.firstChild);
  else { wrap.classList.add("float"); document.body.appendChild(wrap); }
})();
