import React from 'react'
import { Button, Card } from 'react-bootstrap'
import { CartState } from '../context/Context'

const Product = ({ product }) => {
  const {state: { cart }, dispatch } = CartState();

  return (
    <div className='product'>
      <Card>
         <Card.Img variant='top' src={ "https://fakestoreapi.com/img/61pHAEJ4NML._AC_UX679_.jpg" } alt={product.name}/>
         {/* <Card.Img variant='top' src={product.image} alt={product.name}/> */}
         <Card.Body>
          <Card.Title>{ product.name }</Card.Title>
          <Card.Subtitle style={{ paddingBottom:10 }}>
            <span>&#x20AC;{product.price}</span>
          </Card.Subtitle>
          {
            cart.some(p => p.id === product.id) ?
            (<Button variant='danger' onClick={
              () => { dispatch({type: "REMOVE_FROM_CART", payload: product}) }}>
                Remove from cart
            </Button>) :
            (<Button disabled={!product.inStock} onClick={
              () => { dispatch({type: "ADD_TO_CART", payload: product}) }}>
              {!product.inStock ? "Out of stock" : "Add to cart" }
            </Button>)
          }
         </Card.Body>
      </Card>
    </div>
  )
}

export default Product