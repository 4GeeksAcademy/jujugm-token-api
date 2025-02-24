const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			auth: false,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			login: async (email, password) => {


				const myHeaders = new Headers();
				myHeaders.append("Content-Type", "application/json");

				const raw = JSON.stringify({
					"email": email,
					"password": password
				});

				const requestOptions = {
					method: "POST",
					headers: myHeaders,
					body: raw,
				
				};

				try {
					const response = await fetch("https://urban-spork-4vw9jq7pxwh7vgx-3001.app.github.dev/api/login", {
						method: "POST",
						headers: {
							"Content-Type": "application/json"
						},
						body: JSON.stringify({ email, password })
					});
			
					if (!response.ok) {
						throw new Error(`Error en login: ${response.status}`);
					}
			
					const data = await response.json();
					console.log("🔑 Token recibido:", data.access_token);
			
					localStorage.setItem("token", data.access_token);
					setStore({ auth: true }); //  Ahora sí se actualiza el estado
			
				} catch (error) {
					console.error(error);
					return false;
				};
			},
			// con esta funcion pido el token
			getProfileFavorites: async () => {
				let token = localStorage.getItem("token")
				try {
					const response = await fetch("https://orange-capybara-pjprjxvrjpv4h7pp9-3001.app.github.dev/api/profile", {
						method: "GET",
						headers: {
							"Authorization": `Bearer ${token}`
						},
					});
					const result = await response.json();
					
				} catch (error) {
					console.error(error);
				};
			},
			tokenVerify: async () => {
				let token = localStorage.getItem("token")
				try {
					const response = await fetch("https://urban-spork-4vw9jq7pxwh7vgx-3001.app.github.dev/api/favorites", {
						method: "GET",
						headers: {
							"Authorization": `Bearer ${token}`
						},
					});
					const result = await response.json();

					if (response.status !== 200) {
						setStore({auth:result.valid})
					}
					setStore({auth:result.valid})
				} catch (error) {
					console.error(error);
				};
			},
			
							//la peticion en la funcion tokenVerify del front deberia actualizar un estado auth:
			
			logout:()=>{
				//borrar el token del localStorage
					localStorage.removeItem("token");
					setStore({ auth: false });
					console.log("Usuario deslogueado");
			},
			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;
