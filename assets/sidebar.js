/**
 * 侧边栏「开发实现」分组折叠
 */
(function () {
  'use strict';

  if (window.__sidebarCollapseMounted) return;
  window.__sidebarCollapseMounted = true;

  var STORAGE_KEY = 'handbook-sidebar-dev-collapsed';

  function currentPage() {
    var path = window.location.pathname;
    var name = path.substring(path.lastIndexOf('/') + 1);
    return name || 'index.html';
  }

  function isDevSectionPage(page) {
    return (
      page === 'java-development.html' ||
      /^0[5-9]-/.test(page) ||
      /^1[0-7]-/.test(page)
    );
  }

  document.querySelectorAll('.nav-list').forEach(function (navList) {
    var groupLi = navList.querySelector('li.sidebar-group');
    if (!groupLi) return;

    var subitems = [];
    var next = groupLi.nextElementSibling;
    while (next && next.classList.contains('sidebar-subitem')) {
      subitems.push(next);
      next = next.nextElementSibling;
    }
    if (subitems.length === 0) return;

    var wrapper = document.createElement('li');
    wrapper.className = 'sidebar-collapse';

    var header = document.createElement('div');
    header.className = 'sidebar-collapse-header sidebar-group';

    var toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.className = 'sidebar-collapse-toggle';
    toggleBtn.setAttribute('aria-controls', 'sidebar-dev-items');
    toggleBtn.setAttribute('aria-label', '展开或折叠开发实现章节');
    toggleBtn.innerHTML = '<span class="sidebar-collapse-chevron" aria-hidden="true"></span>';

    var labelSpan = groupLi.querySelector('.sidebar-group-label');
    header.appendChild(toggleBtn);
    if (labelSpan) {
      header.appendChild(labelSpan);
    }

    var itemsUl = document.createElement('ul');
    itemsUl.className = 'sidebar-collapse-items';
    itemsUl.id = 'sidebar-dev-items';

    subitems.forEach(function (item) {
      itemsUl.appendChild(item);
    });

    wrapper.appendChild(header);
    wrapper.appendChild(itemsUl);
    groupLi.replaceWith(wrapper);

    var page = currentPage();
    var collapsed = localStorage.getItem(STORAGE_KEY) === 'true';
    if (isDevSectionPage(page)) {
      collapsed = false;
    }

    function setCollapsed(value) {
      wrapper.classList.toggle('is-collapsed', value);
      toggleBtn.setAttribute('aria-expanded', String(!value));
      localStorage.setItem(STORAGE_KEY, String(value));
    }

    setCollapsed(collapsed);

    toggleBtn.addEventListener('click', function () {
      setCollapsed(!wrapper.classList.contains('is-collapsed'));
    });
  });
})();
