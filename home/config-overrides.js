const {
    override,
    addWebpackAlias,
    addWebpackModuleRule
} = require("customize-cra");
const path = require("path");
const resolve = dir => path.join(__dirname, dir);
module.exports = override(
    addWebpackAlias({
        "@": resolve("src"),
        "@pages": resolve("src/pages"),
        "@img": resolve("src/static/img"),
        "@components": resolve("src/components"),
    }),
    addWebpackModuleRule({
        test: /\.(eot|woff2?|ttf|svg)$/,
        exclude: path.resolve(__dirname, "./src/icons"),
        use: [
            {
                loader: "url-loader",
                options: {
                    name: "[name]-[hash:5].min.[ext]",
                    limit: 5000,
                    outputPath: "./static/images",
                    publicPath: "../../static/images",
                },
            },
        ],
    }),
    addWebpackModuleRule({
        test: /\.svg$/,
        loader: "svg-sprite-loader",
        include: path.resolve(__dirname, "./src/icons"),
        options: {
            symbolId: "icon-[name]",
        },
    })
);