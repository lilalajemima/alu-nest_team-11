
document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const phone = document.getElementById('phone').value;
 
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ fullName, email, password, phone }),
    });
  
    const data = await response.json();
    document.getElementById('registerMessage').textContent = data.message;

    if (response.ok) {
      document.getElementById('registerForm').reset();
    }
  });

  document.getElementById('searchRoommateProfilesForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const budget = document.getElementById('searchBudget').value;
    const lifestylePreferences = document.getElementById('searchLifestylePreferences').value;
    const studyHabits = document.getElementById('searchStudyHabits').value;
    const interests = document.getElementById('searchInterests').value;

    const params = new URLSearchParams();
    if (budget) params.append('budget', budget);
    if (lifestylePreferences) params.append('lifestyle_preferences', lifestylePreferences);
    if (studyHabits) params.append('study_habits', studyHabits);
    if (interests) params.append('interests', interests);

    const response = await fetch(`/roommate-profiles?${params.toString()}`);
    const profiles = await response.json();
  
    const profilesList = document.getElementById('profilesList');
    profilesList.innerHTML = profiles.map(profile => `
      <div class="profile-card">
        <h3>${profile.full_name}</h3>
        <p><strong>Budget:</strong> $${profile.roommate_profile.budget}</p>
        <p><strong>Lifestyle:</strong> ${profile.roommate_profile.lifestyle_preferences.join(', ')}</p>
        <p><strong>Study Habits:</strong> ${profile.roommate_profile.study_habits}</p>
        <p><strong>Interests:</strong> ${profile.roommate_profile.interests.join(', ')}</p>
        <p><strong>Bio:</strong> ${profile.roommate_profile.bio}</p>
      </div>
    `).join('');
  });