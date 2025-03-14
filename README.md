# alu-nest_team-11



    <script>
        // Sample database of properties
    const propertiesData = [
    {
        id: "1",
        houseImg: {
            Outdoor: [
                "home/House 1/OutdoorView.jpg",
                "home/House 1/OutdoorView1.jpg"
            ],
            LivingRoom: [
                "home/House 1/LivingRoom.jpg"
            ],
            Kitchen: [
                "home/House 1/Kitchen.jpg"
            ],
            Bedroom: [
                "home/House 1/Bedroom1.jpg"
            ],
            Bathroom: [
                "home/House 1/Bathroom1.jpg"
            ]
        },
        house_overview: {
            house_name: '5-Bedroom House For Rent In Kanombe',
            house_price: 180000,
            status: 'Available',
            bedrooms: 5,
            bathrooms: 4,
            distance: 20,
            property_type: 'House',
            advert_type: "Partnered",
        }
    },
    {
        id: "2",
        houseImg: {
            Outdoor: [
                "home/House 2/OutdoorView.jpg",
                "home/House 2/OutdoorView1.jpg"
            ],
            LivingRoom: [
                "home/House 2/LivingRoom.jpg"
            ],
            Kitchen: [
                "home/House 2/Kitchen.jpg"
            ],
            Bedroom: [
                "home/House 2/Bedroom1.jpg"
            ],
            Bathroom: [
                "home/House 2/Bathroom1.jpg"
            ]
        },
        house_overview: {
            house_name: '3-Bedroom Apartment Near University',
            house_price: 120000,
            status: 'Available',
            bedrooms: 3,
            bathrooms: 2,
            distance: 5,
            property_type: 'Apartment',
            advert_type: "Standard",
        }
    },
    {
        id: "3",
        houseImg: {
            Outdoor: [
                "home/House 3/OutdoorView.jpg",
                "home/House 3/OutdoorView1.jpg"
            ],
            LivingRoom: [
                "home/House 3/LivingRoom.jpg"
            ],
            Kitchen: [
                "home/House 3/Kitchen.jpg"
            ],
            Bedroom: [
                "home/House 3/Bedroom1.jpg"
            ],
            Bathroom: [
                "home/House 3/Bathroom1.jpg"
            ]
        },
        house_overview: {
            house_name: 'Studio Apartment in University District',
            house_price: 85000,
            status: 'Reserved',
            bedrooms: 1,
            bathrooms: 1,
            distance: 2,
            property_type: 'Studio',
            advert_type: "Featured",
        }
    }
];
    
        function renderPropertyCards() {
            const listingsContainer = document.getElementById('listingsContainer');
    
            propertiesData.forEach(property => {
                const propertyCard = document.createElement('div');
                propertyCard.className = 'property-card';
    
                const images = property.houseImg.Outdoor;
    
                let carouselHTML = `
                    <div class="image-carousel">
                        <div class="carousel-images" data-property-id="${property.id}">
                `;
    
                images.forEach((img, index) => {
                    carouselHTML += `<img src="${img}" alt="Property Image ${index + 1}" class="carousel-image" onerror="this.onerror=null; this.src='/fallback.jpg'">`;
                });
    
                carouselHTML += `</div>
                    <div class="carousel-controls">
                        <button class="carousel-control prev" onclick="prevImage('${property.id}')">
                            <i class="fas fa-chevron-left"></i>
                        </button>
                        <button class="carousel-control next" onclick="nextImage('${property.id}')">
                            <i class="fas fa-chevron-right"></i>
                        </button>
                    </div>
                    <div class="carousel-dots" id="dots-${property.id}">
                `;
    
                images.forEach((_, index) => {
                    carouselHTML += `<span class="carousel-dot ${index === 0 ? 'active' : ''}" onclick="goToImage('${property.id}', ${index})"></span>`;
                });
    
                carouselHTML += `</div></div>`;
    
                const statusClass = property.house_overview.status === 'Available' ? 'available' : '';
                carouselHTML += `<div class="property-status ${statusClass}">${property.house_overview.status}</div>`;
    
                if (property.house_overview.advert_type !== 'Standard') {
                    carouselHTML += `<div class="advert-badge">${property.house_overview.advert_type}</div>`;
                }
    
                const propertyInfoHTML = `
                    <div class="property-info">
                        <h3 class="property-title">${property.house_overview.house_name}</h3>
                        <div class="price-tag">$${property.house_overview.house_price.toLocaleString()}/month</div>
                        <div class="property-details">
                            <div class="detail-item"><i class="fas fa-bed"></i> ${property.house_overview.bedrooms} Bed</div>
                            <div class="detail-item"><i class="fas fa-bath"></i> ${property.house_overview.bathrooms} Bath</div>
                            <div class="detail-item"><i class="fas fa-map-marker-alt"></i> ${property.house_overview.distance}km</div>
                            <div class="detail-item"><i class="fas fa-home"></i> ${property.house_overview.property_type}</div>
                        </div>
                    </div>
                `;
    
                propertyCard.innerHTML = carouselHTML + propertyInfoHTML;
                listingsContainer.appendChild(propertyCard);
            });
        }
    
        let currentImageIndices = {};
    
        function initializeCarousel() {
            propertiesData.forEach(property => {
                currentImageIndices[property.id] = 0;
            });
        }
    
        function updateCarousel(propertyId) {
            const carousel = document.querySelector(`.carousel-images[data-property-id="${propertyId}"]`);
            const imageCount = propertiesData.find(p => p.id === propertyId).houseImg.Outdoor.length;
            const currentIndex = currentImageIndices[propertyId];
    
            carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    
            const dots = document.querySelectorAll(`#dots-${propertyId} .carousel-dot`);
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentIndex);
            });
        }
    
        function nextImage(propertyId) {
            const imageCount = propertiesData.find(p => p.id === propertyId).houseImg.Outdoor.length;
            currentImageIndices[propertyId] = (currentImageIndices[propertyId] + 1) % imageCount;
            updateCarousel(propertyId);
        }
    
        function prevImage(propertyId) {
            const imageCount = propertiesData.find(p => p.id === propertyId).houseImg.Outdoor.length;
            currentImageIndices[propertyId] = (currentImageIndices[propertyId] - 1 + imageCount) % imageCount;
            updateCarousel(propertyId);
        }
    
        function goToImage(propertyId, index) {
            currentImageIndices[propertyId] = index;
            updateCarousel(propertyId);
        }
    
        window.onload = function() {
            renderPropertyCards();
            initializeCarousel();
        };
    </script>