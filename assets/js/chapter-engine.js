/**
 * Chapter Interactive Engine
 * Handles tab switching, KaTeX rendering, PYQ filtering, and progress tracking.
 */

(function () {
  'use strict';

  function initChapterTabs() {
    const tabs = document.querySelectorAll('.chapter-tabs .tab-item');
    const panels = document.querySelectorAll('.panels-container .view-panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetId = tab.getAttribute('data-target');
        if (!targetId) return;

        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        const targetPanel = document.getElementById(targetId);
        if (targetPanel) {
          targetPanel.classList.add('active');
          window.scrollTo({ top: 0, behavior: 'smooth' });
          if (typeof renderMathInElement === 'function') {
            renderMathInElement(targetPanel, {
              delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\\(', right: '\\)', display: false },
                { left: '\\[', right: '\\]', display: true }
              ],
              throwOnError: false
            });
          }
        }
      });
    });
  }

  function initSolutionAccordions() {
    document.querySelectorAll('details.solution-accordion').forEach(details => {
      details.addEventListener('toggle', () => {
        if (details.open && typeof renderMathInElement === 'function') {
          const body = details.querySelector('.solution-body');
          if (body) {
            renderMathInElement(body, {
              delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false },
                { left: '\\(', right: '\\)', display: false },
                { left: '\\[', right: '\\]', display: true }
              ],
              throwOnError: false
            });
          }
        }
      });
    });
  }

  function initPyqFilters() {
    const filterChips = document.querySelectorAll('.pyq-filter-bar .filter-chip');
    const questionCards = document.querySelectorAll('.view-panel#panel-pyqs .question-card');

    filterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        filterChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');

        const filter = chip.getAttribute('data-filter'); // e.g. 'all', '1m', '2m', '3m', '5m', '2024', '2023'

        questionCards.forEach(card => {
          if (filter === 'all') {
            card.style.display = 'block';
            return;
          }

          const marks = card.getAttribute('data-marks') || '';
          const year = card.getAttribute('data-year') || '';

          if (filter === '1m' && marks.includes('1')) card.style.display = 'block';
          else if (filter === '2m' && marks.includes('2')) card.style.display = 'block';
          else if (filter === '3m' && marks.includes('3')) card.style.display = 'block';
          else if (filter === '4m' && marks.includes('4')) card.style.display = 'block';
          else if (filter === '5m' && marks.includes('5')) card.style.display = 'block';
          else if (year.includes(filter)) card.style.display = 'block';
          else card.style.display = 'none';
        });
      });
    });
  }

  function initGridToggle() {
    const gridBtn = document.getElementById('gridToggleBtn');
    if (!gridBtn) return;

    const patterns = ['pattern-dots', 'pattern-graph', 'pattern-blank'];
    let currentIdx = 0;

    gridBtn.addEventListener('click', () => {
      document.body.classList.remove('pattern-graph', 'pattern-blank');
      currentIdx = (currentIdx + 1) % patterns.length;

      if (patterns[currentIdx] === 'pattern-graph') {
        document.body.classList.add('pattern-graph');
        gridBtn.innerHTML = '📐 Grid: Graph';
      } else if (patterns[currentIdx] === 'pattern-blank') {
        document.body.classList.add('pattern-blank');
        gridBtn.innerHTML = '◻️ Grid: Blank';
      } else {
        gridBtn.innerHTML = '⁝⁝ Grid: Dots';
      }
    });
  }

  function initProgressTracker() {
    const completeBtn = document.getElementById('markCompletedBtn');
    const slug = document.body.getAttribute('data-chapter-slug');
    if (!completeBtn || !slug) return;

    const storageKey = 'cbse_maths_completed_' + slug;
    const isDone = localStorage.getItem(storageKey) === 'true';

    function updateBtn(done) {
      if (done) {
        completeBtn.innerHTML = '✓ Mastered';
        completeBtn.classList.add('active');
        completeBtn.style.background = '#15803d';
        completeBtn.style.color = '#ffffff';
        completeBtn.style.borderColor = '#15803d';
      } else {
        completeBtn.innerHTML = '○ Mark Complete';
        completeBtn.classList.remove('active');
        completeBtn.style.background = '#ffffff';
        completeBtn.style.color = '#334155';
        completeBtn.style.borderColor = '#cbd5e1';
      }
    }

    updateBtn(isDone);

    completeBtn.addEventListener('click', () => {
      const current = localStorage.getItem(storageKey) === 'true';
      const next = !current;
      localStorage.setItem(storageKey, next ? 'true' : 'false');
      updateBtn(next);

      if (next && window.WhiteboardAnimations) {
        const rect = completeBtn.getBoundingClientRect();
        window.WhiteboardAnimations.triggerConfetti(rect.left + rect.width / 2, rect.top + rect.height / 2);
        window.WhiteboardAnimations.showToast('Chapter Marked Complete! Awesome job 🎉');
      }
    });
  }

  function initKaTeXRendering() {
    if (typeof renderMathInElement === 'function') {
      renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\(', right: '\\)', display: false },
          { left: '\\[', right: '\\]', display: true }
        ],
        throwOnError: false
      });
    }
  }

  function initSmartHeader() {
    const header = document.querySelector('.chapter-header');
    if (!header) return;

    // Create floating toggle pill if not already in DOM
    let togglePill = document.getElementById('headerTogglePill');
    if (!togglePill) {
      togglePill = document.createElement('button');
      togglePill.id = 'headerTogglePill';
      togglePill.className = 'header-toggle-pill';
      togglePill.setAttribute('aria-label', 'Show Navigation & Tabs');
      togglePill.innerHTML = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg> <span>Menu &amp; Tabs</span>';
      document.body.appendChild(togglePill);
    }

    let lastScrollY = window.scrollY;
    let ticking = false;
    const threshold = 10; // Minimum scroll delta

    function hideHeader() {
      header.classList.add('header-hidden');
      header.classList.remove('header-visible');
      document.body.classList.add('header-is-hidden');
    }

    function showHeader() {
      header.classList.remove('header-hidden');
      header.classList.add('header-visible');
      document.body.classList.remove('header-is-hidden');
    }

    function onScroll() {
      const currentScrollY = window.scrollY;

      // Always visible at the very top of the page
      if (currentScrollY <= 40) {
        showHeader();
        lastScrollY = currentScrollY;
        ticking = false;
        return;
      }

      const diff = currentScrollY - lastScrollY;
      if (Math.abs(diff) >= threshold) {
        if (diff > 0 && currentScrollY > 100) {
          // Scrolling DOWN: slide header UP to maximize reading area
          hideHeader();
        } else if (diff < 0) {
          // Scrolling UP: slide header DOWN to reveal navigation & tabs
          showHeader();
        }
        lastScrollY = currentScrollY;
      }
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(onScroll);
        ticking = true;
      }
    }, { passive: true });

    // Tap toggle pill to restore header
    togglePill.addEventListener('click', (e) => {
      e.preventDefault();
      showHeader();
    });

    // Bring header down whenever search trigger is activated
    document.querySelectorAll('.open-search-trigger').forEach(btn => {
      btn.addEventListener('click', showHeader);
    });
  }

  function init() {
    initChapterTabs();
    initSolutionAccordions();
    initPyqFilters();
    initGridToggle();
    initProgressTracker();
    initKaTeXRendering();
    initSmartHeader();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
