


export const load = async ({ params }) => {
    function truncateString(str) {
        if (str.length > 10) {
          return str.slice(2); // Remove the first 2 characters
        }
        return str; // Return the string unchanged if it's not longer than 10
      }
    
    const fetchVideo = async () => {
        let vid = params.vid;
        let user = params.usr;
        return `http://localhost:3000/pullvid?u=${user}&v=c-${truncateString(vid)}`;
    };

    const iscompressed = async () => {
        let vid = params.vid;
        let user = params.usr;
        const response = await fetch(`http://localhost:3000/iscompressed?u=${user}&v=${vid}`);
        const data = await response.json();
        console.log(data);
        return data.compressed;
    };

    return {
        video_url: await fetchVideo(),
        iscompressed: await iscompressed()
    };
};
