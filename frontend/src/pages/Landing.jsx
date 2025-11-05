import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../App";

export default function Landing() {
  const { setUser } = useAuth();
  const [name, setName] = useState("");
  const navigate = useNavigate();

  function login(e) {
    e.preventDefault();
    if(name.trim()==="") return alert('Enter username or continue as guest');
    setUser(name.trim());
    navigate('/dashboard');
  }

  function guest() {
    setUser('Guest');
    navigate('/dashboard');
  }

  return (
    <div style={{display:'grid',placeItems:'center',minHeight:'60vh'}}>
      <div className="card" style={{width:420,textAlign:'center'}}>
        <h2>CUFoodie</h2>
        <p className="small">Discover Morningside Heights eats — simple and fast.</p>
        <form onSubmit={login} style={{marginTop:12}}>
          <input className="input" placeholder="Username" value={name} onChange={e=>setName(e.target.value)} style={{width:'100%'}} />
          <div style={{display:'flex',gap:8,marginTop:12,justifyContent:'center'}}>
            <button className="btn" type="submit">Login</button>
            <button type="button" className="btn" style={{background:'#777'}} onClick={guest}>Continue as Guest</button>
          </div>
        </form>
      </div>
    </div>
  );
}
