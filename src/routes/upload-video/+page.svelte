<script>
  import { onMount } from 'svelte';
  import Cookies from 'js-cookie'

  import {tweened } from "svelte/motion";
  import { cubicOut } from 'svelte/easing';

  let isLoading = false;

  let title = "";
  let file;
  let user;
  let error = "";
  let password;
  let visible = false;
  let uploadProgress = 0;
  $: visible = error === ""

  const progress = tweened(0, {
    duration: 100,
    easing: cubicOut
  });

  onMount(() => {

    if (!Cookies.get("username")) {
        window.location.href = Cookies.get("log-in"); 
    }
    user = Cookies.get("username")

    if (!Cookies.get("password")) {
        window.location.href = Cookies.get("log-in");
    }
    password = Cookies.get("password")

  });

  async function handleSubmit(event) {
    
    event.preventDefault();

    if (!file) {
      error = "No file chosen"
      return
    }
    if (!title) {
      error = "No title"
      return
    }
    

    const formData = new FormData();
    formData.append('video', file); 
    formData.append('user', user);
    formData.append('title', title);
    formData.append('password', password);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:3000/uploadvideo', true);

    isLoading = true

    // Update progress bar
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        uploadProgress = Math.round((event.loaded / event.total) * 100);
        progress.set(uploadProgress/100)
      }
    };

    
    // Handle success and error
    xhr.onload = () => {
      isLoading = false;

      if (xhr.status === 200) {
        console.log('Upload successful');
        window.location.href = `${user}/`;
        
      } else {
        error = 'Upload failed: ' + xhr.responseText;
        console.error(error);
      }
    };

    xhr.onerror = () => {
      isLoading = false;
      error = 'An error occurred during the upload.';
      console.error(error);
    };

    xhr.send(formData);
  }
</script>
<div class="container">
{#if isLoading === false}
    
    <h1>
      Upload Video
    </h1>
    <hr>
    Title <br>
    <input bind:value={title}>
    <hr>
    <br>
  <form on:submit={handleSubmit}>
    <input type="file" accept="video/*" on:change="{(e) => file = e.target.files[0]}" />
    <br><br>
    <button type="submit">Upload Video</button>
  </form>




{/if}
{#if isLoading}
  <h1>
    Uploading...
  </h1>
  <p>
    Don't close this window or your upload will be canceled
    <br>
    Once the upload is done your will be redirected to your account page
    <br><br><br>
  </p>

  <div class="up-prog">{uploadProgress}%</div>
  

  <div class="outer-pro">
    <div class="inner-pro" style="width: {$progress*100}%">
    </div>  
  </div>

{/if}

</div>


<div class="error-container" class:special={visible}>
  {error}
</div>

<style>

  .up-prog {
    margin-bottom: -60px;
    font-size: 30px;
    color: aliceblue;
    font-weight: bold;
  }

  .inner-pro, .outer-pro {  
    height: 40px;
    border-radius: 15px;
    
  }

  
  .outer-pro {
    
    width: calc(100%-20px);
    border: 1px solid #000; 
    z-index: 100; 
    margin: 20px;
  }

  .inner-pro {
    width: 0%;
    background-color: #3498db;;
  }


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

  input[type=file]::file-selector-button {
    border-radius: 5px;
    border: none;
    margin-left: -80px;
    visibility: hidden;
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

  form {
    margin-bottom: 20px;
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
      margin-bottom: 20px;
  }

  button:hover {
      background-color: #2980b9;
      transform: translateY(-2px);
  }
</style>