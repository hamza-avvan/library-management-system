/**
 * Hash-synchronized profile tabs.
 * Config: { root, buttons, panelForTab, validTabs }
 * Methods: init()
 * Events: No custom events are dispatched.
 */
(function () {
  const instances = new WeakMap();

  window.ProfileTabs = function (config) {
    if (!config || !(config.root instanceof Element)) {
      throw new TypeError('ProfileTabs requires a root element.');
    }
    const existing = instances.get(config.root);
    if (existing) return existing;

    if (!config.buttons || typeof config.buttons[Symbol.iterator] !== 'function') {
      throw new TypeError('ProfileTabs requires an iterable buttons collection.');
    }
    if (!Array.isArray(config.validTabs) || config.validTabs.length === 0) {
      throw new TypeError('ProfileTabs requires a non-empty validTabs array.');
    }
    if (!config.panelForTab || typeof config.panelForTab !== 'object') {
      throw new TypeError('ProfileTabs requires a panelForTab mapping.');
    }

    const root = config.root;
    const buttons = Array.from(config.buttons);
    const validTabs = config.validTabs.slice();
    const panelForTab = config.panelForTab;
    if (buttons.length === 0) {
      throw new TypeError('ProfileTabs requires at least one tab button.');
    }

    buttons.forEach(function (button) {
      if (!(button instanceof HTMLElement) || !root.contains(button)) {
        throw new TypeError('ProfileTabs buttons must be elements inside root.');
      }
      if (!validTabs.includes(button.dataset.tab)) {
        throw new TypeError('ProfileTabs button has an unconfigured tab name.');
      }
    });
    validTabs.forEach(function (name) {
      if (!Object.prototype.hasOwnProperty.call(panelForTab, name)
          || !(panelForTab[name] instanceof HTMLElement)
          || !root.contains(panelForTab[name])) {
        throw new TypeError('ProfileTabs requires a panel inside root for tab "' + name + '".');
      }
    });

    let initialized = false;

    function activateTab(name) {
      buttons.forEach(function (button) {
        const active = button.dataset.tab === name;
        button.classList.toggle('active', active);
        button.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      validTabs.forEach(function (tabName) {
        panelForTab[tabName].classList.toggle('active', tabName === name);
      });

      if (history.replaceState) {
        history.replaceState(null, '', '#' + name);
      } else {
        location.hash = name;
      }
    }

    const api = {
      init: function () {
        if (initialized) return api;
        buttons.forEach(function (button) {
          button.addEventListener('click', function () {
            activateTab(button.dataset.tab);
          });
        });
        const initial = (location.hash || '').replace('#', '');
        if (validTabs.includes(initial)) activateTab(initial);
        initialized = true;
        return api;
      }
    };

    instances.set(root, api);
    return api;
  };
})();
