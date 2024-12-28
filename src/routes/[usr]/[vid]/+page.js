export const load = async ({ params }) => {
    const fetchVideo = async () => {
        let vid = params.vid;
        let user = params.usr;
        const iscomp = await iscompressed();
        if (iscomp) {
            vid = `c-${vid}`;
        }
        return `http://localhost:3000/pullvid?u=${user}&v=${vid}`;
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
