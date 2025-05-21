/**
    * @author  EliasDH Team
    * @see https://eliasdh.com
    * @since 01/01/2025
**/

document.addEventListener('DOMContentLoaded', function() {
    loadExternalContent("context-menu", "/assets/includes/context-menu.html");
    loadExternalContent("footer", "https://eliasdh.com/assets/includes/external-footer.html");
});

document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.getElementById('gallery-data');
    const imageFolder = '/assets/media/images/gallery/';
    const imageNames = [
        'mount-plaesant-before1.jpg',
        'mount-plaesant-before2.jpg',
        'mount-plaesant-before3.jpg',
        'mount-plaesant-before4.jpg',
        'mount-plaesant-before5.jpg',
        'mount-plaesant-before6.jpg',
        'office1.jpg',
        'office2.jpg',
        'office3.jpg',
        'the-radcliffe-centre1.jpg',
        'the-radcliffe-centre2.jpg',
        'the-radcliffe-centre3.jpg',
        'the-radcliffe-centre4.jpg',
        'mount-plaesant-after1.jpg',
        'UWC-2025-1.jpg',
        'UWC-2025-2.jpg',
        'UWC-2025-3.jpg',
        'UWC-2025-3.jpg',
        'UWC-2025-4.jpg',
        'UWC-2025-5.jpg',
        'UWC-2025-6.jpg',
        'UWC-2025-7.jpg',
        'UWC-2025-8.jpg',
        'UWC-2025-9.jpg',
        'UWC-2025-10.jpg',
        'UWC-2025-11.jpg',
        'UWC-2025-12.jpg',
        'UWC-2025-13.jpg',
        'UWC-2025-14.jpg'
    ];

    imageNames.forEach((imageName, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.classList.add('images-item');

        if (imageName === 'none') {
            gallery.appendChild(galleryItem);
            return;
        }

        const img = document.createElement('img');
        img.src = `${imageFolder}${imageName}`;
        img.alt = `Image ${index + 1} from internship`;

        img.onload = () => {
            galleryItem.style.width = `${img.naturalWidth}px`;
            galleryItem.style.maxWidth = '100%';
        };

        const caption = document.createElement('div');
        caption.classList.add('images-item-caption');
        caption.textContent = imageName.split('.')[0].replace(/_/g, ' ');

        galleryItem.appendChild(img);
        galleryItem.appendChild(caption);
        gallery.appendChild(galleryItem);
    });
});