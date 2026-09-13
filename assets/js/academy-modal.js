/**
 * Kedar's STEM Academy - Unified Cross-Subject Navigation Modal
 * Whiteboard Edition for CBSE Mathematics
 */
(function() {
  'use strict';

  const ACADEMY_SITES = [
    {
      id: 'physics',
      name: "Kedar's Physics Engine",
      subject: "Physics",
      badge: "CBSE 11 & 12 • NCERT Pure-Line",
      badgeClass: "badge-physics",
      icon: "⚛️",
      tagline: "First-principles derivations, 25 NCERT pure-line chapters, 2020–2025 CBSE PYQ vault with step-wise rubrics, and 8 interactive HTML5 physics lab simulations.",
      url: "https://kedar773.github.io/cbse-physics/",
      action: "Enter Physics Engine"
    },
    {
      id: 'maths',
      name: "Kedar's Mathematics Engine",
      subject: "Mathematics",
      badge: "CBSE 11 & 12 • Step-by-Step Rigor",
      badgeClass: "badge-maths",
      icon: "📐",
      tagline: "Full 27-chapter digital whiteboard with NCERT line notes, official CBSE marking breakdowns, 5-year PYQ archive, formula proof sheets, and built-in problem-solving scratchpad.",
      url: "https://kedar773.github.io/cbse-maths/",
      action: "Enter Mathematics Engine"
    },
    {
      id: 'chemistry',
      name: "Kedar's Chemistry Engine",
      subject: "Chemistry",
      badge: "CBSE 11 & 12 • Physical, Inorganic, Organic",
      badgeClass: "badge-chemistry",
      icon: "🧪",
      tagline: "19 NCERT chapters with 3D WebGL molecular orbital models, step-by-step reaction mechanism pathways, and high-yield JEE Advanced preparation guides.",
      url: "https://kedar773.github.io/cbse-chemistry-alt/",
      action: "Enter Chemistry Engine"
    }
  ];

  function createAcademyModal() {
    if (document.getElementById('academyModalOverlay')) return;

    const currentSiteId = 'maths';

    const cardsHtml = ACADEMY_SITES.map(site => {
      const isCurrent = site.id === currentSiteId;
      const cardClass = `academy-card card-${site.id} ${isCurrent ? 'is-current' : ''}`;
      const statusHtml = isCurrent
        ? `<span class="academy-status-current">Current Subject 📍</span>`
        : `<span class="academy-status-available">Available</span>`;
      const actionHtml = isCurrent
        ? `<span>Currently Browsing</span>`
        : `<span>${site.action}</span><span class="academy-arrow">&rarr;</span>`;

      return `
        <a href="${site.url}" class="${cardClass}" ${isCurrent ? 'aria-current="page"' : ''}>
          <div class="academy-card-top">
            <span class="academy-card-badge ${site.badgeClass}">${site.icon} ${site.subject || site.name.split(' ')[1] || site.id.toUpperCase()}</span>
            ${statusHtml}
          </div>
          <h3 class="academy-card-title">${site.name}</h3>
          <p class="academy-card-desc">${site.tagline}</p>
          <div class="academy-card-action">
            ${actionHtml}
          </div>
        </a>
      `;
    }).join('');

    const modal = document.createElement('div');
    modal.id = 'academyModalOverlay';
    modal.className = 'academy-modal-overlay';
    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    modal.innerHTML = `
      <div class="academy-modal-dialog" role="dialog" aria-labelledby="academyModalTitle">
        <div class="academy-modal-header">
          <div class="academy-brand-title">
            <span class="academy-header-emblem">🏛️</span>
            <div>
              <h2 id="academyModalTitle" class="academy-title">Kedar's STEM Academy</h2>
              <p class="academy-subtitle">Unified Senior Secondary &amp; Competitive Learning Architecture</p>
            </div>
          </div>
          <button type="button" class="academy-modal-close" id="closeAcademyModalBtn" aria-label="Close Academy Hub">&times;</button>
        </div>
        
        <div class="academy-modal-body">
          <p class="academy-intro-note">
            Seamlessly switch between Senior Secondary Mathematics, Physics, and Chemistry study engines. All platforms are strictly NCERT pure-line compliant with verified CBSE PYQ vaults and competitive modules.
          </p>

          <div class="academy-grid">
            ${cardsHtml}
          </div>

          <div class="academy-footer-meta">
            <div class="academy-mentor-info">
              <span>👨‍🏫 Mentored by <strong>Kedar Krishna</strong></span>
              <span class="academy-dot">&bull;</span>
              <span>Bhubaneswar Centers: <em>Arundhati Vihar</em> &amp; <em>Jagannath Vihar</em></span>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const closeBtn = modal.querySelector('#closeAcademyModalBtn');
    if (closeBtn) {
      closeBtn.addEventListener('click', closeAcademyModal);
    }

    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        closeAcademyModal();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.style.display === 'flex') {
        closeAcademyModal();
      }
    });
  }

  function openAcademyModal(e) {
    if (e && e.preventDefault) e.preventDefault();
    createAcademyModal();
    const modal = document.getElementById('academyModalOverlay');
    if (modal) {
      modal.style.display = 'flex';
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeAcademyModal() {
    const modal = document.getElementById('academyModalOverlay');
    if (modal) {
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  function bindTriggers() {
    const triggers = document.querySelectorAll('.academy-modal-trigger, #academyModalToggle, .academy-toggle-btn');
    triggers.forEach(btn => {
      btn.removeEventListener('click', openAcademyModal);
      btn.addEventListener('click', openAcademyModal);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      createAcademyModal();
      bindTriggers();
    });
  } else {
    createAcademyModal();
    bindTriggers();
  }

  window.openAcademyModal = openAcademyModal;
  window.closeAcademyModal = closeAcademyModal;
})();
