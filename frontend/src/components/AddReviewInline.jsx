import React, { useState } from "react";
import { useAuth } from "../App";

export default function AddReviewInline({ restaurantId, onAdded }) {
  const { user } = useAuth();
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');

  async function submit() {
    if (!user) return alert('Login or continue as guest');
    try {
      const payload = { user_name: user, user_id: 1, restaurant_id: restaurantId, rating, comment };
      const res = await fetch('/add_review', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify(payload)
      });
      if(res.ok){ setComment(''); onAdded && onAdded(); }
      else alert('Error adding review');
    } catch(e){ console.error(e) }
  }

  return (
    <div style={{display:'flex',gap:8,alignItems:'center'}}>
      <select value={rating} onChange={e=>setRating(e.target.value)} className="input" style={{width:120}}>
        {[5,4,3,2,1].map(v => <option key={v} value={v}>{v} star</option>)}
      </select>
      <input className="input" placeholder="Write a comment" value={comment} onChange={e=>setComment(e.target.value)} style={{flex:1}} />
      <button className="btn" onClick={submit}>Submit</button>
    </div>
  );
}
