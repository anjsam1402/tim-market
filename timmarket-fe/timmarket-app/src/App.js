
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Header from './components/Header'
import Home from './components/Home'
import Cart from './components/Cart'
import Login from './components/Login';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <div className='main-body'> 
        <Routes>
      {/* <Route exact path="/" element={<Login />} /> */}
          <Route path="/" exact element={<Home />} />
          <Route path="/cart" exact element={<Cart />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
