/**
 * Multi-Dimensional Instant Search Engine
 * Supports Ctrl+K spotlight modal, real-time filtering across Chapters, Topics,
 * Formulas, and CBSE Exam PYQs, with auto-scroll and highlighter halos.
 */

(function () {
  'use strict';

  let searchIndex = null;
  let modal, input, resultsContainer, backdrop;
  let activeFilter = 'all';

  async function loadSearchIndex() {
    if (searchIndex) return searchIndex;
    try {
      // Find path to search_index.json relative to current page
      const depth = window.location.pathname.split('/').filter(Boolean);
      let basePath = 'assets/data/search_index.json';
      if (window.location.pathname.includes('/class-11/') || window.location.pathname.includes('/class-12/')) {
        basePath = '../../assets/data/search_index.json';
      }
      const res = await fetch(basePath);
      if (res.ok) {
        searchIndex = await res.json();
      }
    } catch (e) {
      console.warn('Could not load search index:', e);
    }
    return searchIndex;
  }

  function createSearchModal() {
    if (document.getElementById('searchModalBackdrop')) return;

    backdrop = document.createElement('div');
    backdrop.id = 'searchModalBackdrop';
    backdrop.style.cssText = `
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(15, 23, 42, 0.45); backdrop-filter: blur(4px);
      z-index: 2000; opacity: 0; pointer-events: none;
      transition: opacity 0.25s ease;
      display: flex; align-items: flex-start; justify-content: center;
      padding-top: 10vh;
    `;

    modal = document.createElement('div');
    modal.id = 'searchModal';
    modal.style.cssText = `
      background: #ffffff; width: min(640px, 92vw); max-height: 75vh;
      border: 3px solid #cbd5e1; border-radius: 16px;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
      display: flex; flex-direction: column; overflow: hidden;
      transform: translateY(-20px) scale(0.98);
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    `;

    modal.innerHTML = `
      <div style="padding: 1rem 1.25rem; border-bottom: 2px solid #e2e8f0; display: flex; align-items: center; gap: 0.75rem; background: #f8fafc;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="globalSearchInput" placeholder="Search topics, formulas, chapters, or CBSE PYQs... (Press Esc to close)" style="flex: 1; border: none; background: transparent; font-size: 1.05rem; font-family: var(--font-body); color: #0f172a; outline: none;">
        <button id="searchCloseBtn" style="background: transparent; border: none; font-size: 1.25rem; cursor: pointer; color: #94a3b8; line-height: 1;">&times;</button>
      </div>
      <div style="padding: 0.5rem 1rem; background: #f1f5f9; border-bottom: 1px solid #e2e8f0; display: flex; gap: 0.4rem; overflow-x: auto; font-size: 0.8rem;">
        <button class="search-filter-chip active" data-filter="all" style="padding: 0.2rem 0.65rem; border-radius: 12px; border: 1px solid #cbd5e1; background: var(--marker-blue); color: #fff; cursor: pointer;">All</button>
        <button class="search-filter-chip" data-filter="class-11" style="padding: 0.2rem 0.65rem; border-radius: 12px; border: 1px solid #cbd5e1; background: #fff; color: #475569; cursor: pointer;">Class 11</button>
        <button class="search-filter-chip" data-filter="class-12" style="padding: 0.2rem 0.65rem; border-radius: 12px; border: 1px solid #cbd5e1; background: #fff; color: #475569; cursor: pointer;">Class 12</button>
        <button class="search-filter-chip" data-filter="formula" style="padding: 0.2rem 0.65rem; border-radius: 12px; border: 1px solid #cbd5e1; background: #fff; color: #475569; cursor: pointer;">📐 Formulas</button>
        <button class="search-filter-chip" data-filter="pyq" style="padding: 0.2rem 0.65rem; border-radius: 12px; border: 1px solid #cbd5e1; background: #fff; color: #475569; cursor: pointer;">🎯 PYQs</button>
      </div>
      <div id="searchResultsList" style="flex: 1; overflow-y: auto; padding: 0.75rem;">
        <div style="text-align: center; color: #94a3b8; padding: 2rem; font-family: var(--font-hand); font-size: 1.2rem;">
          Type anything to search NCERT concepts, equations, and CBSE board questions...
        </div>
      </div>
    `;

    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);

    input = modal.querySelector('#globalSearchInput');
    resultsContainer = modal.querySelector('#searchResultsList');

    // Filter Chips
    const chips = modal.querySelectorAll('.search-filter-chip');
    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => {
          c.style.background = '#fff';
          c.style.color = '#475569';
          c.classList.remove('active');
        });
        chip.style.background = 'var(--marker-blue)';
        chip.style.color = '#fff';
        chip.classList.add('active');
        activeFilter = chip.getAttribute('data-filter');
        performSearch(input.value);
      });
    });

    // Event Listeners
    input.addEventListener('input', (e) => performSearch(e.target.value));
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeSearch();
    });
    modal.querySelector('#searchCloseBtn').addEventListener('click', closeSearch);
  }

  function openSearch(initialQuery = '') {
    createSearchModal();
    loadSearchIndex().then(() => {
      backdrop.style.opacity = '1';
      backdrop.style.pointerEvents = 'auto';
      modal.style.transform = 'translateY(0) scale(1)';
      input.value = initialQuery;
      input.focus();
      if (initialQuery) performSearch(initialQuery);
    });
  }

  function closeSearch() {
    if (!backdrop) return;
    backdrop.style.opacity = '0';
    backdrop.style.pointerEvents = 'none';
    modal.style.transform = 'translateY(-20px) scale(0.98)';
  }

  function performSearch(query) {
    if (!searchIndex || !resultsContainer) return;
    const q = query.trim().toLowerCase();

    if (!q) {
      resultsContainer.innerHTML = `
        <div style="text-align: center; color: #94a3b8; padding: 2rem; font-family: var(--font-hand); font-size: 1.2rem;">
          Type anything to search NCERT concepts, equations, and CBSE board questions...
        </div>
      `;
      return;
    }

    const matches = searchIndex.filter(item => {
      // Filter by category
      if (activeFilter === 'class-11' && item.class !== '11') return false;
      if (activeFilter === 'class-12' && item.class !== '12') return false;
      if (activeFilter === 'formula' && item.type !== 'formula') return false;
      if (activeFilter === 'pyq' && item.type !== 'pyq') return false;

      const titleMatch = (item.title || '').toLowerCase().includes(q);
      const textMatch = (item.text || '').toLowerCase().includes(q);
      const tagsMatch = (item.tags || []).some(t => t.toLowerCase().includes(q));
      const chMatch = (item.chapter || '').toLowerCase().includes(q);

      return titleMatch || textMatch || tagsMatch || chMatch;
    }).slice(0, 30);

    if (matches.length === 0) {
      resultsContainer.innerHTML = `
        <div style="text-align: center; color: #64748b; padding: 2rem; font-family: var(--font-hand); font-size: 1.2rem;">
          No matching mathematics topics found for "${query}". Try searching "Matrices", "Bayes", "Derivative", or "2024".
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = matches.map((item, idx) => {
      const typeIcons = {
        chapter: '📂',
        concept: '📑',
        formula: '📐',
        pyq: '🎯'
      };
      const icon = typeIcons[item.type] || '📌';
      return `
        <div class="search-result-item" data-url="${item.url}" data-target-id="${item.targetId || ''}" style="padding: 0.8rem 1rem; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 0.5rem; cursor: pointer; transition: all 0.15s ease; background: #ffffff;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.25rem;">
            <span style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase;">
              ${icon} Class ${item.class} • ${item.chapter}
            </span>
            ${item.badge ? `<span style="font-size: 0.7rem; font-weight: 700; background: #fef9c3; color: #854d0e; padding: 0.1rem 0.5rem; border-radius: 10px;">${item.badge}</span>` : ''}
          </div>
          <div style="font-family: var(--font-title); font-size: 1.05rem; font-weight: 700; color: #1e293b;">
            ${item.title}
          </div>
          ${item.snippet ? `<div style="font-size: 0.85rem; color: #475569; margin-top: 0.2rem; line-height: 1.4;">${item.snippet}</div>` : ''}
        </div>
      `;
    }).join('');

    // Attach click listeners to result items
    resultsContainer.querySelectorAll('.search-result-item').forEach(el => {
      el.addEventListener('mouseenter', () => {
        el.style.background = '#f8fafc';
        el.style.borderColor = 'var(--marker-blue)';
      });
      el.addEventListener('mouseleave', () => {
        el.style.background = '#ffffff';
        el.style.borderColor = '#e2e8f0';
      });
      el.addEventListener('click', () => {
        const url = el.getAttribute('data-url');
        const targetId = el.getAttribute('data-target-id');
        closeSearch();

        if (url) {
          // Check if on same page
          const currentPath = window.location.pathname;
          if (url.startsWith('#') || url === currentPath || url.endsWith(currentPath)) {
            if (targetId) {
              const targetEl = document.getElementById(targetId);
              if (targetEl) {
                targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                targetEl.classList.add('target-highlight-halo');
                setTimeout(() => targetEl.classList.remove('target-highlight-halo'), 3000);
                return;
              }
            }
          }
          window.location.href = url;
        }
      });
    });
  }

  // Hotkey listener (Ctrl+K or /)
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearch();
    } else if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      openSearch();
    } else if (e.key === 'Escape') {
      closeSearch();
    }
  });

  // Attach search triggers across page
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.open-search-trigger').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openSearch();
      });
    });
  });

  window.WhiteboardSearch = {
    open: openSearch,
    close: closeSearch
  };
})();
