import React, { createContext, useContext, useReducer, useState } from 'react'
import faker from "faker"
import { cartReducer, productReducer } from './Reducer'
import APISerive from '../components/APIService'
import axios from 'axios'
// import ShoppingCart from '../components/ShoppingCart'

const Cart = createContext()
faker.seed(99)

const Context = ({ children }) => {
  // const [isOpen, setIsOpen] = useState(false)
  // const openCart = () => setIsOpen(true)
  // const closeCart = () => setIsOpen(false)

  const products = [...Array(20)].map(() => ({
    id: faker.datatype.uuid(),
    name: faker.commerce.productName(),
    image: "https://fakestoreapi.com/img/61pHAEJ4NML._AC_UX679_.jpg",
    price: faker.commerce.price(),
    inStock: faker.random.arrayElement([0, 3, 5, 6, 7])
  }))


  
  // console.log(products1)

  const [state, dispatch] = useReducer(cartReducer, {
    products: products,
    cart: [],
    // isOpen,
    // openCart,
    // closeCart
  })

  const [productState, productDispatch] = useReducer(productReducer, {
    byStock: false,
    byFastDelivery: false,
    byRating: 0,
    searchQuery: "",
  });

  // console.log(productState);

  return (
    <Cart.Provider value={{ state, dispatch, productState, productDispatch }}>
      { children }
      {/* <ShoppingCart openCartFun={isOpen}/> */}
    </Cart.Provider>
  )
}

export default Context

// export default Cart

export const CartState = () => {
  return useContext(Cart);
};