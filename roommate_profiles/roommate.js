// Fetch profiles from the JSON file
async function fetchProfiles() {
    const response = await fetch('./profiles.json');
    const profiles = await response.json();
    return profiles;
  }
  
  function displayProfiles(profiles) {
    const profilesList = document.getElementById('profiles-list');
    profilesList.innerHTML = '';
  
    profiles.forEach(profile => {
      const profileCard = document.createElement('div');
      profileCard.className = 'profile-card';
  
      profileCard.innerHTML = `
        <img src="${profile.profileImage}" alt="Profile Image" class="profile-image">
        <h3>${profile.name}</h3>
        <p>${profile.degreeProgram}, ${profile.intake}</p>
        <p>Personality: ${profile.personalityTrait}</p>
        <p>Budget: ${profile.budgetRange.min} RWF - ${profile.budgetRange.max} RWF</p>
        <p>Looking for: ${profile.lookingFor} roommate</p>
        <p>${profile.description}</p>
        <a href="mailto:${profile.email}" class="contact-button">Contact Me</a>
      `;
  
      profilesList.appendChild(profileCard);
    });
  
    // Add click event to profile images
    const images = document.querySelectorAll('.profile-image');
    images.forEach(image => {
      image.addEventListener('click', () => {
        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-image');
        modal.style.display = 'block';
        modalImg.src = image.src;
      });
    });
  }

 // Close modal when clicking the X button
const closeButton = document.querySelector('.close');
closeButton.addEventListener('click', () => {
  const modal = document.getElementById('image-modal');
  modal.style.display = 'none';
});

// Close modal when clicking outside the image
window.addEventListener('click', (event) => {
  const modal = document.getElementById('image-modal');
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});

  // Filter profiles based on search criteria
  function filterProfiles(profiles, filters) {
    return profiles.filter(profile => {
      // Gender filter
      if (filters.gender && profile.lookingFor !== filters.gender) {
        return false;
      }
  
      // Budget filter
      if (filters.minBudget && profile.budgetRange.max < filters.minBudget) {
        return false;
      }
      if (filters.maxBudget && profile.budgetRange.min > filters.maxBudget) {
        return false;
      }
  
      // Personality filter
      if (filters.personality && profile.personalityTrait !== filters.personality) {
        return false;
      }
  
      return true;
    });
  }
  
  // Handle search form submission
  async function handleSearch(event) {
    event.preventDefault();
  
    const gender = document.getElementById('gender').value;
    const minBudget = parseInt(document.getElementById('min-budget').value);
    const maxBudget = parseInt(document.getElementById('max-budget').value);
    const personality = document.getElementById('personality').value;
  
    const filters = {
      gender,
      minBudget,
      maxBudget,
      personality,
    };
  
    const profiles = await fetchProfiles();
    const filteredProfiles = filterProfiles(profiles, filters);
    displayProfiles(filteredProfiles);
  }
  
  // Add event listener to the search form
  document.getElementById('search-form').addEventListener('submit', handleSearch);
  
  // Fetch and display profiles when the page loads
  window.onload = async () => {
    const profiles = await fetchProfiles();
    displayProfiles(profiles);
  };
