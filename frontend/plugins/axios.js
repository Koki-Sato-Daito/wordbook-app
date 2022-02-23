export default function ({ $axios, redirect }) {
    $axios.onRequest(config => {
        console.log(`(${config.method}) ${config.url} body=${JSON.stringify(config.data)}` +  
        `params=${JSON.stringify(config.params)}`);
    })

    $axios.onError(error => {
        const code = parseInt(error.response && error.response.status);
        console.log('Response status code is ' + code);
    })
}