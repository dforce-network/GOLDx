const { override,addWebpackModuleRule,addWebpackPlugin,} = require("customize-cra");
const path = require("path")
const UglifyJsPlugin = require('uglifyjs-webpack-plugin'); // 代码压缩
const publicPathPlugin = (config, env) => {
    config.devtool = "nosources-source-map"
    config.output = {
      filename: "js/[name].[hash:8].js",
      path: path.resolve(__dirname, "build"),
      publicPath: '/',
      chunkFilename: "js/[name].[hash:8].js"
    }

    return config
  }
  module.exports =  {
    webpack: override(
    publicPathPlugin,
    addWebpackPlugin(
      new UglifyJsPlugin({
        // 开启打包缓存
        cache: true,
        // 开启多线程打包
        parallel: true,
        uglifyOptions: {
          // 删除警告
          warnings: false,
          // 压缩
          compress: {
            // 移除console
            drop_console: true,
            // 移除debugger
            drop_debugger: true,
          },
        },
      })
    ),
    addWebpackModuleRule({
        test: [/\.bmp$/, /\.gif$/, /\.jpe?g$/, /\.png$/, /\.svg$/,/\.otf$/,/\.ttf$/],
        loader: require.resolve('url-loader'),
        options: {
          limit: 64,
          name: 'media/[name].[hash:8].[ext]',
        },
    }),
    addWebpackModuleRule({
        test: [/\.css$/], 
        use: ['style-loader', 'css-loader'],
        // use: [
        //     'style-loader',
        //     {
        //       loader: 'css-loader',
        //       options: {
        //         modules: {localIdentName: 'css/[name].[hash:8].css'},
        //         sourceMap:false
        //       },
        //     }
        //   ],
    })
   )
  }