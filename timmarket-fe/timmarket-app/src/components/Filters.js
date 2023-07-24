import React from 'react'
import { Button, Form } from 'react-bootstrap'
import Rating from './Rating'
import { CartState } from '../context/Context';

const Filters = () => {
  const {
    productDispatch,
    productState: { byStock, byFastDelivery, sort, byRating },
  } = CartState();
  return (
    <div className='filters' sticky="top">
      <span>Filter Products</span>
      <span>
         <Form.Check
         inline
         label="Ascending"
         name='group1'
         type='radio'
         id={`inline-1`}
          onChange={() =>
            productDispatch({
              type: "SORT_BY_PRICE",
              payload: "lowToHigh",
            })
          }
          checked={sort === "lowToHigh" ? true : false}
         />
      </span>
      <span>
         <Form.Check
         inline
         label="Descending"
         name='group1'
         type='radio'
         id={`inline-2`}
          onChange={() =>
            productDispatch({
              type: "SORT_BY_PRICE",
              payload: "highToLow",
            })
          }
          checked={sort === "highToLow" ? true : false}
         />
      </span>
      <span>
         <Form.Check
         inline
         label="Include Out of stock"
         name='group1'
         type='checkbox'
         id={`inline-3`}
          onChange={() =>
            productDispatch({
              type: "FILTER_BY_STOCK",
            })
          }
          checked={byStock?1:0}
         />
      </span>
      <span>
         <Form.Check
         inline
         label="Fast Delivery"
         name='group1'
         type='checkbox's
         id={`inline-4`}
          onChange={() =>
            productDispatch({
              type: "FILTER_BY_DELIVERY",
            })
          }
          checked={byFastDelivery.toString()}
         />
      </span>
      <span>
         <label style={{ paddingRight: 10 }}>Rating</label>
         <Rating style={{ cursor: "pointer" }} rating={ byRating }
          onClick={(i) =>
            productDispatch({
              type: "FILTER_BY_RATING",
              payload: i + 1,
            })
          } />
      </span>
      <Button variant='light'>Clear Filters</Button>
    </div>
  )
}

export default Filters