import { defineConfig } from 'umi';

export default defineConfig({
    nodeModulesTransform: {
        type: 'none',
    },
    routes: [
        { path: '/user', title: 'user', component: '@/pages/user' },
        { path: '/', title: 'index', exact: false, component: '@/pages/index' },
    ],
    hash: true,
    title: 'GOLDx',
})