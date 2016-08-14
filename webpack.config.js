var ExtractTextPlugin = require("extract-text-webpack-plugin");


module.exports = {
  entry: "./connectfour/views/web/static/js/app.js",
  output: {
    path: "./connectfour/views/web/static/js",
    filename: "app.bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.sass$/,
        loader: ExtractTextPlugin.extract("css!sass")
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin("../stylesheets/styles.css", {
      allChunks: true
    })
  ]
};
