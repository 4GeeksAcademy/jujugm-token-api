import React, {useContext} from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";

export const Navbar = () => {
	const {store, actions } = useContext(Context)
	console.log(store.auth);
	return (
		<nav className="navbar navbar-light bg-light">
			<div className="container">
				<Link to="/">
					<span className="navbar-brand mb-0 h1">React Boilerplate</span>
				</Link>
				<div className="ml-auto">
				{store.auth ? (
    <button onClick={() => actions.logout()} className="btn btn-danger">Logout</button>
) : null}
				</div>
			</div>
		</nav>
	);
};
