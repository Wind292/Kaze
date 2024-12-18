<script>
    export let data;  // This will hold the data returned from +page.js

    // Destructure the video_url from the data prop
    let videoSrc = data.video_url;

    let videoValid = true
    checkVideo()

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
        Your browser does not support the video tag.
        <track kind="captions">
    </video>
{/if}

<h1>title</h1>

<style>
    video {
        height: 99.9vh;
        width: 100vw;
        margin-left: -8px;
        margin-top: -8px;
    }

</style>