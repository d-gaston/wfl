import React, { useState } from "react";
import { FaBars, FaTimes, FaHeart } from "react-icons/fa";
import { NavLink } from "react-router-dom";

const NavBar = ({ backgroundStyle, user, logout }) => {
    const [nav, setNav] = useState(false);

    return (
        <div className="flex justify-between items-center w-full h-20 px-4 rounded-bl-2xl rounded-br-2xl text-white bg-opacity-75 bg-pink-500 fixed">
            <div>
                <h1 className="cursor-pointer text-4xl font-header ml-2">
                    <NavLink onClick={nav ? () => setNav(!nav) : null} to="/">
                        H<FaHeart className="inline text-2xl" />
                        me
                    </NavLink>
                </h1>
            </div>

            <ul className="hidden md:flex">
                <li className="px-4 text-2xl font-header cursor-pointer text-white">
                    <NavLink to="restaurants">Restaurants</NavLink>
                </li>
                <li className="text-2xl font-header text-white">
                    <FaHeart />
                </li>
                <li className="px-4 text-2xl font-header cursor-pointer text-white">
                    <NavLink to="reviews">Reviews</NavLink>
                </li>
                <li className="text-2xl font-header text-white">
                    <FaHeart />
                </li>
                {user ? (
                    <>
                    <li className="px-4 text-2xl font-header cursor-pointer text-white">
                        <NavLink to="submitReview">Submit Review</NavLink>
                    </li>
                    <li className="px-4 text-2xl font-header cursor-pointer text-white">
                        <NavLink to="/" onClick={logout}>Log Out</NavLink>
                    </li>
                    </>
                    
                ) : (
                    <li className="px-4 text-2xl font-header cursor-pointer text-white">
                        <NavLink to="login">Log in</NavLink>
                    </li>
                )}
            </ul>
            <div
                onClick={() => setNav(!nav)}
                className="cursor-pointer pr-4 text-white md:hidden"
            >
                {nav ? <FaTimes size={20} /> : <FaBars size={20} />}
            </div>

        </div>
    );
};

export default NavBar;
