(() => {
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach((form) => {
    form.addEventListener(
      'submit',
      (event) => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      },
      false
    );
  });

  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2 }
    );

    revealEls.forEach((el) => observer.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in-view'));
  }

  const typingEls = document.querySelectorAll('[data-typing-lines], [data-typing]');
  typingEls.forEach((typingEl) => {
    const linesAttr = typingEl.dataset.typingLines;
    const singleLine = typingEl.dataset.typing || typingEl.textContent || '';
    const lines = linesAttr ? linesAttr.split('|') : [singleLine];
    const speed = Number(typingEl.dataset.typingSpeed || 28);
    const pause = Number(typingEl.dataset.typingPause || 1200);
    let lineIndex = 0;
    let charIndex = 0;

    const typeLine = () => {
      const currentLine = lines[lineIndex] || '';
      typingEl.textContent = currentLine.slice(0, charIndex);
      charIndex += 1;

      if (charIndex <= currentLine.length) {
        window.setTimeout(typeLine, speed);
        return;
      }

      window.setTimeout(() => {
        lineIndex = (lineIndex + 1) % lines.length;
        charIndex = 0;
        typeLine();
      }, pause);
    };

    typeLine();
  });

  const toggle = document.querySelector('[data-theme-toggle]');
  if (toggle) {
    const root = document.documentElement;
    const stored = localStorage.getItem('theme');
    if (stored) {
      root.setAttribute('data-theme', stored);
    }
    toggle.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
    });
  }
})();
