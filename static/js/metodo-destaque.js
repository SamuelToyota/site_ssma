// Without JavaScript, the same eight dimensions remain available as an accordion.
document.querySelectorAll('[data-destaque]').forEach((workbench) => {
    const navigation = workbench.querySelector('[data-destaque-navigation]');
    const buttons = [...navigation.querySelectorAll('button[aria-controls]')];
    const panels = buttons.map((button) => document.getElementById(button.getAttribute('aria-controls')));
    if (!buttons.length || panels.some((panel) => !panel)) return;

    function select(index) {
        buttons.forEach((button, position) => {
            const selected = position === index;
            button.setAttribute('aria-pressed', String(selected));
            panels[position].hidden = !selected;
            panels[position].open = selected;
        });
    }

    buttons.forEach((button, index) => {
        button.addEventListener('click', () => select(index));
        button.addEventListener('keydown', (event) => {
            let next;
            if (event.key === 'ArrowRight') next = (index + 1) % buttons.length;
            else if (event.key === 'ArrowLeft') next = (index - 1 + buttons.length) % buttons.length;
            else if (event.key === 'Home') next = 0;
            else if (event.key === 'End') next = buttons.length - 1;
            else return;

            event.preventDefault();
            select(next);
            buttons[next].focus();
        });
    });

    select(0);
    workbench.classList.add('destaque-enhanced');
    navigation.hidden = false;
});
