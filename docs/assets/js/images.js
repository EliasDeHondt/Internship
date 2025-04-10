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
        'mount-plaesant-before7.jpg'
    ];

    imageNames.forEach((imageName, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.classList.add('images-item');

        const img = document.createElement('img');
        img.src = `${imageFolder}${imageName}`;
        img.alt = `Image ${index + 1} from internship`;

        const caption = document.createElement('div');
        caption.classList.add('images-item-caption');
        caption.textContent = imageName.split('.')[0].replace(/_/g, ' ');

        galleryItem.appendChild(img);
        galleryItem.appendChild(caption);
        gallery.appendChild(galleryItem);
    });
});