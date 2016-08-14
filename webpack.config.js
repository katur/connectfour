var ExtractTextPlugin = require("extract-text-webpack-plugin");


module.exports = {
  entry: "./connectfour/views/web/static/src/js/app.js",
  output: {
    path: "./connectfour/views/web/static/bin/js",
    filename: "app.bundle.js"
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: [/node_modules/],
      loader: "babel-loader"
    }, {
      test: /\.sass$/,
      exclude: [/node_modules/],
      loader: ExtractTextPlugin.extract("css!sass")
    }]
  },
  plugins: [
    new ExtractTextPlugin("../stylesheets/styles.css", {
      allChunks: true
    })
  ]
};
