import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export default function RestaurantDetail() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);
  const [reviews, setReviews] = useState([]);

  useEffect(() => { fetchData(); }, [id]);

  async function fetchData() {
    try {
      // Fetch all restaurants, dishes, and reviews from backend
      const [rRes, mRes, revRes] = await Promise.all([
        fetch('/api/restaurants'),
        fetch('/api/dishes'),
        fetch('/api/reviews')
      ]);

      const restaurants = await rRes.json();
      const dishes = await mRes.json();
      const reviewsAll = await revRes.json();

      // Match restaurant by name (since backend doesn't return numeric id)
      const r = restaurants.find(r => String(r.name) === String(id) || String(r.restaurant_id) === String(id));
      setRestaurant(r || null);

      if (r) {
        setMenu(dishes.filter(m => String(m.restaurant_name) === String(r.name)));
        setReviews(reviewsAll.filter(rv => String(rv.restaurant_name) === String(r.name)));
      }
    } catch (e) {
      console.error(e);
    }
  }

  if (!restaurant) return <div className="small">Loading…</div>;

  return (
    <div>
      <h3>{restaurant.name}</h3>
      <div className="small">
        {restaurant.cuisine_type} • {restaurant.location} • Avg Rating: {restaurant.avg_rating || '—'}
      </div>

      <div style={{ marginTop: 12 }} className="card">
        <h4>Menu</h4>
        {menu.length === 0 && <div className="small">No menu items available</div>}
        <table className="table">
          <thead>
            <tr><th>Dish</th><th>Price</th><th>Tags</th></tr>
          </thead>
          <tbody>
            {menu.map(m => (
              <tr key={`${m.dish_name}-${m.restaurant_name}`}>
                <td>{m.dish_name}</td>
                <td>${m.price}</td>
                <td className="small">{m.dietary_tags}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: 12 }} className="card">
        <h4>Reviews</h4>
        {reviews.length === 0 && <div className="small">No reviews yet</div>}
        {reviews.map(rv => (
          <div key={rv.review_id} style={{ padding: '8px 0', borderBottom: '1px solid #f0f0f0' }}>
            <div style={{ fontWeight: 600 }}>
              {rv.user_name}
              <span className="small"> • {rv.review_date}</span>
            </div>
            <div className="small">Rating: {rv.rating}</div>
            <div style={{ marginTop: 6 }}>{rv.comment}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

