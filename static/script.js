// Javascript for base.html
document.addEventListener('DOMContentLoaded', function() {
    // Login Form Handling - NEW CODE ADDED HERE
    
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Logging in...';
                submitBtn.classList.add('loading');
            }

            try {
                const response = await fetch('/user/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include', // Important for session cookies
                    body: JSON.stringify({
                        email: this.elements['email'].value,
                        password: this.elements['password'].value
                    })
                });

                const data = await response.json();
                
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Login';
                    submitBtn.classList.remove('loading');
                }

                if (response.ok && data.redirect) {
                    // Successful login - redirect
                    window.location.href = data.redirect;
                } else {
                    // Show error message
                    alert(data.error || 'Login failed. Please try again.');
                }
            } catch (error) {
                console.error('Login error:', error);
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Login';
                    submitBtn.classList.remove('loading');
                }
                alert('An error occurred during login');
            }
        });
    }


document.addEventListener('DOMContentLoaded', function() {
    // Profile Form Handling
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            // Validate budget range
            const budgetMin = parseInt(this.elements['budget_min'].value);
            const budgetMax = parseInt(this.elements['budget_max'].value);
            
            if (budgetMin > budgetMax) {
                e.preventDefault();
                alert('Maximum budget must be greater than minimum budget');
                return;
            }

            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Saving...';
                submitBtn.classList.add('loading');
            }
        });

        // Profile picture preview
        const profilePicInput = profileForm.querySelector('input[name="profile_pic"]');
        if (profilePicInput) {
            profilePicInput.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    const previewContainer = document.createElement('div');
                    previewContainer.className = 'image-preview';
                    
                    const img = document.createElement('img');
                    img.src = URL.createObjectURL(e.target.files[0]);
                    img.style.maxWidth = '150px';
                    img.style.maxHeight = '150px';
                    img.style.marginTop = '10px';
                    
                    previewContainer.appendChild(img);
                    
                    // Remove any existing preview
                    const existingPreview = profileForm.querySelector('.image-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    profilePicInput.after(previewContainer);
                }
            });
        }
    }

    // Listing Form Handling
    const listingForm = document.getElementById('listingForm');
    if (listingForm) {
        listingForm.addEventListener('submit', function(e) {
            // Basic validation
            if (parseInt(this.elements['num_bedrooms'].value) < 1 || 
                parseInt(this.elements['num_bathrooms'].value) < 1) {
                e.preventDefault();
                alert('Number of bedrooms and bathrooms must be at least 1');
                return;
            }

            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Creating...';
                submitBtn.classList.add('loading');
            }
        });

        // Image Preview for Listings
        const fileInput = listingForm.querySelector('input[name="listing_images"]');
        if (fileInput) {
            fileInput.addEventListener('change', function(e) {
                const files = e.target.files;
                const previewContainer = document.createElement('div');
                previewContainer.className = 'multi-image-preview';
                previewContainer.style.display = 'flex';
                previewContainer.style.flexWrap = 'wrap';
                previewContainer.style.gap = '10px';
                previewContainer.style.marginTop = '10px';

                // Remove any existing preview
                const existingPreview = listingForm.querySelector('.multi-image-preview');
                if (existingPreview) {
                    existingPreview.remove();
                }

                if (files.length > 0) {
                    for (let i = 0; i < Math.min(files.length, 4); i++) {
                        const imgContainer = document.createElement('div');
                        imgContainer.style.position = 'relative';
                        
                        const img = document.createElement('img');
                        img.src = URL.createObjectURL(files[i]);
                        img.style.maxWidth = '100px';
                        img.style.maxHeight = '100px';
                        img.style.objectFit = 'cover';
                        
                        const badge = document.createElement('span');
                        badge.textContent = files.length > 4 && i === 3 ? `+${files.length - 3}` : '';
                        badge.style.position = 'absolute';
                        badge.style.top = '5px';
                        badge.style.right = '5px';
                        badge.style.background = 'rgba(0,0,0,0.7)';
                        badge.style.color = 'white';
                        badge.style.borderRadius = '50%';
                        badge.style.width = '20px';
                        badge.style.height = '20px';
                        badge.style.display = 'flex';
                        badge.style.alignItems = 'center';
                        badge.style.justifyContent = 'center';
                        badge.style.fontSize = '12px';
                        
                        imgContainer.appendChild(img);
                        imgContainer.appendChild(badge);
                        previewContainer.appendChild(imgContainer);
                    }
                    
                    fileInput.after(previewContainer);
                }
            });
        }
    }

    // Delete Listing Confirmation
    const deleteForms = document.querySelectorAll('form[action*="/delete_listing/"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this listing? This action cannot be undone.')) {
                e.preventDefault();
            } else {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.textContent = 'Deleting...';
                    submitBtn.classList.add('loading');
                }
            }
        });
    });

    // Archive/Unarchive Confirmation
    const archiveForms = document.querySelectorAll('form[action*="/archive_profile"], form[action*="/unarchive_profile"]');
    archiveForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const action = form.action.includes('unarchive') ? 'reactivate' : 'archive';
            const message = action === 'archive' 
                ? 'Archiving your profile will hide it from searches. You can reactivate it later.' 
                : 'Your profile will be visible to others again.';
                
            if (!confirm(`Are you sure you want to ${action} your profile?\n${message}`)) {
                e.preventDefault();
            } else {
                const submitBtn = form.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.textContent = action === 'archive' ? 'Archiving...' : 'Reactivating...';
                    submitBtn.classList.add('loading');
                }
            }
        });
    });

    // Enhance listing cards with hover effects
    const listingCards = document.querySelectorAll('.listing-card');
    listingCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
});}
