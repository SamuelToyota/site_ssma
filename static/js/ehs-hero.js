(() => {
    const hero = document.querySelector('[data-ehs-hero]');
    if (!hero) return;

    const art = hero.querySelector('[data-ehs-parallax]');
    const toggle = hero.querySelector('[data-ehs-motion]');
    const label = hero.querySelector('[data-ehs-motion-label]');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    let paused = false;
    let frame = 0;
    let offsetX = 0;
    let offsetY = 0;

    const resetParallax = () => {
        cancelAnimationFrame(frame);
        frame = 0;
        art.style.setProperty('--ehs-x', '0px');
        art.style.setProperty('--ehs-y', '0px');
    };

    const updateMotion = () => {
        hero.dataset.motion = paused || reducedMotion.matches ? 'paused' : 'playing';
        toggle.hidden = reducedMotion.matches;
        toggle.setAttribute('aria-pressed', String(paused));
        const text = paused ? 'Retomar animação' : 'Pausar animação';
        toggle.setAttribute('aria-label', text);
        label.textContent = text;
        if (paused || reducedMotion.matches) resetParallax();
    };

    toggle.addEventListener('click', () => {
        paused = !paused;
        updateMotion();
    });
    reducedMotion.addEventListener('change', updateMotion);
    finePointer.addEventListener('change', resetParallax);

    hero.addEventListener('pointermove', (event) => {
        if (paused || reducedMotion.matches || !finePointer.matches) return;
        const bounds = hero.getBoundingClientRect();
        offsetX = ((event.clientX - bounds.left) / bounds.width - .5) * 12;
        offsetY = ((event.clientY - bounds.top) / bounds.height - .5) * 10;
        if (frame) return;
        frame = requestAnimationFrame(() => {
            art.style.setProperty('--ehs-x', `${offsetX.toFixed(2)}px`);
            art.style.setProperty('--ehs-y', `${offsetY.toFixed(2)}px`);
            frame = 0;
        });
    }, { passive: true });
    hero.addEventListener('pointerleave', resetParallax);

    if ('IntersectionObserver' in window) {
        new IntersectionObserver(([entry]) => {
            hero.toggleAttribute('data-offscreen', !entry.isIntersecting);
            if (!entry.isIntersecting) resetParallax();
        }).observe(hero);
    }
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) hero.setAttribute('data-offscreen', '');
        else hero.toggleAttribute('data-offscreen', hero.getBoundingClientRect().bottom <= 0);
    });

    updateMotion();
})();
