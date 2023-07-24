import React, { useEffect, useState } from 'react'
import { CartState } from '../context/Context'
import Product from './Product';
import Filters from './Filters';
import axios from 'axios';

const Home = () => {

  const { 
    state: { products },
    productState: { sort, byStock, byFastDelivery, byRating, searchQuery },
  } = CartState();

  const transformProducts = () => {
    let sortedProducts = products;

    if (sort) {
      sortedProducts = sortedProducts.sort((a, b) =>
        sort === "lowToHigh" ? a.price - b.price : b.price - a.price
      );
    }

    if (!byStock) {
      sortedProducts = sortedProducts.filter((prod) => prod.inStock);
    }

    if (byFastDelivery) {
      sortedProducts = sortedProducts.filter((prod) => prod.fastDelivery);
    }

    if (byRating) {
      sortedProducts = sortedProducts.filter(
        (prod) => prod.ratings >= byRating
      );
    }

    if (searchQuery) {
      sortedProducts = sortedProducts.filter((prod) =>
        prod.name.toLowerCase().includes(searchQuery)
      );
    }

    return sortedProducts;
  };

  const [allProducts, setAllProducts] = useState([])

  const getProducts = async() => {
    const resp = await axios.get(`http://127.0.0.1:9000/get-all-products`)
    console.log(resp.data.data)
    setAllProducts(resp.data.data)
    console.log(allProducts)
  }

  useEffect(() => {
    getProducts()
  }, [allProducts])

  return (
    <div className='home'>
      <Filters />
      <div className='productContainer'>
        {
          transformProducts().map((product) => {
            return <Product product={ product } key={ product.id }/>
          })
        }
      </div>
    </div>
  )
}

export default Home