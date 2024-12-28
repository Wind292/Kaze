<script>
    import Cookies from 'js-cookie'
    import { onMount } from 'svelte';

    onMount(() => {

        // if (Cookies.get("username")) {
        //     window.location.href = Cookies.get("username"); // Opens the link in the current tab
        // }

    });


    let error = "" 

    let username = ""
    let password = ""
    
    async function submit() {
        let encpassword = encodeURIComponent(password);

        let url = `http://localhost:3000/passwordcheck?username=${username}&password=${encpassword}` 

        const response = await fetch(url);
        let data = await response.text();

        console.log(data);

        if (data === "Ok") {
            Cookies.set('password', password, {expires: 30})
            Cookies.set('username', username, {expires: 30})
            
            window.location.href = Cookies.get("username");
            return
        }
        console.log(data)
        error = data
    }
    let visible = true;
    $: visible = error === ""

    function filterID(event) {
        const validChars = /^[a-z0-9_]*$/;
        const input = event.target.value;

        if (!validChars.test(input)) {
        // If the input contains invalid characters, remove them
        username = input.replace(/[^a-z0-9_]/g, '');
        } else {
            username = input;
        }
    }




</script>
<dir class="container">
    <h1>Login</h1>

    <hr>
    User ID <br>
    <input bind:value={username} on:input={filterID} type="text" name="" id="">
    <br><br>
    Password <br>
    <input bind:value={password} type="password" name="" id="">

    

    <hr>
    <button on:click={submit}>Log In</button>

    <br><br>
</dir>

<div class="error-container" class:special={visible}>
    {error}
</div>


<style>

    :root {
        color: rgb(192, 192, 192);
        font-family: Arial, Helvetica, sans-serif;
        background-color: #2e2e2e;
        overflow: hidden;
        user-select: none;
    }
    
    .error-container {
        opacity: 1;
        border-radius: 3px;
        font-weight: bold;
        color: aliceblue;
        border-style: solid;
        text-align: center;
        max-width: fit-content;
        margin-left: -40px;
        padding: 10px;
        width: 50%;
        margin: 20px auto;
        margin-top: calc(20vh + 400px);
        background-color: rgba(255, 0, 0, 0.1);
        opacity: 1;
        transform: scale(0.9);
        animation: appear 0.5s ease-in-out forwards;
        border-radius: 10px;
        border-color: #9f0000;
        transition: opacity 0.2s ease;
    }


    .special {
        opacity: 0;
    }
    
    @keyframes opacity {
        0% {
            opacity: 0;
            transform: scale(0.9); /* Shrink slightly */
        }
        100% {
            opacity: 1;
            transform: scale(1); /* Restore to normal size */
        }
    }


    h1 {
        text-align: center;
        font-size: 50px;
        color: aliceblue;
    }

    hr {
        max-width: 80%;
        display: flex;
        justify-content: center;   
        border: 1px solid rgb(95, 95, 95); 
    }

    input {
        border-radius: 15px;
        border-style: none;
        padding: 5px;
        padding-left: 10px;
        padding-right: 10px;
        background: rgba(255, 255, 255, 0.4);
    }



    .container {
        padding: 0px;
        position: absolute;
        width: 40%;
        border-style: none;
        border-radius: 20px;
        left: 30%;
        top: 20vh;
        background-color: rgba(255, 255, 255, 0.05);
        box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
    }



    button {
        display: inline-block;
        padding: 12px 20px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        background-color: #3498db;
        transition: background-color 0.3s ease, transform 0.3s ease;
        color: white;
        border-radius: 50px;
        border: none;
        box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
    }

    button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }
</style>