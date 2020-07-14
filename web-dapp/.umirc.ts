import { defineConfig } from 'umi';

export default defineConfig({
    nodeModulesTransform: {
        type: 'none',
    },
    // routes: [
    //     { path: '/user', title: 'user', component: '@/pages/user' },
    //     { path: '/', title: 'dForce GOLDx', exact: false, component: '@/pages/index' },
    // ],
    hash: true,
    title: 'dForce GOLDx',
    favicon: '/favicon.ico',
    publicPath: './',
    history: { type: 'hash' }
})