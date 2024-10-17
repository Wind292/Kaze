export const load = ({ params, fetch }) => {
    const fetchVideo = async () => {
        // You can adjust this to return the actual video URL based on params
        const res = await fetch(`http://localhost:3000/usrinfo/${params.usr}`)

        console.log(res.json)

        return await res.json();
    };

    return fetchVideo()
 
};
