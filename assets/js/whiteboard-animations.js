/**
 * Whiteboard Interactive Micro-Animations & Student Action Triggers
 * Delivers lightweight confetti bursts, scroll-activated marker strokes,
 * rubber-stamp animations, and haptic-like visual feedback.
 */

(function () {
  'use strict';

  // 1. Reading Progress Bar
  function initReadingProgressBar() {
    let bar = document.querySelector('.reading-progress-bar');
    if (!bar) {
      bar = document.createElement('div');
      bar.className = 'reading-progress-bar';
      document.body.appendChild(bar);
    }

    window.addEventListener('scroll', () => {
      const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      bar.style.width = scrolled + '%';
    }, { passive: true });
  }

  // 2. IntersectionObserver for Marker Underlines, Stamps & Probability Bars
  function initScrollAnimations() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const el = entry.target;

          // Marker Underline
          if (el.classList.contains('marker-draw-line')) {
            el.classList.add('drawn');
          }

          // PYQ Stamp
          if (el.classList.contains('badge-pyq-stamp')) {
            el.classList.add('animate-stamp');
          }

          // Probability Fill
          if (el.classList.contains('prob-fill')) {
            const targetWidth = el.getAttribute('data-prob') || '85%';
            el.style.width = targetWidth;
          }

          observer.unobserve(el);
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll('.marker-draw-line, .badge-pyq-stamp, .prob-fill').forEach(el => {
      observer.observe(el);
    });
  }

  // 3. Lightweight Confetti Particle Burst for Step-Check Action
  function triggerConfetti(x, y) {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '9999';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ['#1d4ed8', '#15803d', '#dc2626', '#f59e0b', '#7e22ce', '#38bdf8'];

    for (let i = 0; i < 35; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 6 + 2;
      particles.push({
        x: x,
        y: y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed - 2,
        size: Math.random() * 6 + 3,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 1,
        rotation: Math.random() * 360,
        vRot: (Math.random() - 0.5) * 10
      });
    }

    let start = null;
    function frame(ts) {
      if (!start) start = ts;
      const progress = ts - start;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      let alive = false;
      particles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.2; // gravity
        p.alpha -= 0.02;
        p.rotation += p.vRot;

        if (p.alpha > 0) {
          alive = true;
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = Math.max(0, p.alpha);
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 0.7);
          ctx.restore();
        }
      });

      if (alive && progress < 1500) {
        requestAnimationFrame(frame);
      } else {
        canvas.remove();
      }
    }

    requestAnimationFrame(frame);
  }

  // 4. Step Understanding Checkboxes Listener
  function initStepCheckboxes() {
    document.addEventListener('change', (e) => {
      if (e.target && e.target.classList.contains('step-checkbox')) {
        if (e.target.checked) {
          const rect = e.target.getBoundingClientRect();
          triggerConfetti(rect.left + rect.width / 2, rect.top + rect.height / 2);
          showToast('Step Understood! Great progress ⭐');
          
          // Highlight card border gently
          const row = e.target.closest('.step-row') || e.target.closest('.question-card');
          if (row) {
            row.style.transition = 'background-color 0.4s ease';
            row.style.backgroundColor = 'rgba(240, 253, 244, 0.6)';
          }
        }
      }
    });
  }

  // 5. Toast Notification System
  function showToast(message) {
    let toast = document.querySelector('.copy-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'copy-toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2400);
  }

  // 6. Formula Click-to-Copy
  function initFormulaCopy() {
    document.addEventListener('click', (e) => {
      const formulaEl = e.target.closest('.formula-latex-display');
      if (formulaEl) {
        const tex = formulaEl.getAttribute('data-tex') || formulaEl.textContent.trim();
        if (navigator.clipboard) {
          navigator.clipboard.writeText(tex).then(() => {
            showToast('Formula LaTeX copied! 📋');
          });
        }
      }
    });
  }

  // Initialize
  function init() {
    initReadingProgressBar();
    initScrollAnimations();
    initStepCheckboxes();
    initFormulaCopy();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.WhiteboardAnimations = {
    triggerConfetti,
    showToast,
    refreshObservers: initScrollAnimations
  };
})();
