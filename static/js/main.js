/* ============================================================
   ResumeAI — main.js
   Handles: drag-and-drop upload, file validation,
            role selection, loading overlay, score ring animation
   ============================================================ */

(function () {
  'use strict';

  // ─── Drag & Drop Upload ──────────────────────────────────────────
  const dropZone    = document.getElementById('dropZone');
  const resumeInput = document.getElementById('resumeInput');
  const dropContent = document.getElementById('dropContent');
  const filePreview = document.getElementById('filePreview');
  const fileName    = document.getElementById('fileName');
  const fileSize    = document.getElementById('fileSize');
  const removeFile  = document.getElementById('removeFile');
  const uploadForm  = document.getElementById('uploadForm');
  const analyzeBtn  = document.getElementById('analyzeBtn');

  if (dropZone) {
    // Click anywhere on drop zone to trigger file input
    dropZone.addEventListener('click', (e) => {
      if (!e.target.closest('.file-remove-btn') && !e.target.closest('.pick-btn')) {
        resumeInput.click();
      }
    });

    // Drag events
    ['dragenter', 'dragover'].forEach(ev => {
      dropZone.addEventListener(ev, (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
      });
    });

    ['dragleave', 'dragend', 'drop'].forEach(ev => {
      dropZone.addEventListener(ev, () => {
        dropZone.classList.remove('drag-over');
      });
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      const file = e.dataTransfer.files[0];
      if (file) handleFileSelection(file);
    });
  }

  if (resumeInput) {
    resumeInput.addEventListener('change', () => {
      if (resumeInput.files[0]) handleFileSelection(resumeInput.files[0]);
    });
  }

  if (removeFile) {
    removeFile.addEventListener('click', (e) => {
      e.stopPropagation();
      clearFileSelection();
    });
  }

  function handleFileSelection(file) {
    const allowed = ['application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!['pdf', 'docx'].includes(ext)) {
      showToast('⚠️ Only PDF and DOCX files are supported.', 'error');
      return;
    }
    if (file.size > 16 * 1024 * 1024) {
      showToast('⚠️ File exceeds the 16 MB limit.', 'error');
      return;
    }

    // Update the real file input
    const dt = new DataTransfer();
    dt.items.add(file);
    resumeInput.files = dt.files;

    // Update UI
    if (fileName) fileName.textContent = file.name;
    if (fileSize) fileSize.textContent  = formatBytes(file.size);
    if (dropContent) dropContent.style.display = 'none';
    if (filePreview) filePreview.style.display  = 'flex';
  }

  function clearFileSelection() {
    resumeInput.value = '';
    if (dropContent) dropContent.style.display = '';
    if (filePreview) filePreview.style.display  = 'none';
  }

  function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  // ─── Role Selection Visual Feedback ─────────────────────────────
  const roleItems = document.querySelectorAll('.role-select-item');
  roleItems.forEach(item => {
    item.addEventListener('click', () => {
      roleItems.forEach(i => i.removeAttribute('data-selected'));
      item.setAttribute('data-selected', 'true');
    });
  });

  // ─── Form Submission + Loading Overlay ──────────────────────────
  if (uploadForm) {
    uploadForm.addEventListener('submit', (e) => {
      const file     = resumeInput && resumeInput.files[0];
      const roleEl   = document.querySelector('input[name="job_role"]:checked');

      if (!file) {
        e.preventDefault();
        showToast('⚠️ Please upload a resume file first.', 'error');
        return;
      }
      if (!roleEl) {
        e.preventDefault();
        showToast('⚠️ Please select a target job role.', 'error');
        return;
      }

      // Show loading overlay
      showLoadingOverlay();
    });
  }

  function showLoadingOverlay() {
    const overlay = document.getElementById('loadingOverlay');
    if (!overlay) return;
    overlay.style.display = 'flex';

    // Animate step transitions
    const steps   = overlay.querySelectorAll('.loading-step');
    let currentStep = 0;
    const delays   = [0, 1200, 2400, 3600, 4600];

    steps.forEach((step, i) => {
      setTimeout(() => {
        // Mark previous as done
        if (i > 0) {
          steps[i - 1].classList.remove('active');
          steps[i - 1].classList.add('done');
        }
        step.classList.add('active');
      }, delays[i]);
    });
  }

  // ─── Score Ring Animation (Result Page) ─────────────────────────
  const ringFill    = document.getElementById('ringFill');
  const scoreNumber = document.getElementById('scoreNumber');

  if (ringFill && typeof window.RESUME_SCORE !== 'undefined') {
    const score       = parseFloat(window.RESUME_SCORE) || 0;
    const circumference = 2 * Math.PI * 80; // r=80 → ~502.65

    // Start at offset=circumference (empty) and animate to score
    ringFill.style.strokeDashoffset = circumference;

    requestAnimationFrame(() => {
      setTimeout(() => {
        const offset = circumference - (score / 100) * circumference;
        ringFill.style.strokeDashoffset = offset;
      }, 300);
    });

    // Count-up animation for the number
    let current = 0;
    const duration = 1500;
    const step     = 16;
    const increment = score / (duration / step);

    const counter = setInterval(() => {
      current += increment;
      if (current >= score) {
        current = score;
        clearInterval(counter);
      }
      if (scoreNumber) scoreNumber.textContent = Math.round(current);
    }, step);
  }

  // ─── Chip Entrance Animation ──────────────────────────────────
  const chips = document.querySelectorAll('.chip');
  if (chips.length && 'IntersectionObserver' in window) {
    chips.forEach((chip, i) => {
      chip.style.opacity   = '0';
      chip.style.transform = 'translateY(8px)';
      chip.style.transition = `opacity 0.3s ease ${i * 0.03}s, transform 0.3s ease ${i * 0.03}s`;
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity   = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    chips.forEach(chip => observer.observe(chip));
  }

  // ─── Toast Notifications ─────────────────────────────────────
  function showToast(message, type = 'info') {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 2rem;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: ${type === 'error' ? 'rgba(239,68,68,0.95)' : 'rgba(59,130,246,0.95)'};
      color: #fff;
      padding: 0.875rem 1.5rem;
      border-radius: 10px;
      font-family: 'Inter', sans-serif;
      font-size: 0.875rem;
      font-weight: 600;
      z-index: 9999;
      opacity: 0;
      transition: all 0.3s ease;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      max-width: 90vw;
      text-align: center;
    `;
    document.body.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.opacity   = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(() => {
      toast.style.opacity   = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // ─── Smooth Scroll for anchor links ──────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ─── Fade-in Cards on Scroll ──────────────────────────────────
  if ('IntersectionObserver' in window) {
    const cards = document.querySelectorAll('.step-card, .feature-card, .role-card');
    cards.forEach((card, i) => {
      card.style.opacity   = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = `opacity 0.4s ease ${i * 0.08}s, transform 0.4s ease ${i * 0.08}s`;
    });

    const cardObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity   = '1';
          entry.target.style.transform = 'translateY(0)';
          cardObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    cards.forEach(card => cardObserver.observe(card));
  }

})();
