console.log("Hello World from JS");

const express = require("express");
var api = express();
const port = '8080'

api.use(express.static(__dirname+'/'));

api.get("/", (req, res) => {
    console.log('deeeeeeeeeeeeeeeeeeeeeeeeee')
    res.send("Hello World");
});

api.post('/add', (req, res) => {
    // console.log(req);
    res.json({'f': 'ffffffffffffffffffffff'})
    console.log('Post request recieved')
});

// THIS BELONGS AT THE BOTTOM FOREVER
api.listen(port, () => {
    console.log("API is up, port:"+port);
});
