const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: './',
  devServer: {
    allowedHosts: 'all',
    host: '0.0.0.0',
    client: {
      webSocketURL: {
        hostname: '0.0.0.0',
        pathname: '/ws',
        port: 8080
      }
    }
  }
})
