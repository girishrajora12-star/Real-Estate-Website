/**
 * @license
 * KAVAL Architecture & Interiors
 * Award-Style Cinematic Showcase
 */

// =========================================================================
// WALKTHROUGH COPY & TIMESTAMPS (Easily customize narrative lines & timings)
// Total video duration: 20.06 seconds
// Edit text or timestamp (in seconds) to adjust lines synced to the video
// =========================================================================
export const WALKTHROUGH_TOTAL_DURATION = 20.06;

export const WALKTHROUGH_CUES = [
  { time: 0,  text: "Home begins\nat the doorstep." },
  { time: 2,  text: "Crafted in teak,\nbuilt to welcome." },
  { time: 3,  text: "Bring the garden\ninside." },
  { time: 5,  text: "Rooms that invite\nyou to stay." },
  { time: 7,  text: "Long dinners.\nOpen views." },
  { time: 8,  text: "Privacy, without\nclosing off." },
  { time: 10, text: "Stairs that feel\nlike sculpture." },
  { time: 12, text: "Details with\na story." },
  { time: 13, text: "Every step\nsoftly lit." },
  { time: 15, text: "Tradition on\nevery wall." },
  { time: 17, text: "Slow down.\nSwing a little." },
  { time: 18, text: "Wake up above\nthe treetops." }
];

window.addEventListener('DOMContentLoaded', () => {
  initApp();
});

