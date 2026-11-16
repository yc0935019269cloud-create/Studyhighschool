/* 心智圖引擎：NotebookLM 式由左往右展開的樹狀圖。
   資料格式：{t:"標題", n:"點開後的說明（可含簡單 HTML）", href:"相關講義", c:[子節點...]} */
(function () {
  var GX = 46, GY = 10, DUR = 260;
  var stage, world, svg, noteBox, nodes = [], root, scale = 1, tx = 0, ty = 0, sel = null, animId = 0;

  function el(tag, cls, html) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html != null) e.innerHTML = html;
    return e;
  }

  function build(d, parent, depth) {
    var n = { d: d, parent: parent, depth: depth, kids: [], open: depth < 1, x: 0, y: 0, px: 0, py: 0, vis: depth === 0 };
    n.el = el("div", "nd" + (depth === 0 ? " root" : "") + (depth === 1 ? " d1" : "") + (d.c && d.c.length ? " br" : "") + (d.n || d.href ? " hasnote" : ""));
    n.el.appendChild(el("span", "tx", d.t));
    if (d.c && d.c.length) {
      n.tg = el("button", "tg");
      n.tg.type = "button";
      n.tg.addEventListener("click", function (ev) { ev.stopPropagation(); toggle(n); });
      n.tg.addEventListener("pointerdown", function (ev) { ev.stopPropagation(); });
      n.el.appendChild(n.tg);
    }
    n.el.addEventListener("pointerdown", function (ev) { ev.stopPropagation(); });
    n.el.addEventListener("click", function () {
      if (n.d.n || n.d.href) showNote(n);
      else if (n.kids.length) toggle(n);
    });
    world.appendChild(n.el);
    nodes.push(n);
    (d.c || []).forEach(function (cd) { n.kids.push(build(cd, n, depth + 1)); });
    return n;
  }

  function measure() {
    nodes.forEach(function (n) { n.w = n.el.offsetWidth; n.h = n.el.offsetHeight; });
  }

  // 回傳子樹高度；y 為子樹頂端
  function lay(n, x, y) {
    n.x = x;
    var shown = n.open ? n.kids : [];
    if (!shown.length) { n.y = y; return n.h; }
    var cx = x + n.w + GX, cy = y, first = null, last = null;
    shown.forEach(function (k, i) {
      if (i) cy += GY;
      var h = lay(k, cx, cy);
      if (!first) first = k;
      last = k;
      cy += h;
    });
    var total = cy - y;
    var mid = (first.y + first.h / 2 + last.y + last.h / 2) / 2;
    n.y = mid - n.h / 2;
    if (n.h > total) { var shift = (n.h - total) / 2; shown.forEach(function (k) { moveTree(k, shift); }); n.y = y; return n.h; }
    if (n.y < y) { var s2 = y - n.y; shown.forEach(function (k) { moveTree(k, s2); }); n.y = y; total += s2; }
    return Math.max(total, n.y + n.h - y);
  }
  function moveTree(n, dy) { n.y += dy; if (n.open) n.kids.forEach(function (k) { moveTree(k, dy); }); }

  function markVis(n, v) {
    n.vis = v;
    n.kids.forEach(function (k) { markVis(k, v && n.open); });
  }
  // 隱藏的節點收到最近一個可見祖先的位置
  function hiddenTargets(n, anchor) {
    n.kids.forEach(function (k) {
      if (!k.vis) { k.x = anchor.x + anchor.w - k.w; k.y = anchor.y + anchor.h / 2 - k.h / 2; hiddenTargets(k, anchor); }
      else hiddenTargets(k, k);
    });
  }

  function edgePath(a, b) {
    var x1 = a.cx + a.w, y1 = a.cy + a.h / 2, x2 = b.cx, y2 = b.cy + b.h / 2, m = (x1 + x2) / 2;
    return "M" + x1 + "," + y1 + " C" + m + "," + y1 + " " + m + "," + y2 + " " + x2 + "," + y2;
  }

  function paint() {
    var paths = [];
    nodes.forEach(function (n) {
      n.el.style.transform = "translate(" + n.cx + "px," + n.cy + "px)";
      n.el.style.opacity = n.op;
      n.el.style.visibility = n.op < 0.02 ? "hidden" : "visible";
      if (n.parent && n.op > 0.02) paths.push('<path style="opacity:' + n.op + '" d="' + edgePath(n.parent, n) + '"/>');
      if (n.tg) n.tg.textContent = n.open ? "‹" : "›";
    });
    svg.innerHTML = paths.join("");
    world.style.transform = "translate(" + tx + "px," + ty + "px) scale(" + scale + ")";
  }

  // anchor：維持在畫面同一位置的節點
  function relayout(anchor, animate) {
    markVis(root, true);
    lay(root, 0, 0);
    hiddenTargets(root, root);
    var from = nodes.map(function (n) { return [n.cx, n.cy, n.op]; });
    var tx0 = tx, ty0 = ty, tx1 = tx, ty1 = ty;
    if (anchor && anchor.cx != null) { tx1 = tx - (anchor.x - anchor.cx) * scale; ty1 = ty - (anchor.y - anchor.cy) * scale; }
    var id = ++animId;
    if (!animate || from[0][0] == null) {
      nodes.forEach(function (n) { n.cx = n.x; n.cy = n.y; n.op = n.vis ? 1 : 0; });
      tx = tx1; ty = ty1; paint(); return;
    }
    var t0 = performance.now();
    (function step(now) {
      if (id !== animId) return;
      var p = Math.min(1, (now - t0) / DUR), e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
      nodes.forEach(function (n, i) {
        var f = from[i];
        n.cx = f[0] + (n.x - f[0]) * e; n.cy = f[1] + (n.y - f[1]) * e;
        n.op = f[2] + ((n.vis ? 1 : 0) - f[2]) * e;
      });
      tx = tx0 + (tx1 - tx0) * e; ty = ty0 + (ty1 - ty0) * e;
      paint();
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }

  function toggle(n) { n.open = !n.open; relayout(n, true); }

  function setAll(open) {
    nodes.forEach(function (n) { if (n.kids.length) n.open = open || n.depth < 1; });
    relayout(null, false);
    fit();
  }

  function fit() {
    var minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
    nodes.forEach(function (n) {
      if (!n.vis) return;
      minX = Math.min(minX, n.x); minY = Math.min(minY, n.y);
      maxX = Math.max(maxX, n.x + n.w + 14); maxY = Math.max(maxY, n.y + n.h);
    });
    var top = document.querySelector(".mm-top").offsetHeight + 16;
    var W = stage.clientWidth - 40, H = stage.clientHeight - top - 30;
    scale = Math.max(0.25, Math.min(1.15, W / (maxX - minX), H / (maxY - minY)));
    tx = 20 + (W - (maxX - minX) * scale) / 2 - minX * scale;
    if (tx > 40) tx = Math.min(tx, 40 + (W - (maxX - minX) * scale) / 2);
    ty = top + (H - (maxY - minY) * scale) / 2 - minY * scale;
    paint();
  }

  function zoomAt(f, px, py) {
    var ns = Math.max(0.2, Math.min(3, scale * f));
    tx = px - (px - tx) * ns / scale; ty = py - (py - ty) * ns / scale; scale = ns;
    paint();
  }

  function pathOf(n) {
    var a = [];
    for (var p = n.parent; p; p = p.parent) a.unshift(p.d.t.replace(/<[^>]+>/g, ""));
    return a.join(" › ");
  }
  function showNote(n) {
    if (sel) sel.el.classList.remove("sel");
    sel = n; n.el.classList.add("sel");
    var h = '<button class="x" type="button" aria-label="關閉">×</button>';
    if (n.parent) h += '<div class="path">' + pathOf(n) + "</div>";
    h += "<h2>" + n.d.t + "</h2>" + (n.d.n || "");
    if (n.kids.length) h += '<p><a href="#" data-tg>' + (n.open ? "收起" : "展開") + "這個分支（" + n.kids.length + " 項）</a></p>";
    if (n.d.href) h += '<p><a href="' + n.d.href + '">開啟講義 →</a></p>';
    noteBox.innerHTML = h;
    noteBox.classList.add("on");
    noteBox.querySelector(".x").onclick = hideNote;
    var t = noteBox.querySelector("[data-tg]");
    if (t) t.onclick = function (e) { e.preventDefault(); toggle(n); showNote(n); };
  }
  function hideNote() { noteBox.classList.remove("on"); if (sel) sel.el.classList.remove("sel"); sel = null; }

  function interact() {
    var pts = {}, last = null, pinch = null;
    stage.addEventListener("pointerdown", function (e) {
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      stage.setPointerCapture(e.pointerId);
      stage.classList.add("drag");
      animId++;
    });
    stage.addEventListener("pointermove", function (e) {
      if (!pts[e.pointerId]) return;
      var prev = pts[e.pointerId];
      pts[e.pointerId] = { x: e.clientX, y: e.clientY };
      var ids = Object.keys(pts);
      if (ids.length === 2) {
        var a = pts[ids[0]], b = pts[ids[1]], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (pinch) zoomAt(d / pinch, (a.x + b.x) / 2, (a.y + b.y) / 2);
        pinch = d;
      } else {
        tx += e.clientX - prev.x; ty += e.clientY - prev.y; paint();
      }
    });
    function up(e) { delete pts[e.pointerId]; pinch = null; if (!Object.keys(pts).length) stage.classList.remove("drag"); }
    stage.addEventListener("pointerup", up);
    stage.addEventListener("pointercancel", up);
    stage.addEventListener("wheel", function (e) {
      e.preventDefault();
      var dy = e.deltaMode === 1 ? e.deltaY * 30 : e.deltaY;
      zoomAt(Math.exp(-dy * 0.0015), e.clientX, e.clientY);
    }, { passive: false });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") hideNote(); });
    window.addEventListener("resize", function () { fit(); });
  }

  window.MindMap = {
    render: function (data) {
      stage = document.getElementById("stage");
      world = document.getElementById("world");
      svg = document.getElementById("edges");
      noteBox = document.getElementById("note");
      root = build(data, null, 0);
      measure();
      relayout(null, false);
      fit();
      interact();
      document.querySelectorAll("[data-act]").forEach(function (b) {
        b.addEventListener("click", function () {
          var a = b.getAttribute("data-act");
          if (a === "open") setAll(true);
          else if (a === "close") setAll(false);
          else if (a === "fit") fit();
          else if (a === "in") zoomAt(1.2, stage.clientWidth / 2, stage.clientHeight / 2);
          else if (a === "out") zoomAt(1 / 1.2, stage.clientWidth / 2, stage.clientHeight / 2);
        });
      });
    }
  };
})();
