const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = (env, args) => ({
  devtool: 'source-map',
  mode: args.mode,
  entry: './src/index.js',
  watch: args.mode === 'development',
  output: {
    path: path.resolve(__dirname + '../../../src/static/twitter_bot'),
    filename: '[name].[contenthash].js'
  },
  plugins: [
    new CleanWebpackPlugin({
      cleanOnceBeforeBuildPatterns: ['**/*', '!images/**', '!site_media/**']
    }),
  ],
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          chunks: 'initial',
          name: 'vendors',
          enforce: true,
          minSize: 70000, // 限制最小大小 ( byte )
        },
        default: {
          name: 'main',
        },
      },
    },
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'], // Load CSS files
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/,
        use: ['file-loader'], // Load image files
      },
    ]
  }
});