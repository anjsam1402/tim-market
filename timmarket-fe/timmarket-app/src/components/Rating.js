import React from 'react'
import { AiFillStar, AiOutlineStar } from 'react-icons/ai'

const Rating = ({ rating, onClick, style}) => {
  return (
   <>
      {[...Array(5)].map((_, idx) => (
            <span key={idx} onClick={() => onClick(idx)} style={style}>
               {
                  rating > idx ? (<AiFillStar fontSize="15px" />) :
                  (<AiOutlineStar fontSize="15px" />)
               }
            </span>
         ))
      }
   </> 
   )
}

export default Rating