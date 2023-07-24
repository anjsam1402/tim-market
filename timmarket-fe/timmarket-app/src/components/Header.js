import React, { useState } from 'react'
import { Badge, Button, Container, Dropdown, FormControl, Nav, Navbar, NavbarBrand } from 'react-bootstrap'
import { ImCart } from 'react-icons/im'
import { Link } from 'react-router-dom'
import { CartState } from '../context/Context'
import Cart from './ShoppingCart'
import Product from './Product'
import { AiFillDelete } from 'react-icons/ai'


const Header = () => {
   const {state:{ cart,}, dispatch} = CartState();
   // const [isCartOpen, setIsCartOpen] = useState(false)

  return (
      <Navbar sticky="top" bg="danger" style={{ height: 80 }}>
      {/* // <Navbar sticky="top" className='bg-white shadow-sm mb-3 '> */}
         <Container>
            <NavbarBrand>
               <Link to="/">Shopping Cart</Link>
            </NavbarBrand>
            <Navbar.Text className='search'>
               <FormControl
                  style={{ width: 400 }}
                  placeholder='Looking for something'
                  className='m-auto'
               />
            </Navbar.Text>
            <Nav>
               <Dropdown align="end">
                  <Dropdown.Toggle variant='primary'>
                     <ImCart color='white' fontSize="25px" />
                     <Badge>{ cart.length }</Badge>
                  </Dropdown.Toggle>
                  <Dropdown.Menu className="dropdown-menu-right" style={{ minWidth:370 }}>
                     {
                        cart.length > 0 ? 
                        (<>
                           {cart.map((prod) => (
                              <span className='cartitem' key={prod.id}>
                                 <img src={prod.image} className="cartItemImg" alt={prod.name} />
                                 <div className='cartItemDetail'>
                                    <span>{ prod.name }</span>
                                    <span>&#x20AC;{ prod.price }</span>
                                 </div>
                                 <AiFillDelete 
                                    fontSize={"20px"}
                                    style={{ cursor:"pointer" }}
                                    onClick={()=>dispatch({ type: "REMOVE_FROM_CART", payload: prod })}/>
                              </span>
                           ))}
                           <Link to="/cart">
                              <Button style={{ width: "95%", margin: "0 10px"}}>
                                 Go to Cart
                              </Button>
                           </Link>
                        </>) : 
                        (<span> Cart is empty</span>)
                     }
                  </Dropdown.Menu>
               </Dropdown>
               {/* <Button style={{ width:"3rem", height:"3rem", position:"relative" }}
                  variant='outline-primary'
                  className='rounded-circle'
                  size="sm"
                  onClick={()=> {
                     openCart();
                  }}
               >
                  <ImCart color='white' fontSize="30px" />
                  <div className='rounded-circle bg-secondary d-flex justify-content-center align-items-center' 
                  style={{ 
                     height:"1.5rem", 
                     width:"1.5rem", 
                     color:"white",
                     bottom:0,
                     right:0,
                     position:"absolute",
                     transform:"translate(25%, 25%)"
                  }}>{ cart.length }</div>
               </Button> */}
            </Nav>
         </Container>
      </Navbar>
  )
}

export default Header;