function initApp() {
  const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = window.innerWidth < 768 || ('ontouchstart' in window);

  // Register GSAP ScrollTrigger
  if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // Smooth scroll helper for anchors
  const scrollToTarget = (target) => {
    if (typeof target === 'number') {
      window.scrollTo({ top: target, behavior: 'smooth' });
    } else {
      const el = typeof target === 'string' ? document.querySelector(target) : target;
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  // =========================================================================
  // 1. CUSTOM CURSOR
  // =========================================================================
  initCustomCursor();

  function initCustomCursor() {
    if (isMobile) return;
    const cursor = document.querySelector('.custom-cursor');
    const label = document.querySelector('.cursor-label');
    if (!cursor) return;

    const setX = gsap.quickTo(cursor, 'x', { duration: 0.18, ease: 'power3.out' });
    const setY = gsap.quickTo(cursor, 'y', { duration: 0.18, ease: 'power3.out' });

    window.addEventListener('mousemove', (e) => {
      setX(e.clientX);
      setY(e.clientY);
    });

    document.querySelectorAll('[data-cursor]').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        const type = el.getAttribute('data-cursor');
        cursor.classList.add('is-expanded');
        if (label) {
          label.textContent = type === 'play' ? 'PLAY' : 'VIEW';
        }
      });
      el.addEventListener('mouseleave', () => {
        cursor.classList.remove('is-expanded');
      });
    });

    document.addEventListener('mouseleave', () => {
      cursor.style.opacity = '0';
    });
    document.addEventListener('mouseenter', () => {
      cursor.style.opacity = '1';
    });
  }

  // =========================================================================
  // 2. PRELOADER & INTRO TIMELINE
  // =========================================================================
  initPreloader();

  function initPreloader() {
    const preloader = document.querySelector('.preloader');
    const counterEl = document.querySelector('.preloader-counter');
    const barEl = document.querySelector('.preloader-bar');

    let counter = { val: 0 };

    gsap.to(counter, {
      val: 100,
      duration: 1.4,
      ease: 'power2.out',
      onUpdate: () => {
        const rounded = Math.floor(counter.val);
        if (counterEl) counterEl.textContent = rounded.toString().padStart(2, '0');
        if (barEl) barEl.style.width = `${rounded}%`;
      },
      onComplete: () => {
        gsap.to(preloader, {
          yPercent: -100,
          duration: 1.0,
          ease: 'expo.inOut',
          onComplete: () => {
            if (preloader) preloader.style.display = 'none';
            ScrollTrigger.refresh();
            playHeroIntro();
          }
        });
      }
    });
  }

  function playHeroIntro() {
    const tl = gsap.timeline();

    tl.fromTo('.floating-nav',
      { y: -30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.9, ease: 'power3.out' },
      0.2
    );

    tl.fromTo(['.hero-top-meta', '.hero-bottom-grid', '.hero-chapters-container'],
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.9, stagger: 0.12, ease: 'power3.out' },
      0.4
    );
  }

  // =========================================================================
  // 3. FLOATING PILL NAV BEHAVIOR
  // =========================================================================
  initNavigation();

  function initNavigation() {
    const nav = document.querySelector('.floating-nav');
    if (!nav) return;

    window.addEventListener('scroll', () => {
      if (window.scrollY > 80) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    });

    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        if (targetId && targetId.startsWith('#')) {
          scrollToTarget(targetId);
        }
      });
    });

    const brand = document.querySelector('.nav-brand');
    if (brand) {
      brand.addEventListener('click', (e) => {
        e.preventDefault();
        scrollToTarget(0);
      });
    }
  }

  // =========================================================================
  // 4. SECTION 1: HERO SCROLL-CONTROLLED FRAME WALKTHROUGH
  //    300 frames from the 20s walkthrough video played on Canvas on scroll
  //    Zero video file needed in codebase; smooth frame-by-frame scrub
  // =========================================================================
  initHeroWalkthrough();

  function initHeroWalkthrough() {
    const heroSection = document.querySelector('#hero');
    const canvas = document.querySelector('#heroCanvas');
    const progressFill = document.querySelector('.hero-progress-fill');
    const chapters = document.querySelectorAll('.hero-chapter');

    if (!heroSection || !canvas) return;

    const ctx = canvas.getContext('2d', { alpha: false });
    let totalFrames = 150;
    let videoDuration = 20.06;
    let frameImages = new Array(totalFrames);
    let lastDrawnIndex = 0;
    let targetFrameIndex = 0;
    let currentFrameIndex = 0;

    const getFramePath = (idx) => {
      const num = Math.min(totalFrames, Math.max(1, idx + 1));
      return `/assets/frames/frame_${num.toString().padStart(4, '0')}.jpg`;
    };

    // Fast cover-fit drawer maintaining natural aspect ratio
    const drawCoverImage = (img) => {
      if (!img) return;
      const cw = canvas.width;
      const ch = canvas.height;
      const iw = img.naturalWidth || img.videoWidth || img.width;
      const ih = img.naturalHeight || img.videoHeight || img.height;
      if (!iw || !ih) return;

      const scale = Math.max(cw / iw, ch / ih);
      const nw = iw * scale;
      const nh = ih * scale;
      const ox = (cw - nw) * 0.5;
      const oy = (ch - nh) * 0.5;

      ctx.drawImage(img, 0, 0, iw, ih, ox, oy, nw, nh);
    };

    // Draw frame at index or nearest available loaded frame
    const drawFrame = (index) => {
      const clamped = Math.min(totalFrames - 1, Math.max(0, index));
      const targetImg = frameImages[clamped];

      if (targetImg && targetImg.complete && targetImg.naturalWidth > 0) {
        drawCoverImage(targetImg);
        lastDrawnIndex = clamped;
        return;
      }

      // If requested frame is still buffering, draw nearest loaded frame
      for (let offset = 1; offset < 40; offset++) {
        const left = clamped - offset;
        if (left >= 0 && frameImages[left]?.complete && frameImages[left].naturalWidth > 0) {
          drawCoverImage(frameImages[left]);
          return;
        }
        const right = clamped + offset;
        if (right < totalFrames && frameImages[right]?.complete && frameImages[right].naturalWidth > 0) {
          drawCoverImage(frameImages[right]);
          return;
        }
      }

      if (frameImages[lastDrawnIndex]?.complete && frameImages[lastDrawnIndex].naturalWidth > 0) {
        drawCoverImage(frameImages[lastDrawnIndex]);
      }
    };

    // Size canvas with device pixel ratio
    const resizeCanvas = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.floor(window.innerWidth * dpr);
      canvas.height = Math.floor(window.innerHeight * dpr);
      drawFrame(Math.round(currentFrameIndex));
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Preload extracted frames from House Walkthrough Website.mp4
    const ensureFrameLoaded = (idx) => {
      const clamped = Math.min(totalFrames - 1, Math.max(0, idx));
      if (!frameImages[clamped]) {
        const img = new Image();
        img.src = getFramePath(clamped);
        frameImages[clamped] = img;
      }
    };

    // Preload extracted frames intelligently for smooth scrub
    const loadFrames = (count) => {
      totalFrames = count || totalFrames;
      frameImages = new Array(totalFrames);

      // Load frame 1 immediately
      const firstImg = new Image();
      firstImg.src = getFramePath(0);
      firstImg.onload = () => {
        frameImages[0] = firstImg;
        drawCoverImage(firstImg);
        if (typeof ScrollTrigger !== 'undefined') {
          ScrollTrigger.refresh();
        }
      };
      frameImages[0] = firstImg;

      // Pass 1: Keyframe stride for immediate scrub coverage across whole timeline
      const stride = totalFrames > 300 ? 10 : 3;
      for (let i = 0; i < totalFrames; i += stride) {
        ensureFrameLoaded(i);
      }

      // Pass 2: Buffer initial 35 frames
      for (let i = 1; i < Math.min(35, totalFrames); i++) {
        ensureFrameLoaded(i);
      }
    };

    // Start loading frames immediately
    loadFrames(totalFrames);

    // Sync manifest parameters and expose reloader
    const syncManifest = async () => {
      try {
        const res = await fetch(`/assets/frames/manifest.json?t=${Date.now()}`);
        if (res.ok) {
          const data = await res.json();
          if (data && data.totalFrames) {
            totalFrames = data.totalFrames;
            videoDuration = data.duration || 20.0;
            loadFrames(totalFrames);
          }
        }
      } catch (e) {}
    };

    window.reloadWalkthroughFrames = syncManifest;
    syncManifest();

    // Smooth render tick loop (interpolates between frames when scrolling)
    function tick() {
      const diff = targetFrameIndex - currentFrameIndex;
      if (Math.abs(diff) > 0.05) {
        currentFrameIndex += diff * 0.35;
        drawFrame(Math.round(currentFrameIndex));

        // Buffer lookahead frames around scroll position
        const center = Math.round(targetFrameIndex);
        for (let i = -12; i <= 24; i++) {
          ensureFrameLoaded(center + i);
        }
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);

    const setChapter = (index) => {
      chapters.forEach((ch, idx) => {
        if (idx === index) {
          ch.classList.add('active');
        } else {
          ch.classList.remove('active');
        }
      });
    };

    if (typeof ScrollTrigger !== 'undefined') {
      ScrollTrigger.create({
        trigger: heroSection,
        start: 'top top',
        end: '+=400%',
        pin: true,
        pinSpacing: true,
        anticipatePin: 1,
        onUpdate: (self) => {
          const progress = Math.min(1, Math.max(0, self.progress));
          targetFrameIndex = progress * (totalFrames - 1);

          // Vertical progress bar fill
          if (progressFill) {
            progressFill.style.height = `${(progress * 100).toFixed(1)}%`;
          }

          // 12 Scene headings synced across the walkthrough timeline
          const cues = [0, 1.8, 3.4, 5.2, 7.0, 8.8, 10.6, 12.4, 14.2, 16.0, 17.8, 19.2];
          const currentSec = progress * videoDuration;
          let activeIndex = 0;
          for (let i = cues.length - 1; i >= 0; i--) {
            if (currentSec >= cues[i] - 0.1) {
              activeIndex = i;
              break;
            }
          }
          setChapter(activeIndex);
        }
      });
    }
  }

  // =========================================================================
  // 5. SECTION 2: INTRO + FLOATING CARDS
  //    Revealed directly when the video finishes to the end!
  // =========================================================================
  initIntroCards();

  function initIntroCards() {
    if (typeof ScrollTrigger !== 'undefined') {
      gsap.from('.intro-headline .line', {
        yPercent: 110,
        duration: 1.1,
        stagger: 0.12,
        ease: 'power4.out',
        scrollTrigger: {
          trigger: '.intro-cards-section',
          start: 'top 75%'
        }
      });
    }

    const cardTilts = [-5, 6, -4, 5];
    const cards = document.querySelectorAll('.floating-room-card');

    cards.forEach((card, i) => {
      if (!isMobile) {
        card.style.transform = `rotate(${cardTilts[i % cardTilts.length]}deg)`;
      }

      if (typeof ScrollTrigger !== 'undefined' && !isMobile) {
        const speed = (i % 2 === 0 ? -30 : 40);
        gsap.to(card, {
          y: speed,
          ease: 'none',
          scrollTrigger: {
            trigger: card,
            start: 'top 90%',
            end: 'bottom 10%',
            scrub: 1
          }
        });
      }

      const favBtn = card.querySelector('.card-favorite-btn');
      if (favBtn) {
        favBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          favBtn.classList.toggle('active');
          const isFav = favBtn.classList.contains('active');
          favBtn.innerHTML = isFav
            ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="#E63946"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`
            : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>`;
        });
      }

      card.addEventListener('click', () => {
        const title = card.querySelector('.card-title')?.textContent || 'Room Details';
        openModal(`Curated Space: ${title}`, `Explore material finishes, floor plans, and daylight choreography for ${title}.`);
      });
    });

    const searchInput = document.querySelector('.search-pill-input');
    const searchBtn = document.querySelector('.search-pill-btn');

    const filterCards = () => {
      const q = (searchInput?.value || '').toLowerCase().trim();
      cards.forEach(card => {
        const title = (card.querySelector('.card-title')?.textContent || '').toLowerCase();
        const meta = (card.querySelector('.card-meta')?.textContent || '').toLowerCase();
        if (!q || title.includes(q) || meta.includes(q)) {
          card.style.display = 'block';
          card.style.opacity = '1';
        } else {
          card.style.opacity = '0.2';
        }
      });
    };

    if (searchInput) searchInput.addEventListener('input', filterCards);
    if (searchBtn) searchBtn.addEventListener('click', filterCards);
  }

  // =========================================================================
  // 6. SECTION 3: PROJECT LIST
  // =========================================================================
  initProjectList();

  function initProjectList() {
    const listWrapper = document.querySelector('.project-items-wrapper');
    const rows = document.querySelectorAll('.project-row');

    if (typeof ScrollTrigger !== 'undefined' && listWrapper) {
      gsap.fromTo(listWrapper,
        { rotateX: 14, opacity: 0.6 },
        {
          rotateX: 0,
          opacity: 1,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: '.project-list-section',
            start: 'top 80%',
            end: 'top 30%',
            scrub: 1
          }
        }
      );
    }

    rows.forEach((row) => {
      const btn = row.querySelector('.project-preview-btn');
      const title = row.querySelector('.project-title-lockup')?.textContent?.trim() || 'Architecture Project';

      if (btn) {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          openModal(title, `Schedule an architectural walkthrough or view complete construction documentation for ${title}.`);
        });
      }

      row.addEventListener('click', () => {
        openModal(title, `Schedule an architectural walkthrough or view complete construction documentation for ${title}.`);
      });
    });
  }

  // =========================================================================
  // 7. SECTION 4: DUSK IMAGE WITH FLOATING TAGS
  // =========================================================================
  initDuskSection();

  function initDuskSection() {
    const duskImg = document.querySelector('.dusk-image');
    const tags = document.querySelectorAll('.dusk-tag');

    if (typeof ScrollTrigger !== 'undefined' && duskImg) {
      gsap.fromTo(duskImg,
        { scale: 1.12 },
        {
          scale: 1.0,
          ease: 'none',
          scrollTrigger: {
            trigger: '.dusk-section',
            start: 'top bottom',
            end: 'bottom top',
            scrub: true
          }
        }
      );
    }

    // Feature definitions for Section 4 interactive popups
    const FEATURE_DETAILS = {
      'teak-cladding': {
        category: 'Façade & Materiality',
        title: 'Teak Wood Cladding',
        description: 'Sustainably sourced Indonesian reclaimed teak, kiln-seasoned and hand-planed to endure tropical climates and coastal weathering. Finished with organic tung oil to preserve the rich amber grain and velvety tactile depth while forming a breathable, high-performance thermal exterior envelope.',
        specs: [
          { label: 'Origin', value: 'East Java Aged Timber' },
          { label: 'Profile', value: '28mm Solid Tongue & Groove' },
          { label: 'Finish', value: 'Organic Zero-VOC Tung Oil' },
          { label: 'Thermal Envelope', value: 'Natural Aerated R-Value' }
        ]
      },
      'smart-climate': {
        category: 'Passive Engineering & Automation',
        title: 'Smart Climate & Thermal Architecture',
        description: 'An intelligent hybrid climate system orchestrating hidden sub-slab geothermal channels with motorized solid teak louvers. Discrete microclimate sensors track wind angles, solar azimuth, and ambient humidity to modulate natural cross-ventilation silently with zero acoustic distraction.',
        specs: [
          { label: 'Sensory Grid', value: 'Multi-Zone Air Quality & Temp' },
          { label: 'Circulation', value: 'Passive Solar Thermal Chimney' },
          { label: 'Automation', value: 'Concealed Bus Architecture' },
          { label: 'Efficiency', value: '42% Lower Active HVAC Draw' }
        ]
      },
      'warm-lighting': {
        category: 'Atmospheric Illumination',
        title: 'Warm Pendant Lighting',
        description: 'Hand-blown amber art-glass spheres suspended from spun brass armatures, calibrated for evening circadian calm. Dual-circuit dimming curves transition from daytime clarity to a rich 2200K amber glow that grazes natural stone and timber textures.',
        specs: [
          { label: 'Color Temp', value: '2200K – 2700K Warm Dimming' },
          { label: 'Glasswork', value: 'Handcrafted Mouth-Blown Amber' },
          { label: 'Hardware', value: 'Spun Brass with Natural Patina' },
          { label: 'Control', value: 'Phase-Adaptive Architectural Drivers' }
        ]
      }
    };

    const featureModal = document.getElementById('featureModal');
    const featureModalTitle = document.getElementById('featureModalTitle');
    const featureModalCategory = document.getElementById('featureModalCategory');
    const featureModalDesc = document.getElementById('featureModalDesc');
    const featureModalSpecs = document.getElementById('featureModalSpecs');
    const featureModalClose = document.querySelector('.feature-modal-close-btn');
    const featureModalDismiss = document.querySelector('.feature-modal-dismiss-btn');
    const featureModalAction = document.querySelector('.feature-modal-action-btn');

    function openFeaturePopup(key) {
      const data = FEATURE_DETAILS[key] || FEATURE_DETAILS['teak-cladding'];
      if (!featureModal) return;

      if (featureModalTitle) featureModalTitle.textContent = data.title;
      if (featureModalCategory) featureModalCategory.textContent = data.category;
      if (featureModalDesc) featureModalDesc.textContent = data.description;

      if (featureModalSpecs) {
        featureModalSpecs.innerHTML = data.specs.map((s) => `
          <div class="feature-spec-item">
            <span class="spec-label">${s.label}</span>
            <span class="spec-value">${s.value}</span>
          </div>
        `).join('');
      }

      featureModal.classList.add('is-open');
    }

    function closeFeaturePopup() {
      if (featureModal) featureModal.classList.remove('is-open');
    }

    if (featureModalClose) featureModalClose.addEventListener('click', closeFeaturePopup);
    if (featureModalDismiss) featureModalDismiss.addEventListener('click', closeFeaturePopup);
    if (featureModal) {
      featureModal.addEventListener('click', (e) => {
        if (e.target === featureModal) closeFeaturePopup();
      });
    }

    if (featureModalAction) {
      featureModalAction.addEventListener('click', () => {
        const title = featureModalTitle ? featureModalTitle.textContent : 'Architectural Detail';
        closeFeaturePopup();
        openModal(`Commission Detail: ${title}`, `Please share your site location and requirements. Our architects will integrate ${title} into your custom floor plan.`);
      });
    }

    tags.forEach((tag, idx) => {
      gsap.to(tag, {
        y: idx % 2 === 0 ? -10 : 10,
        duration: 3 + idx * 0.5,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: idx * 0.3
      });

      tag.addEventListener('click', () => {
        const featureKey = tag.getAttribute('data-feature') || 'teak-cladding';
        openFeaturePopup(featureKey);
      });
    });
  }

  // =========================================================================
  // 8. SECTION 5: PROCESS (HORIZONTAL SCROLL - 4 POINTS ONLY)
  //    Seamlessly transitions to footer CTA with zero black gap
  // =========================================================================
  initProcessScroll();

  function initProcessScroll() {
    const track = document.querySelector('.process-track');
    const container = document.querySelector('.process-pinned-container');

    if (typeof ScrollTrigger !== 'undefined' && track && container && !isMobile) {
      // Calculate exact distance to scroll through all 4 panels without any overscroll or black screen
      const getScrollDistance = () => track.scrollWidth - window.innerWidth;

      gsap.to(track, {
        x: () => -getScrollDistance(),
        ease: 'none',
        scrollTrigger: {
          trigger: container,
          pin: true,
          scrub: 1.2,
          start: 'top top',
          end: () => `+=${getScrollDistance() + 200}`,
          anticipatePin: 1,
          invalidateOnRefresh: true
        }
      });
    }
  }

  // =========================================================================
  // 9. SECTION 6: FOOTER & MAGNETIC BUTTON
  // =========================================================================
  initFooter();

  function initFooter() {
    const magnetBtn = document.querySelector('.magnetic-circle-btn');
    const magnetWrap = document.querySelector('.magnetic-btn-wrap');

    if (magnetBtn && magnetWrap && !isMobile) {
      const setX = gsap.quickTo(magnetBtn, 'x', { duration: 0.3, ease: 'power3.out' });
      const setY = gsap.quickTo(magnetBtn, 'y', { duration: 0.3, ease: 'power3.out' });

      magnetWrap.addEventListener('mousemove', (e) => {
        const rect = magnetWrap.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const dist = Math.hypot(e.clientX - centerX, e.clientY - centerY);

        if (dist < 100) {
          const offsetX = (e.clientX - centerX) * 0.45;
          const offsetY = (e.clientY - centerY) * 0.45;
          setX(offsetX);
          setY(offsetY);
        }
      });

      magnetWrap.addEventListener('mouseleave', () => {
        setX(0);
        setY(0);
      });
    }

    if (magnetBtn) {
      magnetBtn.addEventListener('click', () => {
        openModal("Start a Project", "Tell us about your property, desired square footage, and timeline.");
      });
    }

    const backToTop = document.querySelector('.back-to-top-btn');
    if (backToTop) {
      backToTop.addEventListener('click', () => {
        scrollToTarget(0);
      });
    }

    const navCta = document.querySelector('.nav-cta');
    if (navCta) {
      navCta.addEventListener('click', (e) => {
        e.preventDefault();
        openModal("Commission an Architectural Sanctuary", "Connect with KAVAL's lead partners in Bali, Tokyo, or Zurich.");
      });
    }
  }

  // =========================================================================
  // 10. INTERACTIVE MODAL & FORM
  // =========================================================================
  const modal = document.querySelector('.modal-overlay');
  const modalTitle = document.querySelector('.modal-title');
  const modalDesc = document.querySelector('.modal-desc');
  const modalClose = document.querySelector('.modal-close-btn');
  const modalForm = document.querySelector('.modal-form');

  function openModal(title, desc) {
    if (modalTitle) modalTitle.textContent = title;
    if (modalDesc) modalDesc.textContent = desc;
    if (modal) modal.classList.add('is-open');
  }

  function closeModal() {
    if (modal) modal.classList.remove('is-open');
  }

  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal();
      const fModal = document.getElementById('featureModal');
      if (fModal) fModal.classList.remove('is-open');
    }
  });

  if (modalForm) {
    modalForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = modalForm.querySelector('.form-submit-btn');
      if (submitBtn) {
        submitBtn.textContent = 'Commission Inquiry Sent';
        submitBtn.style.background = '#F2A24B';
        submitBtn.style.color = '#000';
      }
      setTimeout(() => {
        closeModal();
        if (submitBtn) {
          submitBtn.textContent = 'Submit Inquiry';
          submitBtn.style.background = '';
          submitBtn.style.color = '';
        }
      }, 1400);
    });
  }

  // =========================================================================
  // 11. WALKTHROUGH VIDEO & FRAME MANAGER
  // =========================================================================
  initVideoManager();

  function initVideoManager() {
    const videoModal = document.getElementById('videoModal');
    const openBtn = document.getElementById('openVideoModalBtn');
    const closeBtn = document.getElementById('closeVideoModalBtn');
    const dropzone = document.getElementById('videoDropzone');
    const fileInput = document.getElementById('videoFileInput');
    const progressWrap = document.getElementById('videoUploadProgressWrap');
    const progressBar = document.getElementById('videoProgressBar');
    const progressLabel = document.getElementById('videoProgressLabel');
    const progressPercent = document.getElementById('videoProgressPercent');
    const activeFramesCount = document.getElementById('activeFramesCount');
    const sourceVideoName = document.getElementById('sourceVideoName');
    const triggerBtn = document.getElementById('triggerExtractBtn');
    const urlInput = document.getElementById('videoUrlInput');
    const urlBtn = document.getElementById('extractUrlBtn');

    if (!videoModal) return;

    const openVideoModal = () => {
      videoModal.style.display = 'flex';
      refreshStatus();
    };

    const closeVideoModal = () => {
      videoModal.style.display = 'none';
    };

    if (openBtn) openBtn.addEventListener('click', openVideoModal);
    if (closeBtn) closeBtn.addEventListener('click', closeVideoModal);
    const heroQuickBtn = document.getElementById('heroQuickUploadBtn');
    if (heroQuickBtn) {
      heroQuickBtn.addEventListener('click', () => {
        if (fileInput) fileInput.click();
      });
    }
    videoModal.addEventListener('click', (e) => {
      if (e.target === videoModal) closeVideoModal();
    });

    const refreshStatus = async () => {
      try {
        const res = await fetch('/api/frames-status');
        if (res.ok) {
          const data = await res.json();
          if (activeFramesCount) {
            activeFramesCount.textContent = `${data.frameCount} Frames Extracted`;
          }
          if (sourceVideoName) {
            sourceVideoName.textContent = data.manifest?.video || (data.videoExists ? 'hf_20261016_142815_403ea31a-8a9a-43a4-a7ff-2aa022b64a3f.mp4' : 'Kerala Walkthrough Frames');
          }
        }
      } catch (e) {
        if (activeFramesCount) activeFramesCount.textContent = 'Active (150 Frames)';
      }
    };

    refreshStatus();

    const uploadFile = (file) => {
      if (!file) return;
      if (progressWrap) progressWrap.style.display = 'block';
      if (progressLabel) progressLabel.textContent = `Uploading ${file.name}...`;
      if (progressBar) progressBar.style.width = '0%';
      if (progressPercent) progressPercent.textContent = '0%';

      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/api/upload-video', true);
      xhr.setRequestHeader('x-filename', file.name);

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          const percent = Math.round((e.loaded / e.total) * 90);
          if (progressBar) progressBar.style.width = `${percent}%`;
          if (progressPercent) progressPercent.textContent = `${percent}%`;
          if (percent >= 90 && progressLabel) {
            progressLabel.textContent = 'Extracting frames with ffmpeg & updating landing page...';
          }
        }
      };

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          if (progressBar) progressBar.style.width = '100%';
          if (progressPercent) progressPercent.textContent = '100%';
          if (progressLabel) progressLabel.textContent = 'Frames extracted successfully!';
          setTimeout(() => {
            if (window.reloadWalkthroughFrames) {
              window.reloadWalkthroughFrames();
            }
            refreshStatus();
            setTimeout(closeVideoModal, 1200);
          }, 600);
        } else {
          try {
            const err = JSON.parse(xhr.responseText);
            if (progressLabel) progressLabel.textContent = `Error: ${err.error || 'Upload failed'}`;
          } catch (e) {
            if (progressLabel) progressLabel.textContent = 'Extraction failed. Check video format.';
          }
        }
      };

      xhr.onerror = () => {
        if (progressLabel) progressLabel.textContent = 'Network error during upload.';
      };

      xhr.send(file);
    };

    window.addEventListener('dragover', (e) => {
      e.preventDefault();
    });
    window.addEventListener('drop', (e) => {
      e.preventDefault();
      if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        if (file.name.endsWith('.mp4') || file.type.startsWith('video/')) {
          openVideoModal();
          uploadFile(file);
        }
      }
    });

    if (dropzone) {
      dropzone.addEventListener('click', () => fileInput && fileInput.click());
      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = '#F2A24B';
        dropzone.style.background = 'rgba(242, 162, 75, 0.08)';
      });
      dropzone.addEventListener('dragleave', () => {
        dropzone.style.borderColor = 'rgba(242, 162, 75, 0.4)';
        dropzone.style.background = 'rgba(242, 162, 75, 0.03)';
      });
      dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = 'rgba(242, 162, 75, 0.4)';
        dropzone.style.background = 'rgba(242, 162, 75, 0.03)';
        if (e.dataTransfer && e.dataTransfer.files.length > 0) {
          uploadFile(e.dataTransfer.files[0]);
        }
      });
    }

    if (fileInput) {
      fileInput.addEventListener('change', () => {
        if (fileInput.files && fileInput.files.length > 0) {
          uploadFile(fileInput.files[0]);
        }
      });
    }

    if (triggerBtn) {
      triggerBtn.addEventListener('click', async () => {
        triggerBtn.textContent = 'Extracting frames...';
        triggerBtn.disabled = true;
        try {
          const res = await fetch('/api/trigger-extract', { method: 'POST' });
          const data = await res.json();
          if (data.ok) {
            triggerBtn.textContent = 'Frames Extracted!';
            if (window.reloadWalkthroughFrames) window.reloadWalkthroughFrames();
            refreshStatus();
            setTimeout(() => {
              triggerBtn.textContent = 'Extract Frames from Current Project Video';
              triggerBtn.disabled = false;
              closeVideoModal();
            }, 1200);
          } else {
            triggerBtn.textContent = data.error || 'Failed to extract';
            setTimeout(() => {
              triggerBtn.textContent = 'Extract Frames from Current Project Video';
              triggerBtn.disabled = false;
            }, 3000);
          }
        } catch (err) {
          triggerBtn.textContent = 'Extraction trigger error';
          setTimeout(() => {
            triggerBtn.textContent = 'Extract Frames from Current Project Video';
            triggerBtn.disabled = false;
          }, 2500);
        }
      });
    }

    if (urlBtn && urlInput) {
      urlBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;
        urlBtn.textContent = 'Fetching...';
        urlBtn.disabled = true;
        try {
          const res = await fetch('/api/extract-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url }),
          });
          const data = await res.json();
          if (data.ok) {
            urlBtn.textContent = 'Done!';
            if (window.reloadWalkthroughFrames) window.reloadWalkthroughFrames();
            refreshStatus();
            setTimeout(closeVideoModal, 1200);
          } else {
            urlBtn.textContent = 'Failed';
            alert(data.error || 'Failed to fetch video');
          }
        } catch (err) {
          urlBtn.textContent = 'Error';
        } finally {
          setTimeout(() => {
            urlBtn.textContent = 'Fetch';
            urlBtn.disabled = false;
          }, 2000);
        }
      });
    }
  }
}
