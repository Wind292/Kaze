<script>
    import { onMount } from 'svelte';

    export let data;  // This will hold the data returned from +page.js

    let iscompressed = data.iscompressed;

    // Destructure the video_url from the data prop
    let videoSrc;
    let videoValid = true;



    onMount(() => {
        videoSrc = data.video_url;

        if (!videoSrc) {
            videoValid = false;
        }
        if (!iscompressed ) {
            videoSrc = videoSrc.replace("c-", "")
        }

        console.log(videoSrc);
        checkVideo();
    });

    function checkVideo() {
        const videoElement = document.createElement('video');
        videoElement.src = videoSrc;
        
        videoElement.addEventListener('loadedmetadata', () => {
            videoValid = true;
        });

        videoElement.addEventListener('error', () => {
            videoValid = false;
        });
    }
</script>

{#if !videoValid}
    <p>Sorry, the video could not be loaded or is unavailable.</p>
{:else}
    
    <video width="90%" controls>
        <source src={videoSrc} type="video/mp4" />
        Your browser does not support the video tag. Use something like Chrome or Firefox.
        <track kind="captions">
    </video>
    <h1>title</h1>
    {videoSrc}
{/if}

<style>  
    /* Hides scrollbar in WebKit browsers like Chrome and Safari */
    :root::-webkit-scrollbar {
        display: none;
    }
    :root {
        overflow-x: hidden;
        overflow: auto; /* Ensures scrolling is still functional */
        scrollbar-width: none; /* Hides scrollbar in Firefox */
        color: rgb(192, 192, 192);
        font-family: Arial, Helvetica, sans-serif;
        background-color: #2e2e2e;
        user-select: none;
    }
    video {
        height: 99.9vh;
        width: 100vw;
        margin-left: -8px;
        margin-top: -8px;
    }
    p {
        font-size: 100%;
    }
</style>