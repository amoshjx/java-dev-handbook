(function () {
  'use strict';

  var MERMAID_LOCAL = 'assets/mermaid.min.js?v=10.9.3';
  var MERMAID_CDN =
    'https://cdn.jsdelivr.net/npm/mermaid@10.9.3/dist/mermaid.min.js';
  var MERMAID_WAIT_MS = 8000;

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function waitForGlobal(name, timeoutMs) {
    return new Promise(function (resolve, reject) {
      if (window[name]) {
        resolve(window[name]);
        return;
      }

      var started = Date.now();
      (function poll() {
        if (window[name]) {
          resolve(window[name]);
          return;
        }
        if (Date.now() - started >= timeoutMs) {
          reject(new Error(name + ' 未在 ' + timeoutMs + 'ms 内就绪'));
          return;
        }
        requestAnimationFrame(poll);
      })();
    });
  }

  function ensureMermaid() {
    if (window.mermaid) return Promise.resolve(window.mermaid);
    return loadScript(MERMAID_LOCAL)
      .then(function () {
        return waitForGlobal('mermaid', MERMAID_WAIT_MS);
      })
      .catch(function () {
        return loadScript(MERMAID_CDN).then(function () {
          return waitForGlobal('mermaid', MERMAID_WAIT_MS);
        });
      });
  }

  function initMermaid() {
    var blocks = document.querySelectorAll('pre.mermaid');
    if (!blocks.length) return;

    ensureMermaid()
      .then(function () {
        mermaid.initialize({
          startOnLoad: false,
          theme: 'neutral',
          securityLevel: 'loose',
          flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
          sequence: { useMaxWidth: true, wrap: true },
          fontFamily:
            '"Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif'
        });
        return mermaid.run({
          nodes: blocks,
          suppressErrors: true
        }).then(function () {
          blocks.forEach(function (el, index) {
            if (!el.querySelector('svg')) {
              var preview = (el.textContent || '').trim().split('\n')[0];
              console.warn(
                '[diagram.js] 图表 #' + (index + 1) + ' 未渲染',
                preview ? '(' + preview + ')' : '',
                el
              );
              el.classList.add('mermaid-fallback');
            }
          });
        });
      })
      .catch(function (err) {
        console.warn('[diagram.js] Mermaid 加载或初始化失败:', err);
        blocks.forEach(function (el) {
          el.classList.add('mermaid-fallback');
        });
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }
})();
