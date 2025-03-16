// The Fetch Feature 
async function fetchProfiles() {
  const response = await fetch('http://localhost:5000/profiles'); 
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


async function handleSearch(event) {
  event.preventDefault();

  
  const gender = document.getElementById('gender').value;
  const minBudget = document.getElementById('min-budget').value;
  const maxBudget = document.getElementById('max-budget').value;
  const personality = document.getElementById('personality').value;

  
  const params = new URLSearchParams();
  if (gender) params.append('gender', gender);
  if (minBudget) params.append('minBudget', minBudget);
  if (maxBudget) params.append('maxBudget', maxBudget);
  if (personality) params.append('personality', personality);

  
  const response = await fetch(`http://localhost:5000/profiles/filter?${params.toString()}`);
  const filteredProfiles = await response.json();

  
  displayProfiles(filteredProfiles);
}

document.getElementById('search-form').addEventListener('submit', handleSearch);

window.onload = async () => {
  const profiles = await fetchProfiles(); 
  displayProfiles(profiles); 
};