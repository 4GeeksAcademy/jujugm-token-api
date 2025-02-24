import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";

export const Profile = () => {
    const { store, actions } = useContext(Context);


    useEffect(()=>{
        actions.getProfileFavorites()
    },[])

    return (
        <div className="text-center mt-5">
            <h1>Profile</h1>
        </div>
    );
};
