<script>
    export let data;  // This will hold the data returned from +page.js

    
    // Destructure the video_url from the data prop
    let videoSrc = data.video_url;
</script>

<video width="90%" controls>
    <source src={videoSrc} type="video/mp4" />
    Your browser does not support the video tag.
    <track kind="captions">
</video>
