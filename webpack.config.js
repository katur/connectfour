const ExtractTextPlugin = require('extract-text-webpack-plugin');
const WebpackNotifierPlugin = require('webpack-notifier');


module.exports = {
  entry: './connectfour/web/static/js/src/connectfour.js',
  output: {
    path: './connectfour/web/static/js/bin',
    filename: 'connectfour.bundle.js'
  },
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: [/node_modules/],
      loader: 'babel-loader'
    }, {
      test: /\.sass$/,
      exclude: [/node_modules/],
      loader: ExtractTextPlugin.extract('css!sass')
    }]
  },
  plugins: [
    new ExtractTextPlugin('../../stylesheets/bin/styles.css', {
      allChunks: true
    }),
    new WebpackNotifierPlugin()
  ],
  resolve: {
    extensions: ['', '.webpack.js', '.web.js', '.js', '.jsx', '.sass']
  }
};
