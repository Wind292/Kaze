export const load = ({ params }) => {
    const fetchVideo = () => {
        // You can adjust this to return the actual video URL based on params
        return `http://localhost:3000/${params.usr}/${params.vid}.mp4`; 
    };

    return {
        video_url: fetchVideo()
    };
};
