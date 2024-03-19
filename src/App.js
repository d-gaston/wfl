import NavBar from "./components/NavBar";
import backgroundImg from "./Background.jpeg";
import ExteriorLinks from "./components/ExteriorLinks";
import React, { useState, useEffect } from "react";
import { Outlet } from "react-router-dom";
import { useNavigate } from "react-router-dom";
function App() {
    const backgroundStyle = {
        backgroundImage: `url(${backgroundImg})`,
        backgroundSize: "cover",
        backgroundPosition: "left bottom",
        backgroundRepeat: "no-repeat",
        minHeight: "100vh",
        position: "fixed",
        width: "100%",
        zIndex: "-1",
    };
    const contentStyle = {
        minHeight: "100vh",
        overflowY: "auto",
    };
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    /**********************
        Check Session 
        Done whenever the page is reloaded
    ************************/
    useEffect(() => {
        fetch(`/check_session`).then((res) => {
            if (res.ok) {
                res.json().then((user) => setUser(user));
            }
        });
    }, []);

    /**********************
        Authentication
        Functions that will be passed down
    ************************/
    function attemptLogin(userInfo) {
        fetch(`/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Accepts: "application/json",
            },
            body: JSON.stringify(userInfo),
        })
            .then((res) => {
                if (res.ok) {
                    return res.json();
                }
                throw res;
            })
            // if we log in successfully, we want to store the
            // user object in state
            .then((data) => {
                setUser(data);
                // go to the home page if we log in successfully
                navigate("/");
            })
            .catch((e) => {
                alert('incorrect username or password')
                console.log(e);
            });
    }
    function logout() {
        // for logging out we just set user to null
        fetch(`/logout`, { method: "DELETE" }).then((res) => {
            if (res.ok) {
                setUser(null);
            }
        });
    }
    return (
        <div style={backgroundStyle}>
            <NavBar
                backgroundStyle={backgroundStyle}
                user={user}
                logout={logout}
            />
            <div style={contentStyle}>
                <Outlet context={{ user, attemptLogin, logout }} />
                <ExteriorLinks />
            </div>
            <footer className="mt-4 text-xs">Made by Kirstyn Canull</footer>
        </div>
    );
}

export default App;
