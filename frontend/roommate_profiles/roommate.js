
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


const closeButton = document.querySelector('.close');
closeButton.addEventListener('click', () => {
  const modal = document.getElementById('image-modal');
  modal.style.display = 'none';
});


window.addEventListener('click', (event) => {
  const modal = document.getElementById('image-modal');
  if (event.target === modal) {
    modal.style.display = 'none';
  }
});


  function filterProfiles(profiles, filters) {
    return profiles.filter(profile => {
  
      if (filters.gender && profile.lookingFor !== filters.gender) {
        return false;
      }
  

      if (filters.minBudget && profile.budgetRange.max < filters.minBudget) {
        return false;
      }
      if (filters.maxBudget && profile.budgetRange.min > filters.maxBudget) {
        return false;
      }
  

      if (filters.personality && profile.personalityTrait !== filters.personality) {
        return false;
      }
  
      return true;
    });
  }
  

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
  

  document.getElementById('search-form').addEventListener('submit', handleSearch);
  

  window.onload = async () => {
    const profiles = await fetchProfiles();
    displayProfiles(profiles);
  };
