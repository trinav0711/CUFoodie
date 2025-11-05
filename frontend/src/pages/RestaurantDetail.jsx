import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../App";

export default function RestaurantDetail() {
  const { id } = useParams();
  const [restaurant,setRestaurant] = useState(null);
  const [menu,setMenu] = useState([]);
  const [reviews,setReviews] = useState([]);

  useEffect(()=>{ fetchData(); }, [id]);

  async function fetchData() {
    try {//Flask API calls to get restaurant details, menu, and reviews
      const [rRes, mRes, revRes] = await Promise.all([
        fetch(`/restaurant_api/${id}`),
        fetch(`/menu_api/${id}`),
        fetch(`/reviews_api?restaurant_id=${id}`)
      ]);
      setRestaurant(await rRes.json());
      setMenu(await mRes.json());
      setReviews(await revRes.json());
    } catch(e){ console.error(e); }
  }

  if(!restaurant) return <div className="small">Loading…</div>;

  return (
    <div>
      <h3>{restaurant.name}</h3>
      <div className="small">{restaurant.cuisine_type} • {restaurant.location} • Avg Rating: {restaurant.avg_rating||'—'}</div>

      <div style={{marginTop:12}} className="card">
        <h4>Menu</h4>
        <table className="table"><thead><tr><th>Dish</th><th>Price</th><th>Tags</th></tr></thead>
        <tbody>
          {menu.map(m=>(
            <tr key={m.menu_id}><td>{m.name}</td><td>${m.price}</td><td className="small">{m.dietary_tags}</td></tr>
          ))}
        </tbody></table>
      </div>

      <div style={{marginTop:12}} className="card">
        <h4>Reviews</h4>
        {reviews.length===0 && <div className="small">No reviews yet</div>}
        {reviews.map(rv=>(
          <div key={rv.review_id} style={{padding:'8px 0',borderBottom:'1px solid #f0f0f0'}}>
            <div style={{fontWeight:600}}>{rv.user_name} <span className="small">• {rv.review_date}</span></div>
            <div className="small">Rating: {rv.rating}</div>
            <div style={{marginTop:6}}>{rv.comment}</div>
          </div>
        ))}
        <div style={{marginTop:10}}>
          <AddReviewInline restaurantId={id} onAdded={fetchData} />
        </div>
      </div>
    </div>
  );
}

function AddReviewInline({restaurantId, onAdded}) {
  const { user } = useAuth();
  const [rating,setRating] = useState(5);
  const [comment,setComment] = useState('');

  async function submit() {
    if(!user) return alert('Login or continue as guest to post review');
    try {
      const payload = { user_name:user, user_id:1, restaurant_id:restaurantId, rating, comment };
      const res = await fetch('/add_review', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
      if(res.ok){ setComment(''); onAdded && onAdded(); }
      else alert('Error adding review');
    } catch(e){ console.error(e); }
  }

  return (
    <div style={{display:'flex',gap:8,alignItems:'center'}}>
      <select value={rating} onChange={e=>setRating(e.target.value)} className="input" style={{width:120}}>
        {[5,4,3,2,1].map(v=> <option key={v} value={v}>{v} star</option>)}
      </select>
      <input className="input" placeholder="Write a short comment" value={comment} onChange={e=>setComment(e.target.value)} style={{flex:1}} />
      <button className="btn" onClick={submit}>Submit</button>
    </div>
  );
}
