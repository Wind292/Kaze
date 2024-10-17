<script>
    
    
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

{#each data.videos as vid}
    <a href="/{data.userid}/{vid.id}">
        <div class="vidcard">
            {vid.name}
            <br>
        </div>
    </a>
{/each}

<style>
    :root {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;    
    }
    h1 {
        margin-bottom: -10px;
    }
    .userid {
        font-weight: 600;
        color: #676767;
    }
    .vidcard {
        margin-left: 50px;
        padding: 4px;
        margin-bottom: 10px;
    }
</style>