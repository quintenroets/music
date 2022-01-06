import http from "./HttpService.ts"

class MusicService {
    getNewArtist(name){
        return http
            .get("/newartist", {params: {"name": name}})
            .then(response => {
                return response.data;
            });

    }
    addArtist(id, name){
        return http
            .get("/addartist", {params: {"id": id, "name": name}})
            .then(response => {
                return response.data;
            });
    }
    ChangeArtist(id){
        return http
            .get("/changeartist", {params: {"id": id}})
            .then(response => {
                return response.data;
            });
    }

    getRecommendedArtists(){
        return http
            .get("/recommendedartists")
            .then(response => {
                return response.data;
            });
    }

    getArtists(){
        return http
            .get("/artists")
            .then(response => {
                return response.data;
            });
    }
}

export default new MusicService();