// Main JavaScript
const API_BASE = 'http://localhost:8000';

// Set minimum date to today
document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('checkin').setAttribute('min', today);
    document.getElementById('checkout').setAttribute('min', today);
    
    // Update cart count
    updateCartCount();
});

// Search form submission
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        city: document.getElementById('city').value,
        checkin: document.getElementById('checkin').value,
        checkout: document.getElementById('checkout').value,
        guests: parseInt(document.getElementById('guests').value)
    };
    
    // Validate dates
    if (formData.checkin >= formData.checkout) {
        alert('Checkout date must be after checkin date');
        return;
    }
    
    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').innerHTML = '';
    
    try {
        const response = await fetch(`${API_BASE}/search/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const offers = await response.json();
        displayOffers(offers, formData);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('results').innerHTML = '<p class="error">Error searching hotels. Please try again.</p>';
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
});

function displayOffers(offers, searchData) {
    const resultsDiv = document.getElementById('results');
    
    if (offers.length === 0) {
        resultsDiv.innerHTML = '<p>No hotels found. Try different search criteria.</p>';
        return;
    }
    
    resultsDiv.innerHTML = offers.map(offer => `
        <div class="offer-card">
            <h3>${offer.hotel.name}</h3>
            <div class="stars">${'⭐'.repeat(offer.hotel.stars)}</div>
            <p class="details">
                <strong>Room:</strong> ${offer.room_type.name} (${offer.room_type.capacity} guests)<br>
                <strong>Rate:</strong> ${offer.rate_plan.title} - ${offer.rate_plan.meal}<br>
                <strong>Refundable:</strong> ${offer.rate_plan.refundable ? 'Yes' : 'No'}<br>
                <strong>Nights:</strong> ${offer.nights}
            </p>
            <div class="price">${formatPrice(offer.total_price)} UZS</div>
            <button onclick="addToCart(${JSON.stringify(offer).replace(/"/g, '&quot;')}, ${JSON.stringify(searchData).replace(/"/g, '&quot;')})">
                Add to Cart
            </button>
        </div>
    `).join('');
}

async function addToCart(offer, searchData) {
    const cartItem = {
        hotel_id: offer.hotel.id,
        room_type_id: offer.room_type.id,
        rate_id: offer.rate_plan.id,
        checkin: searchData.checkin,
        checkout: searchData.checkout,
        guests: searchData.guests
    };
    
    try {
        const response = await fetch(`${API_BASE}/cart/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cartItem)
        });
        
        if (!response.ok) {
            throw new Error('Failed to add to cart');
        }
        
        alert('Added to cart!');
        updateCartCount();
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding to cart');
    }
}

async function updateCartCount() {
    try {
        const response = await fetch(`${API_BASE}/cart/`);
        const items = await response.json();
        document.getElementById('cart-count').textContent = items.length;
    } catch (error) {
        console.error('Error updating cart count:', error);
    }
}

function formatPrice(amount) {
    return new Intl.NumberFormat('uz-UZ').format(amount);
}
