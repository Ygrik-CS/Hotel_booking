// Cart JavaScript
const API_BASE = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    loadCart();
    
    document.getElementById('checkout-btn').addEventListener('click', checkout);
    document.getElementById('clear-cart-btn').addEventListener('click', clearCart);
});

async function loadCart() {
    try {
        const response = await fetch(`${API_BASE}/cart/`);
        if (!response.ok) {
            throw new Error('Failed to load cart');
        }
        
        const items = await response.json();
        displayCartItems(items);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('cart-items').innerHTML = '<p class="error">Error loading cart</p>';
    }
}

function displayCartItems(items) {
    const cartItemsDiv = document.getElementById('cart-items');
    
    if (items.length === 0) {
        cartItemsDiv.innerHTML = `
            <div class="empty-cart">
                <h3>Your cart is empty</h3>
                <p><a href="/static/html/index.html">Start searching for hotels</a></p>
            </div>
        `;
        updateSummary(items);
        return;
    }
    
    cartItemsDiv.innerHTML = items.map(item => `
        <div class="cart-item">
            <div class="cart-item-details">
                <h3>Hotel Booking</h3>
                <p><strong>Check-in:</strong> ${item.checkin}</p>
                <p><strong>Check-out:</strong> ${item.checkout}</p>
                <p><strong>Guests:</strong> ${item.guests}</p>
            </div>
            <button onclick="removeFromCart(${item.id})">Remove</button>
        </div>
    `).join('');
    
    updateSummary(items);
}

function updateSummary(items) {
    document.getElementById('total-items').textContent = items.length;
    // Note: Total price would need to be calculated from prices API
    document.getElementById('total-price').textContent = formatPrice(items.length * 100000);
}

async function removeFromCart(itemId) {
    try {
        const response = await fetch(`${API_BASE}/cart/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to remove item');
        }
        
        loadCart();
    } catch (error) {
        console.error('Error:', error);
        alert('Error removing item from cart');
    }
}

async function clearCart() {
    if (!confirm('Are you sure you want to clear your cart?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/cart/`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to clear cart');
        }
        
        loadCart();
    } catch (error) {
        console.error('Error:', error);
        alert('Error clearing cart');
    }
}

async function checkout() {
    alert('Checkout functionality would be implemented here.\nIn a full implementation, this would:\n1. Create a guest\n2. Create a booking\n3. Process payment');
}

function formatPrice(amount) {
    return new Intl.NumberFormat('uz-UZ').format(amount);
}
