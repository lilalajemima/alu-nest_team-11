// app.js
async function fetchNeighborhoods() {
    try {
        console.log('Fetching neighborhoods...');
        const response = await fetch('http://localhost:5000/api/neighborhoods');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Fetched neighborhoods:', data);
        return data;
    } catch (error) {
        console.error('Error fetching neighborhoods:', error);
        return [];
    }
}

function displayComparison(neighborhood1, neighborhood2) {
    console.log('Displaying comparison:', neighborhood1, neighborhood2);
    const comparisonSection = document.getElementById('comparison-section');
    
    if (!comparisonSection) {
        console.error('Comparison section element not found!');
        return;
    }

    comparisonSection.innerHTML = `
        <div class="comparison-container">
            <div class="neighborhood-card">
                <h2>${neighborhood1.name}</h2>
                <div class="details">
                    <p><strong>🚶 Walk:</strong> ${neighborhood1.commute.byFoot.time} (${neighborhood1.commute.byFoot.distance})</p>
                    <p><strong>🚴 Bike:</strong> ${neighborhood1.commute.byBike.time} (${neighborhood1.commute.byBike.distance})</p>
                    <p><strong>👮 Police Station:</strong> ${neighborhood1.safety.policeStation}</p>
                    <p><strong>🛒 Groceries:</strong> ${neighborhood1.groceryStores.description}</p>
                    <p><strong>💊 Pharmacies:</strong> ${neighborhood1.pharmacies.description}</p>
                    <p><strong>🏥 Health:</strong> ${neighborhood1.healthFacilities.description}</p>
                </div>
            </div>

            <div class="vs-divider">VS</div>

            <div class="neighborhood-card">
                <h2>${neighborhood2.name}</h2>
                <div class="details">
                    <p><strong>🚶 Walk:</strong> ${neighborhood2.commute.byFoot.time} (${neighborhood2.commute.byFoot.distance})</p>
                    <p><strong>🚴 Bike:</strong> ${neighborhood2.commute.byBike.time} (${neighborhood2.commute.byBike.distance})</p>
                    <p><strong>👮 Police Station:</strong> ${neighborhood2.safety.policeStation}</p>
                    <p><strong>🛒 Groceries:</strong> ${neighborhood2.groceryStores.description}</p>
                    <p><strong>💊 Pharmacies:</strong> ${neighborhood2.pharmacies.description}</p>
                    <p><strong>🏥 Health:</strong> ${neighborhood2.healthFacilities.description}</p>
                </div>
            </div>
        </div>
    `;
}

async function handleComparison(event) {
    event.preventDefault();
    console.log('Handling comparison...');
    
    const neighborhood1Id = document.getElementById('neighborhood1').value;
    const neighborhood2Id = document.getElementById('neighborhood2').value;

    if (!neighborhood1Id || !neighborhood2Id) {
        alert('Please select two neighborhoods to compare');
        return;
    }

    try {
        console.log(`Fetching comparison for ${neighborhood1Id} and ${neighborhood2Id}`);
        const response = await fetch(
            `http://localhost:5000/api/compare?id1=${neighborhood1Id}&id2=${neighborhood2Id}`
        );
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Comparison data:', data);
        
        if (!data.neighborhood1 || !data.neighborhood2) {
            throw new Error('Missing neighborhood data in response');
        }
        
        displayComparison(data.neighborhood1, data.neighborhood2);
    } catch (error) {
        console.error('Comparison error:', error);
        alert('Error fetching comparison data: ' + error.message);
    }
}

async function initializeSelectors() {
    try {
        console.log('Initializing selectors...');
        const neighborhoods = await fetchNeighborhoods();
        const selector1 = document.getElementById('neighborhood1');
        const selector2 = document.getElementById('neighborhood2');

        if (!selector1 || !selector2) {
            throw new Error('Neighborhood select elements not found!');
        }

        // Clear existing options
        selector1.innerHTML = '<option value="">Select Neighborhood</option>';
        selector2.innerHTML = '<option value="">Select Neighborhood</option>';

        neighborhoods.forEach(neighborhood => {
            const option = document.createElement('option');
            option.value = neighborhood._id;
            option.textContent = neighborhood.name;
            selector1.appendChild(option.cloneNode(true));
            selector2.appendChild(option);
        });
    } catch (error) {
        console.error('Initialization error:', error);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed');
    
    const compareForm = document.getElementById('compare-form');
    if (compareForm) {
        compareForm.addEventListener('submit', handleComparison);
    } else {
        console.error('Compare form not found!');
    }

    initializeSelectors();
});

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', function() {
        this.classList.toggle('active');
        navLinks.classList.toggle('active');
    });

    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.header')) {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        }
    });

    // Close menu when clicking a nav link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
});
