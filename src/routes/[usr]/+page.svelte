<script>
    function truncateString(str) {
        if (str.length > 10) {
          return str.slice(2); // Remove the first 2 characters
        }
        return str; // Return the string unchanged if it's not longer than 10
      }
    
    
    export let data;  // This will hold the data returned from +page.js
    import Cookies from 'js-cookie'
    // Destructure the video_url from the data prop

    let isowner = Cookies.get('username') === data.userid;

    

</script>

<dir class="useridheading">
    <h1>
        {data.display_name}
    </h1>
    <p class="userid">
        {data.userid}
    </p>
</dir>
<hr>

{#if isowner}
    <a href="/upload-video">
        <button>Upload Video</button>   
    </a>
{/if}
<div class='cards'>
    {#each data.videos as vid}
        
        <a href="/{data.userid}/{truncateString(vid.id)}" class="card">
            <img src={`http://localhost:3000/pullthumb?u=${data.userid}&v=${truncateString(vid.id)}`} alt="thumbnail">
            <div class="vidcard">
                {vid.name}
                <br>
            </div>
            
        </a>
    {/each}
</div>
<style>
:root {
        color: rgb(192, 192, 192);
        font-family: Arial, Helvetica, sans-serif;
        background-color: #2e2e2e;
        user-select: none;
    }

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 50px;
    padding: 30px;
}

.card {
    text-decoration: none;
    color: inherit;
}

img {
    width: 100%;
    height: 75%;
    border-radius: 20px;
}

.vidcard {
    border-radius: 20px;
    text-indent: 20px;
    padding-top: 10px; 
    padding-bottom: 10px; 
    color: rgb(255, 255, 255);
    margin-top: -10px;
}   

a {
    color: #2980b9;
    font-size: 20px;
    text-decoration: none;
    
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
        margin-bottom: -10px;
        font-size: 50px;
        color: aliceblue;
    }

    hr {

        border: 1px solid rgb(95, 95, 95); 
    }




    button {
        position: absolute;
        top: 10px;
        right: 40px;
        margin-left: 20px;
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
        margin-bottom: 30px;
        margin-top: 30px;
    }

    button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
    }
</style>