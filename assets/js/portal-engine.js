/**
 * Whiteboard Portal Engine (Home Hub)
 * Handles Class 11/12 switcher, domain filters, mastery tracking, and stats HUD.
 */

(function () {
  'use strict';

  function initClassSwitcher() {
    const classTabs = document.querySelectorAll('.portal-class-tab');
    const classSections = document.querySelectorAll('.class-directory-section');

    classTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const targetClass = tab.getAttribute('data-class'); // '11' or '12'

        classTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        classSections.forEach(sec => {
          if (sec.getAttribute('data-class') === targetClass) {
            sec.style.display = 'block';
          } else {
            sec.style.display = 'none';
          }
        });
      });
    });
  }

  function initDomainFilters() {
    const chips = document.querySelectorAll('.domain-filter-chip');
    const cards = document.querySelectorAll('.chapter-card');

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        chips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');

        const domain = chip.getAttribute('data-domain'); // 'all', 'calculus', 'algebra', etc.

        cards.forEach(card => {
          if (domain === 'all') {
            card.style.display = 'flex';
            return;
          }

          const cardDomain = (card.getAttribute('data-domain') || '').toLowerCase();
          if (cardDomain === domain.toLowerCase()) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  function updateMasteryStats() {
    const cards = document.querySelectorAll('.chapter-card');
    let completed = 0;

    cards.forEach(card => {
      const slug = card.getAttribute('data-slug');
      if (slug && localStorage.getItem('cbse_maths_completed_' + slug) === 'true') {
        completed++;
        const badge = card.querySelector('.completion-indicator');
        if (badge) {
          badge.innerHTML = '✓ Mastered';
          badge.style.background = '#15803d';
          badge.style.color = '#ffffff';
        }
      }
    });

    const statEl = document.getElementById('statMasteredCount');
    if (statEl) {
      statEl.textContent = completed;
    }
  }

  function initHeroSearch() {
    const heroInput = document.getElementById('heroSearchInput');
    if (heroInput && window.WhiteboardSearch) {
      heroInput.addEventListener('focus', () => {
        window.WhiteboardSearch.open();
      });
      heroInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          window.WhiteboardSearch.open(heroInput.value);
        }
      });
    }
  }

  function init() {
    initClassSwitcher();
    initDomainFilters();
    updateMasteryStats();
    initHeroSearch();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
