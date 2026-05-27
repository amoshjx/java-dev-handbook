/**
 * 章内目录：从 main 内 section.section[id] 生成右侧浮动 TOC
 */
(function () {
  if (window.__chapterTocMounted) return;
  window.__chapterTocMounted = true;

  const main = document.querySelector("main.main");
  if (!main) return;

  const sections = main.querySelectorAll("section.section[id]");
  if (sections.length === 0) return;

  if (document.querySelector("aside.chapter-toc")) return;

  document.querySelectorAll(".nav-group").forEach(function (group) {
    const title = group.querySelector(".nav-title");
    if (title && title.textContent.trim() === "本章目录") {
      group.remove();
    }
  });

  const layout = document.querySelector(".layout");
  if (!layout) return;

  const pageBody = document.createElement("div");
  pageBody.className = "page-body";
  main.parentNode.insertBefore(pageBody, main);
  pageBody.appendChild(main);

  const aside = document.createElement("aside");
  aside.className = "chapter-toc";
  aside.setAttribute("aria-label", "本章目录");

  const header = document.createElement("div");
  header.className = "chapter-toc-header";
  header.innerHTML =
    '<span class="chapter-toc-title">本章目录</span>' +
    '<button type="button" class="chapter-toc-close" aria-label="关闭目录">×</button>';

  const nav = document.createElement("nav");
  const list = document.createElement("ul");
  list.className = "chapter-toc-list";

  const links = [];

  sections.forEach(function (section) {
    const id = section.id;
    const heading = section.querySelector("h2");
    const label = heading ? heading.textContent.trim() : id;
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = "#" + id;
    a.textContent = label;
    li.appendChild(a);
    list.appendChild(li);
    links.push({ id: id, link: a });
  });

  nav.appendChild(list);
  aside.appendChild(header);
  aside.appendChild(nav);
  pageBody.appendChild(aside);

  document.body.classList.add("has-chapter-toc");

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "chapter-toc-toggle";
  toggle.setAttribute("aria-label", "打开本章目录");
  toggle.setAttribute("aria-expanded", "false");
  toggle.innerHTML =
    '<span class="chapter-toc-toggle-icon" aria-hidden="true">☰</span>' +
    '<span class="chapter-toc-toggle-text">目录</span>';
  document.body.appendChild(toggle);

  const overlay = document.createElement("div");
  overlay.className = "chapter-toc-overlay";
  overlay.setAttribute("aria-hidden", "true");
  document.body.appendChild(overlay);

  const closeBtn = header.querySelector(".chapter-toc-close");

  function openToc() {
    aside.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    document.body.classList.add("chapter-toc-open");
  }

  function closeToc() {
    aside.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("chapter-toc-open");
  }

  toggle.addEventListener("click", function () {
    if (aside.classList.contains("is-open")) {
      closeToc();
    } else {
      openToc();
    }
  });

  closeBtn.addEventListener("click", closeToc);
  overlay.addEventListener("click", closeToc);

  aside.addEventListener("click", function (e) {
    if (e.target.closest("a") && window.matchMedia("(max-width: 1023px)").matches) {
      closeToc();
    }
  });

  function setActive(id) {
    links.forEach(function (item) {
      item.link.classList.toggle("active", item.id === id);
    });
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      function (entries) {
        const visible = entries
          .filter(function (e) {
            return e.isIntersecting;
          })
          .sort(function (a, b) {
            return b.intersectionRatio - a.intersectionRatio;
          });
        if (visible.length > 0) {
          setActive(visible[0].target.id);
        }
      },
      { rootMargin: "-20% 0px -65% 0px", threshold: [0, 0.25, 0.5, 1] }
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
  } else if (links.length > 0) {
    setActive(links[0].id);
  }
})();
