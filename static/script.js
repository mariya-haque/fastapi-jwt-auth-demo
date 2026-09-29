let token = "";

// ======================
// SIGNUP
// ======================

async function signup() {

    const username = document.getElementById("signup_username").value;
    const email = document.getElementById("signup_email").value;
    const password = document.getElementById("signup_password").value;

    const response = await fetch("/signup", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username,
            email,
            password
        })
    });

    const data = await response.json();

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}


// ======================
// LOGIN
// ======================

async function login() {

    const username = document.getElementById("login_username").value;
    const password = document.getElementById("login_password").value;

    const response = await fetch("/login", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username,
            password
        })

    });

    const data = await response.json();

    if (data.token) {

        token = data.token;

        localStorage.setItem("token", token);

    }

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}


// ======================
// PROFILE
// ======================

async function profile() {

    token = localStorage.getItem("token");

    const response = await fetch("/profile", {

        method: "GET",

        headers: {
            Authorization: "Bearer " + token
        }

    });

    const data = await response.json();

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}


// ======================
// GET USERS
// ======================

async function getUsers() {

    const response = await fetch("/users");

    const data = await response.json();

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}


// ======================
// DELETE USER
// ======================

async function deleteUser() {

    token = localStorage.getItem("token");

    const response = await fetch("/delete", {

        method: "DELETE",

        headers: {
            Authorization: "Bearer " + token
        }

    });

    const data = await response.json();

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}


// ======================
// LOGOUT
// ======================

async function logout() {

    token = localStorage.getItem("token");

    const response = await fetch("/logout", {

        method: "POST",

        headers: {
            Authorization: "Bearer " + token
        }

    });

    const data = await response.json();

    localStorage.removeItem("token");

    document.getElementById("output").innerHTML =
        JSON.stringify(data, null, 4);

}