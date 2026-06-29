(function () {
  'use strict';

  var MERMAID_VERSION = '10.9.3';
  var MERMAID_FILE = 'mermaid.min.js?v=' + MERMAID_VERSION;
  // 国内可访问的 CDN 镜像（BootCDN / Staticfile / npmmirror）
  var MERMAID_CDNS = [
    'https://cdn.bootcdn.net/ajax/libs/mermaid/' +
      MERMAID_VERSION +
      '/mermaid.min.js',
    'https://cdn.staticfile.net/mermaid/' +
      MERMAID_VERSION +
      '/mermaid.min.js',
    'https://registry.npmmirror.com/mermaid/' +
      MERMAID_VERSION +
      '/files/dist/mermaid.min.js'
  ];
  var MERMAID_WAIT_MS = 8000;
  var FONT_FAMILY =
    '"Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif';

  function getDiagramScriptBase() {
    var scripts = document.getElementsByTagName('script');
    for (var i = scripts.length - 1; i >= 0; i--) {
      var src = scripts[i].src;
      if (src && src.indexOf('diagram.js') !== -1) {
        return src.slice(0, src.lastIndexOf('/') + 1);
      }
    }
    return 'assets/';
  }

  function resolveAssetUrl(file) {
    var base = getDiagramScriptBase();
    try {
      return new URL(file, base).href;
    } catch (e) {
      return base + file;
    }
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function loadFirstScript(urls) {
    var index = 0;

    function tryNext() {
      if (index >= urls.length) {
        return Promise.reject(new Error('所有 Mermaid 资源均加载失败'));
      }
      var url = urls[index++];
      return loadScript(url).catch(tryNext);
    }

    return tryNext();
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
    var localUrl = resolveAssetUrl(MERMAID_FILE);
    return loadScript(localUrl)
      .then(function () {
        return waitForGlobal('mermaid', MERMAID_WAIT_MS);
      })
      .catch(function () {
        return loadFirstScript(MERMAID_CDNS).then(function () {
          return waitForGlobal('mermaid', MERMAID_WAIT_MS);
        });
      });
  }

  function prefersDark() {
    return (
      window.matchMedia &&
      window.matchMedia('(prefers-color-scheme: dark)').matches
    );
  }

  function mermaidConfig() {
    var dark = prefersDark();
    var shared = {
      startOnLoad: false,
      securityLevel: 'loose',
      flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' },
      sequence: { useMaxWidth: true, wrap: true },
      gantt: { useMaxWidth: true },
      fontFamily: FONT_FAMILY,
      fontSize: dark ? '15px' : '14px'
    };

    if (!dark) {
      return Object.assign(shared, { theme: 'neutral' });
    }

    return Object.assign(shared, {
      theme: 'dark',
      themeVariables: {
        darkMode: true,
        background: 'transparent',
        primaryColor: '#1e3a5f',
        primaryTextColor: '#f8fafc',
        primaryBorderColor: '#60a5fa',
        secondaryColor: '#14532d',
        secondaryTextColor: '#ecfdf5',
        secondaryBorderColor: '#34d399',
        tertiaryColor: '#312e81',
        tertiaryTextColor: '#e0e7ff',
        tertiaryBorderColor: '#818cf8',
        lineColor: '#94a3b8',
        textColor: '#e5e7eb',
        mainBkg: '#1e293b',
        nodeBorder: '#64748b',
        clusterBkg: '#0f172a',
        clusterBorder: '#475569',
        defaultLinkColor: '#94a3b8',
        titleColor: '#f8fafc',
        edgeLabelBackground: '#1e293b',
        nodeTextColor: '#f8fafc',
        actorBorder: '#64748b',
        actorBkg: '#1e293b',
        actorTextColor: '#f8fafc',
        actorLineColor: '#94a3b8',
        signalColor: '#94a3b8',
        signalTextColor: '#f8fafc',
        labelBoxBkgColor: '#1e293b',
        labelBoxBorderColor: '#64748b',
        labelTextColor: '#f8fafc',
        loopTextColor: '#e5e7eb',
        noteBkgColor: '#422006',
        noteTextColor: '#fef3c7',
        noteBorderColor: '#f59e0b',
        activationBorderColor: '#64748b',
        activationBkgColor: '#334155',
        sequenceNumberColor: '#0f172a',
        sectionBkgColor: '#1e293b',
        altSectionBkgColor: '#0f172a',
        sectionBkgColor2: '#334155',
        gridColor: '#475569',
        todayLineColor: '#60a5fa',
        taskTextColor: '#f8fafc',
        taskTextOutsideColor: '#f8fafc',
        taskTextLightColor: '#0f172a',
        taskTextDarkColor: '#f8fafc',
        taskBkgColor: '#1e3a5f',
        activeTaskBkgColor: '#2563eb',
        activeTaskBorderColor: '#60a5fa',
        doneTaskBkgColor: '#14532d',
        doneTaskBorderColor: '#34d399',
        critTaskBkgColor: '#7f1d1d',
        critTaskBorderColor: '#f87171',
        milestoneBkgColor: '#422006',
        milestoneBorderColor: '#fbbf24',
        git0: '#1e3a5f',
        git1: '#14532d',
        git2: '#312e81',
        git3: '#422006',
        git4: '#581c87',
        git5: '#713f12',
        git6: '#134e4a',
        git7: '#831843',
        gitInv0: '#f8fafc',
        gitBranchLabel0: '#f8fafc',
        gitBranchLabel1: '#f8fafc',
        gitBranchLabel2: '#f8fafc',
        gitBranchLabel3: '#f8fafc',
        gitBranchLabel4: '#f8fafc',
        gitBranchLabel5: '#f8fafc',
        gitBranchLabel6: '#f8fafc',
        gitBranchLabel7: '#f8fafc',
        quadrant1Fill: '#1e3a5f',
        quadrant2Fill: '#14532d',
        quadrant3Fill: '#374151',
        quadrant4Fill: '#422006',
        quadrantPointFill: '#60a5fa',
        quadrantXAxisTextColor: '#f8fafc',
        quadrantYAxisTextColor: '#f8fafc',
        quadrantTitleFill: '#f8fafc',
        quadrantLabelFill: '#e5e7eb',
        stateLabelColor: '#f8fafc',
        labelColor: '#e5e7eb',
        errorBkgColor: '#7f1d1d',
        errorTextColor: '#fecaca'
      }
    });
  }

  function rememberSources(blocks) {
    blocks.forEach(function (el) {
      if (!el.dataset.mermaidSource) {
        el.dataset.mermaidSource = (el.textContent || '').trim();
      }
    });
  }

  function restoreSources(blocks) {
    blocks.forEach(function (el) {
      var source = el.dataset.mermaidSource;
      if (source) {
        el.textContent = source;
        el.classList.remove('mermaid-fallback');
      }
    });
  }

  function markFallbacks(blocks) {
    blocks.forEach(function (el, index) {
      if (!el.querySelector('svg')) {
        var preview = (el.dataset.mermaidSource || el.textContent || '')
          .trim()
          .split('\n')[0];
        console.warn(
          '[diagram.js] 图表 #' + (index + 1) + ' 未渲染',
          preview ? '(' + preview + ')' : '',
          el
        );
        el.classList.add('mermaid-fallback');
      }
    });
  }

  function renderMermaid(blocks) {
    rememberSources(blocks);
    restoreSources(blocks);
    mermaid.initialize(mermaidConfig());
    return mermaid
      .run({
        nodes: blocks,
        suppressErrors: true
      })
      .then(function () {
        markFallbacks(blocks);
      });
  }

  function initMermaid() {
    var blocks = document.querySelectorAll('pre.mermaid');
    if (!blocks.length) return;

    ensureMermaid()
      .then(function () {
        return renderMermaid(blocks);
      })
      .catch(function (err) {
        console.warn('[diagram.js] Mermaid 加载或初始化失败:', err);
        blocks.forEach(function (el) {
          el.classList.add('mermaid-fallback');
        });
      });

    if (window.matchMedia) {
      var media = window.matchMedia('(prefers-color-scheme: dark)');
      if (typeof media.addEventListener === 'function') {
        media.addEventListener('change', function () {
          if (!window.mermaid) return;
          renderMermaid(blocks).catch(function (err) {
            console.warn('[diagram.js] 主题切换后重渲染失败:', err);
          });
        });
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMermaid);
  } else {
    initMermaid();
  }
})();
