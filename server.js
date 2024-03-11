//..............Include Express..................................//
const express = require("express");
const fs = require("fs");
const handlebars = require("express-handlebars");
// const fetch = require("node-fetch");

//..............Create an Express server object..................//
const app = express();

//..............Apply Express middleware to the server object....//
app.use(express.json()); //Used to parse JSON bodies (needed for POST requests)
app.use(express.urlencoded());
app.use(express.static("public")); //specify location of static assests
app.set("views", __dirname + "/views"); //specify location of templates
app.set("view engine", "handlebars"); //specify templating library
app.engine(
  "handlebars",
  handlebars({
    layoutsDir: __dirname + "/views/layouts",
  }),
); //Sets handlebars configurations

//.............Define server routes..............................//
const port = 3000;
//Sets a basic route
app.get("/", (req, res) => res.send("Hello World !"));

//Makes the app listen to port 3000
app.listen(port, () => console.log(`App listening to port ${port}`));
