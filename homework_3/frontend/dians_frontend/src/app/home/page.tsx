import React from "react";
import {ROUTES} from "@/src/config/routes";
import Link from "next/link";

const Home = () => {
    return (
        <div>
            <h1>Home</h1>
            <div>
                <Link href={ROUTES.ABOUT}>Click me!</Link>
            </div>
        </div>
    );
};

export default Home;