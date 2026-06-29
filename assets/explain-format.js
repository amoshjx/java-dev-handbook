/**
 * 概要块自动断句与 strong 分段（仅排版，不改文案）
 * 依赖：DOM 就绪后执行；与 chapter-toc.js 顺序：本脚本在前
 */
(function () {
  "use strict";

  var MIN_SPLIT_LEN = 80;
  var PROTECTED = { CODE: 1, A: 1, PRE: 1, STRONG: 1, EM: 1, BR: 1 };

  function textLen(el) {
    return (el.textContent || "").replace(/\s+/g, "").length;
  }

  function isProtected(el) {
    return el && el.nodeType === 1 && PROTECTED[el.nodeName];
  }

  function endsSentence(text) {
    return /[。.；;!?！？]\s*$/.test((text || "").trim());
  }

  function trailingTextBefore(node) {
    var t = "";
    var cur = node;
    while (cur) {
      if (cur.nodeType === 3) {
        t = cur.textContent + t;
      } else if (cur.nodeType === 1 && !isProtected(cur)) {
        var kids = cur.childNodes;
        for (var i = kids.length - 1; i >= 0; i--) {
          var part = trailingTextBefore(kids[i]);
          if (part) return part + t;
        }
      }
      cur = cur.previousSibling;
    }
    return t.trim();
  }

  function strongIsLabel(strong) {
    var n = strong.nextSibling;
    if (!n || n.nodeType !== 3) return false;
    return /^[\s：:]+/.test(n.textContent);
  }

  function directStrongCount(p) {
    var count = 0;
    var kids = p.childNodes;
    for (var i = 0; i < kids.length; i++) {
      if (kids[i].nodeType === 1 && kids[i].nodeName === "STRONG") count++;
    }
    return count;
  }

  function trimLeadingWhitespace(fragment) {
    while (fragment.firstChild && fragment.firstChild.nodeType === 3) {
      var trimmed = fragment.firstChild.textContent.replace(/^\s+/, "");
      if (!trimmed) {
        fragment.removeChild(fragment.firstChild);
        continue;
      }
      if (trimmed !== fragment.firstChild.textContent) {
        fragment.firstChild.textContent = trimmed;
      }
      break;
    }
  }

  function precededByBreak(strong) {
    var n = strong.previousSibling;
    while (n && n.nodeType === 3 && !/[^\s]/.test(n.textContent)) {
      n = n.previousSibling;
    }
    return n && n.nodeName === "BR";
  }

  function markStrongLeads(root) {
    var strongs = root.querySelectorAll("strong");
    for (var i = 0; i < strongs.length; i++) {
      var s = strongs[i];
      if (s.closest("code, a, pre")) continue;
      if (!s.previousSibling) continue;
      if (precededByBreak(s)) continue;
      if (endsSentence(trailingTextBefore(s))) {
        s.classList.add("explain-strong-head");
      } else if (strongIsLabel(s)) {
        s.classList.add("explain-strong-head");
      }
    }
  }

  function splitTextChunk(text) {
    var parts = [];
    var start = 0;
    for (var i = 0; i < text.length; i++) {
      var ch = text.charAt(i);
      if (ch === "\u3002" || ch === "\uff1b" || ch === ";") {
        parts.push(text.slice(start, i + 1));
        start = i + 1;
        continue;
      }
      if (ch === ".") {
        var prev = i > 0 ? text.charAt(i - 1) : "";
        var next = i + 1 < text.length ? text.charAt(i + 1) : "";
        if (/\d/.test(prev) && /\d/.test(next)) continue;
        if (
          !next ||
          /\s/.test(next) ||
          next === "<" ||
          /[\u4e00-\u9fff\u3001\u300c\uff08]/.test(next)
        ) {
          parts.push(text.slice(start, i + 1));
          start = i + 1;
        }
      }
    }
    if (start < text.length) parts.push(text.slice(start));
    return parts.filter(function (p) {
      return p.length > 0;
    });
  }

  /** @returns {DocumentFragment[]} */
  function segmentParagraph(p) {
    var segments = [];
    var buf = document.createDocumentFragment();

    function flush() {
      if (!buf.childNodes.length) return;
      segments.push(buf);
      buf = document.createDocumentFragment();
    }

    function walk(node) {
      if (node.nodeType === 3) {
        var pieces = splitTextChunk(node.textContent);
        for (var i = 0; i < pieces.length; i++) {
          if (pieces[i]) buf.appendChild(document.createTextNode(pieces[i]));
          if (i < pieces.length - 1) flush();
        }
        return;
      }
      if (node.nodeType !== 1) return;
      if (isProtected(node)) {
        buf.appendChild(node.cloneNode(true));
        return;
      }
      var children = node.childNodes;
      for (var j = 0; j < children.length; j++) walk(children[j]);
    }

    var top = p.childNodes;
    for (var k = 0; k < top.length; k++) walk(top[k]);
    flush();
    return segments;
  }

  function splitParagraph(p) {
    if (p.querySelector("p")) return;
    var len = textLen(p);
    markStrongLeads(p);
    if (len <= MIN_SPLIT_LEN) return;
    if (directStrongCount(p) >= 2) return;

    var segments = segmentParagraph(p);
    if (segments.length <= 1) return;

    var parent = p.parentNode;
    var ref = p.nextSibling;
    for (var i = 0; i < segments.length; i++) {
      var np = document.createElement("p");
      np.className = "explain-sentence";
      trimLeadingWhitespace(segments[i]);
      np.appendChild(segments[i]);
      markStrongLeads(np);
      parent.insertBefore(np, ref);
    }
    parent.removeChild(p);
  }

  function formatBlock(block) {
    var paras = block.querySelectorAll(":scope > p");
    if (!paras.length) return;
    var direct = Array.prototype.filter.call(paras, function (p) {
      return p.parentNode === block;
    });
    for (var i = 0; i < direct.length; i++) {
      splitParagraph(direct[i]);
    }
  }

  function run() {
    var blocks = document.querySelectorAll(".block-explain");
    for (var i = 0; i < blocks.length; i++) formatBlock(blocks[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
