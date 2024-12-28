<script>
    import Cookies from 'js-cookie'
    let username = Cookies.get("username")
    let showTakeme = true
    if (username) { showTakeme = true }

    function pressTakeme() {
        window.location.href = username;
    }

</script>


<title>Kaze</title>
<body>
    <div class="container">
        <header class="header">
            <h1 class="logo">風</h1>
            <span class="name">Kaze</span>
        </header>

        <div class="content">
            <p class="tagline">Upload and share videos!</p>
            
            <p class="cta-text">
                To get started, make an account
            </p>
            
            <div class="actions">
                <a href="/create-account" class="button createacc">Create Account</a>
                
                <div class="or-divider">
                    <span>or</span>
                </div>
                
                <a href="/log-in" class="button login">Log in</a>
            </div>
        </div>
        {#if showTakeme}
            <button class="takeme" on:click={pressTakeme}>
                Take me to my account page
            </button>  
        {/if}

    </div>

</body>



<style>

:root {
    --primary-color: #3498db;
    --secondary-color: #f1c40f;
    --background-color: #2e2e2e;
    --text-color: rgb(192, 192, 192);
    --font-family: Arial, Helvetica, sans-serif;
    background-color: #2e2e2e;
    overflow: hidden;
    user-select: none;
}

*,
*:before,
*:after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.takeme {
    margin-top: 10px;
    background-color: #0000;
    border-style: none;
    color: rgba(0, 0, 0, 0.6);
    font-size: 17px;
}
.takeme:hover {
    cursor: pointer;
    color: rgba(0, 0, 0, 0.8);
}

body {
    font-family: var(--font-family);
    background-color: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: -80px;
}

.container {
    max-width: 800px;
    width: 90%;
    text-align: center;
    padding: 20px;
}

.header {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 40px;
}

.logo {
    font-size: 300px;
    color: hsl(199, 58%, 93%);
    transition: transform 0.3s ease;
    margin-bottom: -100px;
    margin-right: -30px;
    margin-left: 15%;
    text-shadow: 0px 30px 50px rgba(0, 0, 0, 1);
}

.name {
    font-size: 50px;
    font-weight: bold;
    color: hsl(195, 77%, 81%);
    margin-left: 10px;
    position: relative;
    top: 30px;
    text-shadow: 0px 0px 40px rgba(0, 0, 0, 1);
}

.content {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 5px 5px 20px rgba(0, 0, 0, 0.3);
}
.tagline {
    font-size: 24px;
    margin-bottom: 20px;
    color: #dbdbdb;
}

.cta-text {
    font-size: 18px;
    margin-bottom: 30px;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.button {
    display: inline-block;
    padding: 12px 20px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

.createacc {
    background-color: var(--primary-color);
    color: white;
    border-radius: 50px;
    border: none;
    box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
}

.createacc:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
}

.login {
    background-color: transparent;
    color: var(--secondary-color);
    border: 2px solid var(--secondary-color);
    border-radius: 50px;
}

.login:hover {
    background-color: rgba(241, 196, 15, 0.1);
    transform: translateY(-2px);
}

.or-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 15px;
}

.or-divider::before,
.or-divider::after {
    content: '';
    width: 40%;
    height: 1px;
    background-color: rgba(255, 255, 255, 0.2);
}

.or-divider span {
    border-radius: 10px;
    padding: 0 10px;
    background-color: var(--background-color);
}


.logo:hover {
    transform: scale(1.05);
}

@media screen and (max-width: 600px) {
    .container {
        width: 95%;
    }

    .logo {
        font-size: 200px;
    }

    .name {
        font-size: 30px;
    }

    .button {
        font-size: 16px;
        padding: 10px 15px;
    }
}
</style>