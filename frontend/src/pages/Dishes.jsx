import React, { useState, useEffect } from "react";

export default function Dishes() {
  const [name,setName] = useState('');
  const [tag,setTag] = useState('');
  const [maxPrice,setMaxPrice] = useState('');
  const [data,setData] = useState([]);

  async function fetchList() {
    const q = new URLSearchParams({name, tag, maxPrice}).toString();
    //Flask endpoint invoked here to get dishes
    const res = await fetch('/dishes_api?'+q);
    setData(await res.json());
  }

  useEffect(()=>{ fetchList(); }, []);

  return (
    <div>
      <h3>Dishes</h3>
      <div className="card">
        <div className="controls">
          <input className="input" placeholder="Dish name" value={name} onChange={e=>setName(e.target.value)} />
          <input className="input" placeholder="Dietary tag" value={tag} onChange={e=>setTag(e.target.value)} />
          <input className="input" placeholder="Max price" value={maxPrice} onChange={e=>setMaxPrice(e.target.value)} style={{width:120}} />
          <button className="btn" onClick={fetchList}>Apply</button>
        </div>

        <table className="table" style={{marginTop:12}}>
          <thead><tr><th>Dish</th><th>Served At</th><th>Price</th><th>Tags</th></tr></thead>
          <tbody>
            {data.length===0 && <tr><td colSpan={4} className="small">No dishes — press Apply</td></tr>}
            {data.map(d=>(
              <tr key={`${d.dish_id}-${d.restaurant_id}`}>
                <td>{d.name}</td>
                <td>{d.restaurant_name}</td>
                <td>${d.price}</td>
                <td className="small">{d.dietary_tags}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
