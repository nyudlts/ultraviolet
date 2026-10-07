import '@google/model-viewer';

const viewer = document.querySelector('#gltf-viewer');
const progress = document.querySelector('#gltf-progress');

viewer.addEventListener('progress', (event) => {
    const percent = event.detail.totalProgress * 100;
    progress.style.width = `${percent}%`;
});

viewer.addEventListener('load', () => {
    progress.style.width = '100%';
    setTimeout(() => {
        progress.parentElement.style.display = 'none';
    }, 300);
});

viewer.addEventListener('error', () => {
    progress.parentElement.style.display = 'none';
});
