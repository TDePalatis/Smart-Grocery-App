
const items = [
  {
    name: 'Milk',
    quantity: 2,
    expiry: '2025-05-01',
    image: 'https://images.pexels.com/photos/248412/pexels-photo-248412.jpeg?auto=compress&cs=tinysrgb&w=1200'
  },
  {
    name: 'Eggs',
    quantity: 12,
    expiry: '2025-04-25',
    image: 'https://images.pexels.com/photos/518525/pexels-photo-518525.jpeg?auto=compress&cs=tinysrgb&w=1200'
  },
  {
    name: 'Bread',
    quantity: 2,
    expiry: '2025-04-30',
    image: 'https://images.pexels.com/photos/30478768/pexels-photo-30478768/free-photo-of-freshly-baked-loaf-of-bread-on-cooling-rack.jpeg?auto=compress&cs=tinysrgb&w=1200'
  },
  {
    name: 'butter',
    quantity: 1,
    expiry: '2025-06-15',
    image: 'https://images.pexels.com/photos/7110152/pexels-photo-7110152.jpeg?auto=compress&cs=tinysrgb&w=1200'
  },
  {
    name: 'jam',
    quantity: 1,
    expiry: '2025-06-01',
    image: 'https://images.pexels.com/photos/1051849/pexels-photo-1051849.jpeg?auto=compress&cs=tinysrgb&w=1200'
  }
];

const container = document.getElementById('inventory-view');

items.forEach(item => {
  const div = document.createElement('div');
  div.innerHTML = `
    <img src="${item.image}" alt="${item.name}" style="width: 100%; border-radius: 8px;">
    <strong>${item.name}</strong><br>
    Qty: ${item.quantity}<br>
    Expires: ${item.expiry}
  `;
  div.style.border = "1px solid #ccc";
  div.style.padding = "10px";
  div.style.borderRadius = "8px";
  div.style.background = "#fff";
  container.appendChild(div);
});
