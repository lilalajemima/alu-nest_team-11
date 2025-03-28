
document.getElementById('housingSearchForm').addEventListener('submit', function (e) {
    e.preventDefault();
  
    
    const minRent = parseInt(document.getElementById('minRent').value) || 0;
    const maxRent = parseInt(document.getElementById('maxRent').value) || Infinity;
    const bedrooms = document.getElementById('bedrooms').value;
    const location = document.getElementById('location').value;
    const amenities = Array.from(document.querySelectorAll('.amenities-checkboxes input:checked')).map((cb) => cb.name);
  
    // Filter listings
    const listings = document.querySelectorAll('.listing');
    listings.forEach((listing) => {
      const rent = parseInt(listing.getAttribute('data-rent'));
      const listingBedrooms = listing.getAttribute('data-bedrooms');
      const listingLocation = listing.getAttribute('data-location');
      const listingAmenities = amenities.every((amenity) => listing.getAttribute(`data-${amenity}`) === 'true');
  
      const matchesRent = rent >= minRent && rent <= maxRent;
      const matchesBedrooms = bedrooms === 'any' || listingBedrooms === bedrooms;
      const matchesLocation = location === 'any' || listingLocation === location;
      const matchesAmenities = amenities.length === 0 || listingAmenities;
  
      if (matchesRent && matchesBedrooms && matchesLocation && matchesAmenities) {
        listing.style.display = 'block';
      } else {
        listing.style.display = 'none';
      }
    });
  });
  
  
  const carousels = document.querySelectorAll('.image-carousel');
  
  carousels.forEach(carousel => {
    const images = carousel.querySelector('.carousel-images');
    const prevBtn = carousel.querySelector('.carousel-control.prev');
    const nextBtn = carousel.querySelector('.carousel-control.next');
    let currentIndex = 0;
  
    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + images.children.length) % images.children.length;
      images.style.transform = `translateX(-${currentIndex * 100}%)`;
    });
  
    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % images.children.length;
      images.style.transform = `translateX(-${currentIndex * 100}%)`;
    });
  });
  
  
  const modal = document.getElementById('listingModal');
  const closeModal = document.querySelector('.close-modal');
  const modalImage = document.getElementById('modalImage');
  
  
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('carousel-image')) {
      modalImage.src = e.target.src;
      modal.style.display = 'flex';
    }
  });
  

  closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
  });
  

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
  
  
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('contact-btn')) {
      const email = e.target.getAttribute('data-email');
      const whatsapp = e.target.getAttribute('data-whatsapp');
  
      if (email) {
        
        window.location.href = `mailto:${email}`;
      } else if (whatsapp) {
        
        const message = "Hello, I am interested in your house listing. Can i have  more details?";
        window.open(`https://wa.me/${whatsapp}?text=${encodeURIComponent(message)}`, '_blank');
      } else {
        alert('No contact information available.');
      }
    }
  });