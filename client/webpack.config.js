const path = require( 'path' );
const webpack = require( 'webpack' );
const CopyPlugin = require('copy-webpack-plugin');

module.exports = {
    entry: {
        main: [
            path.resolve(__dirname, 'src/index.js')
        ]
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].bundle.js',
        sourceMapFilename: '[name].bundle.map'
    },
    module: {
        rules: [
            {
                test: /\.jsx?/,
                exclude: /node_modules/,
                use: 'babel-loader'
            },
            {
                test: /\.css$/i,
                exclude: /node_modules/,
                use: ['style-loader', 'css-loader']
            }
        ]
    },
    plugins: [
        new webpack.NamedModulesPlugin(),
        new CopyPlugin([{ from: "src/index.html", to: "index.html" }])
    ]
};
