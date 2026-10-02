/**
 * Book image uploader for add/edit forms.
 * Config: { dropzone, fileInput, previewGrid, counter, frontImageInput,
 *   hiddenFileInputs, form, seeded, removedInput, maxImages, maxSizeMB, name }
 * Methods: init()
 * Events: No custom events are dispatched.
 */
(function () {
  const instances = new WeakMap();

  window.ImageUploader = function (config) {
    if (!config || !(config.dropzone instanceof HTMLElement)) {
      throw new TypeError('ImageUploader requires a dropzone element.');
    }

    const existing = instances.get(config.dropzone);
    if (existing) return existing;

    function requireElement(value, type, name) {
      if (!(value instanceof type)) {
        throw new TypeError('ImageUploader requires ' + name + ' to be a valid element.');
      }
      return value;
    }

    const dropzone = requireElement(config.dropzone, HTMLElement, 'dropzone');
    const fileInput = requireElement(config.fileInput, HTMLInputElement, 'fileInput');
    const previewGrid = requireElement(config.previewGrid, HTMLElement, 'previewGrid');
    const imgCounter = requireElement(config.counter, HTMLElement, 'counter');
    const frontImageInput = requireElement(config.frontImageInput, HTMLInputElement, 'frontImageInput');
    const hiddenFileInputs = requireElement(config.hiddenFileInputs, HTMLElement, 'hiddenFileInputs');
    const form = requireElement(config.form, HTMLFormElement, 'form');
    const removedInput = config.removedInput == null
      ? null
      : requireElement(config.removedInput, HTMLInputElement, 'removedInput');
    const maxImages = config.maxImages === undefined ? 5 : config.maxImages;
    const maxSizeMB = config.maxSizeMB === undefined ? 5 : config.maxSizeMB;
    const inputName = config.name === undefined ? 'images' : config.name;
    const seeded = config.seeded === undefined ? [] : config.seeded;

    if (!Number.isInteger(maxImages) || maxImages < 1) {
      throw new RangeError('ImageUploader maxImages must be a positive integer.');
    }
    if (!Number.isFinite(maxSizeMB) || maxSizeMB <= 0) {
      throw new RangeError('ImageUploader maxSizeMB must be a positive number.');
    }
    if (typeof inputName !== 'string' || inputName.length === 0) {
      throw new TypeError('ImageUploader name must be a non-empty string.');
    }
    if (!Array.isArray(seeded)) {
      throw new TypeError('ImageUploader seeded must be an array.');
    }
    if (seeded.length > 0 && !removedInput) {
      throw new TypeError('ImageUploader requires removedInput when seeded images are provided.');
    }

    const items = seeded.map(function (item) {
      if (!item || item.type !== 'existing' || item.id == null || typeof item.url !== 'string') {
        throw new TypeError('ImageUploader seeded entries must contain an existing image id and URL.');
      }
      return {
        type: 'existing',
        id: String(item.id),
        url: item.url,
        front: Boolean(item.front)
      };
    });
    let initialized = false;

    function render() {
      previewGrid.innerHTML = '';

      items.forEach(function (item, index) {
        const card = document.createElement('div');
        card.className = 'preview-item' + (item.front ? ' is-front' : '');

        const img = document.createElement('img');
        img.src = item.url;
        img.alt = 'Book image ' + (index + 1);
        card.appendChild(img);

        if (item.front) {
          const tag = document.createElement('span');
          tag.className = 'front-tag';
          tag.innerHTML = '<i class="bi bi-star-fill"></i> Front';
          card.appendChild(tag);
        }

        const overlay = document.createElement('div');
        overlay.className = 'overlay';
        if (!item.front) {
          const setFrontBtn = document.createElement('button');
          setFrontBtn.type = 'button';
          setFrontBtn.className = 'btn-set-front';
          setFrontBtn.innerHTML = '<i class="bi bi-star"></i> Set as Front';
          setFrontBtn.addEventListener('click', function () { setFront(index); });
          overlay.appendChild(setFrontBtn);
        }

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn-remove';
        removeBtn.innerHTML = '<i class="bi bi-trash3"></i> Remove';
        removeBtn.addEventListener('click', function () { remove(index); });
        overlay.appendChild(removeBtn);
        card.appendChild(overlay);
        previewGrid.appendChild(card);
      });

      imgCounter.textContent = items.length + ' / ' + maxImages;
      imgCounter.classList.toggle('full', items.length >= maxImages);
      dropzone.classList.toggle('disabled', items.length >= maxImages);

      const front = items.find(function (item) { return item.front; });
      if (front) {
        frontImageInput.value = front.type === 'existing'
          ? 'existing:' + front.id
          : 'new:' + items.indexOf(front);
      } else {
        frontImageInput.value = '';
      }
    }

    function setFront(index) {
      items.forEach(function (item, itemIndex) {
        item.front = itemIndex === index;
      });
      render();
    }

    function remove(index) {
      const [removed] = items.splice(index, 1);
      if (removed.type === 'existing') {
        const current = removedInput.value ? removedInput.value.split(',') : [];
        current.push(removed.id);
        removedInput.value = current.join(',');
      }
      if (removed.front && items.length > 0) items[0].front = true;
      render();
    }

    function addFiles(fileList) {
      for (const file of Array.from(fileList)) {
        if (items.length >= maxImages) {
          alert('You can upload a maximum of ' + maxImages + ' images.');
          break;
        }
        if (!file.type.startsWith('image/')) {
          alert(file.name + ' is not an image.');
          continue;
        }
        if (file.size > maxSizeMB * 1024 * 1024) {
          alert(file.name + ' is larger than ' + maxSizeMB + ' MB.');
          continue;
        }
        items.push({
          type: 'new',
          file: file,
          url: URL.createObjectURL(file),
          front: items.length === 0
        });
      }
      render();
    }

    const api = {
      init: function () {
        if (initialized) return api;

        dropzone.addEventListener('click', function () {
          if (!dropzone.classList.contains('disabled')) fileInput.click();
        });
        dropzone.addEventListener('keydown', function (event) {
          if ((event.key === 'Enter' || event.key === ' ') && !dropzone.classList.contains('disabled')) {
            event.preventDefault();
            fileInput.click();
          }
        });
        fileInput.addEventListener('change', function (event) {
          addFiles(event.target.files);
          fileInput.value = '';
        });
        ['dragenter', 'dragover'].forEach(function (eventName) {
          dropzone.addEventListener(eventName, function (event) {
            event.preventDefault();
            event.stopPropagation();
            if (!dropzone.classList.contains('disabled')) dropzone.classList.add('dragover');
          });
        });
        ['dragleave', 'drop'].forEach(function (eventName) {
          dropzone.addEventListener(eventName, function (event) {
            event.preventDefault();
            event.stopPropagation();
            dropzone.classList.remove('dragover');
          });
        });
        dropzone.addEventListener('drop', function (event) {
          if (dropzone.classList.contains('disabled')) return;
          if (event.dataTransfer && event.dataTransfer.files) addFiles(event.dataTransfer.files);
        });
        window.addEventListener('dragover', function (event) { event.preventDefault(); });
        window.addEventListener('drop', function (event) { event.preventDefault(); });

        form.addEventListener('submit', function () {
          hiddenFileInputs.innerHTML = '';
          items.forEach(function (item) {
            if (item.type === 'new' && item.file) {
              const input = document.createElement('input');
              input.type = 'file';
              input.name = inputName;
              input.style.display = 'none';
              const dataTransfer = new DataTransfer();
              dataTransfer.items.add(item.file);
              input.files = dataTransfer.files;
              hiddenFileInputs.appendChild(input);
            }
          });
        });

        initialized = true;
        render();
        return api;
      }
    };

    instances.set(dropzone, api);
    return api;
  };
})();
