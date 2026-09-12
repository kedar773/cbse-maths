/**
 * Contact & Feedback Modal Controller
 * Connects directly to instructor Kedar Krishna (chemistrykedar@gmail.com)
 * Sourced from Kedar's Academy CBSE Teaching Centers (Bhubaneswar)
 */
(function () {
  'use strict';

  function initContactModal() {
    const modal = document.getElementById('contactModal');
    if (!modal) return;

    const triggers = document.querySelectorAll('.contact-modal-trigger, #contactModalToggle, #footerContactBtn');
    const closeBtn = document.getElementById('closeContactModal');
    const form = document.getElementById('feedbackForm');

    function openModal() {
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    triggers.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', closeModal);
    }

    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });

    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('fbName')?.value || '';
        const targetClass = document.getElementById('fbClass')?.value || '';
        const subject = document.getElementById('fbSubject')?.value || '';
        const message = document.getElementById('fbMessage')?.value || '';

        const mailSubject = encodeURIComponent(`[Kedar's Academy Math Engine] ${subject} (${targetClass})`);
        const mailBody = encodeURIComponent(
          `Hi Kedar Krishna,\n\nName: ${name}\nTarget: ${targetClass}\nTopic: ${subject}\n\nMessage/Doubt:\n${message}\n\n---\nSent via Kedar's Academy Mathematics Engine`
        );

        window.location.href = `mailto:chemistrykedar@gmail.com?subject=${mailSubject}&body=${mailBody}`;

        if (window.WhiteboardAnimations && typeof window.WhiteboardAnimations.showToast === 'function') {
          window.WhiteboardAnimations.showToast('Opening mail client to send message! 🎉');
        }
        closeModal();
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initContactModal);
  } else {
    initContactModal();
  }
})();
