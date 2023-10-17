module.exports = {
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
            use: ['style-loader', 'css-loader']
        },
        {
            test: /\.svg$/,
            use: 'file-loader', // or 'url-loader' if you prefer
        },
      ]
    }
  };