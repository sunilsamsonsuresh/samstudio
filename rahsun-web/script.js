document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    const form = document.getElementById('enquiry-form');
    const galleryTabs = document.querySelectorAll('.gallery-tab');
    const galleryItems = document.querySelectorAll('.gallery-item');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeLightbox = document.querySelector('.close-lightbox');
    const prevLightbox = document.querySelector('.prev-lightbox');
    const nextLightbox = document.querySelector('.next-lightbox');

    let currentImageIndex = 0;
    let currentCategoryImages = [];

    // Gallery filtering
    galleryTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            galleryTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            tab.classList.add('active');
            
            const category = tab.dataset.category;
            
            galleryItems.forEach(item => {
                if (category === 'all' || item.dataset.category === category) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Lightbox functionality
    galleryItems.forEach((item, index) => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            const caption = item.querySelector('.gallery-caption');
            
            // Get all visible images in current category
            const activeTab = document.querySelector('.gallery-tab.active');
            const currentCategory = activeTab.dataset.category;
            currentCategoryImages = Array.from(galleryItems)
                .filter(item => {
                    if (currentCategory === 'all') return true;
                    return item.dataset.category === currentCategory;
                })
                .map(item => ({
                    src: item.querySelector('img').src,
                    caption: item.querySelector('.gallery-caption').textContent
                }));

            currentImageIndex = currentCategoryImages.findIndex(img => img.src === item.querySelector('img').src);
            
            openLightbox(img.src, caption.textContent);
        });
    });

    function openLightbox(src, caption) {
        lightbox.classList.add('active');
        lightboxImg.src = src;
        lightboxCaption.textContent = caption;
        document.body.style.overflow = 'hidden';
    }

    function closeLightboxHandler() {
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';
    }

    function showNextImage() {
        currentImageIndex = (currentImageIndex + 1) % currentCategoryImages.length;
        const nextImage = currentCategoryImages[currentImageIndex];
        lightboxImg.src = nextImage.src;
        lightboxCaption.textContent = nextImage.caption;
    }

    function showPrevImage() {
        currentImageIndex = (currentImageIndex - 1 + currentCategoryImages.length) % currentCategoryImages.length;
        const prevImage = currentCategoryImages[currentImageIndex];
        lightboxImg.src = prevImage.src;
        lightboxCaption.textContent = prevImage.caption;
    }

    closeLightbox.addEventListener('click', closeLightboxHandler);
    nextLightbox.addEventListener('click', showNextImage);
    prevLightbox.addEventListener('click', showPrevImage);

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (lightbox.classList.contains('active')) {
            if (e.key === 'Escape') {
                closeLightboxHandler();
            } else if (e.key === 'ArrowRight') {
                showNextImage();
            } else if (e.key === 'ArrowLeft') {
                showPrevImage();
            }
        }
    });

    // Close lightbox when clicking outside the image
    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightboxHandler();
        }
    });

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });

    // WhatsApp form submission
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const name = document.getElementById('name').value;
            const phone = document.getElementById('phone').value;
            const checkIn = document.getElementById('check-in').value;
            const checkOut = document.getElementById('check-out').value;
            const adults = document.getElementById('adults').value;
            const children = document.getElementById('children').value;

            // Format the message
            const message = `New Enquiry from Website:\nName: ${name}\nPhone: ${phone}\nCheck-in: ${checkIn}\nCheck-out: ${checkOut}\nAdults: ${adults}\nChildren: ${children}`;

            // Encode the message for URL
            const encodedMessage = encodeURIComponent(message);
            
            // Format WhatsApp number (always use 91 prefix for India)
            const baseNumber = window.config.contactPhone.replace(/\D/g, ''); // Remove any non-digits
            const whatsappNumber = '91' + baseNumber;
            
            // Create the WhatsApp URL
            const whatsappUrl = `https://api.whatsapp.com/send/?phone=${whatsappNumber}&text=${encodedMessage}&type=phone_number&app_absent=0`;
            
            // Open WhatsApp in a new tab
            window.open(whatsappUrl, '_blank');
            
            // Reset the form
            form.reset();
        });
    }

    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    });

    // Slideshow functionality
    const slides = document.querySelectorAll('.slide');
    const prevButton = document.querySelector('.prev-slide');
    const nextButton = document.querySelector('.next-slide');
    let currentSlide = 0;

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        slides[index].classList.add('active');
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    function prevSlide() {
        currentSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(currentSlide);
    }

    // Initialize first slide
    showSlide(currentSlide);

    // Add event listeners
    prevButton.addEventListener('click', prevSlide);
    nextButton.addEventListener('click', nextSlide);

    // Auto-advance slides every 5 seconds
    setInterval(nextSlide, 5000);

    const reviewSlides = document.querySelectorAll('.review-slide');
    const prevReviewBtn = document.querySelector('.prev-review');
    const nextReviewBtn = document.querySelector('.next-review');
    const reviewDots = document.querySelector('.review-dots');
    let currentReviewIndex = 0;
    let reviewInterval;

    function createDots() {
        reviewSlides.forEach((_, index) => {
            const dot = document.createElement('div');
            dot.classList.add('review-dot');
            if (index === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                currentReviewIndex = index;
                showReview(currentReviewIndex);
                resetInterval();
            });
            reviewDots.appendChild(dot);
        });
    }

    function updateDots() {
        const dots = document.querySelectorAll('.review-dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentReviewIndex);
        });
    }

    function showReview(index) {
        reviewSlides.forEach(slide => slide.classList.remove('active'));
        reviewSlides[index].classList.add('active');
        updateDots();
    }

    function nextReview() {
        currentReviewIndex = (currentReviewIndex + 1) % reviewSlides.length;
        showReview(currentReviewIndex);
    }

    function prevReview() {
        currentReviewIndex = (currentReviewIndex - 1 + reviewSlides.length) % reviewSlides.length;
        showReview(currentReviewIndex);
    }

    function startInterval() {
        reviewInterval = setInterval(nextReview, 3000);
    }

    function resetInterval() {
        clearInterval(reviewInterval);
        startInterval();
    }

    prevReviewBtn.addEventListener('click', () => {
        prevReview();
        resetInterval();
    });

    nextReviewBtn.addEventListener('click', () => {
        nextReview();
        resetInterval();
    });

    createDots();
    showReview(currentReviewIndex);
    startInterval();

    // Pause on hover
    const slideshow = document.querySelector('.reviews-slideshow');
    slideshow.addEventListener('mouseenter', () => {
        clearInterval(reviewInterval);
    });

    slideshow.addEventListener('mouseleave', () => {
        startInterval();
    });

    const seeMoreGalleryBtn = document.querySelector('.see-more-gallery-btn');

    seeMoreGalleryBtn.addEventListener('click', () => {
        galleryItems.forEach(item => {
            item.classList.remove('hidden');
        });
        seeMoreGalleryBtn.style.display = 'none';
    });
}); 