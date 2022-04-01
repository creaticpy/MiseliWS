function replacer(key, value) {
    if (typeof value === 'function') {
        return value.toString()
    }
    if (key === 'clave') {

    } else if (key === 'valor') {

    }
    console.log(key.name, value, "key y value en value nro llamada:")
    return value
}

// https://gomakethings.com/serializing-form-data-with-the-vanilla-js-formdata-object/
function serialize(form_id) {
    let obj = {};
    let formData = new FormData(document.getElementById(form_id));
    for (let key of formData.keys()) {
        obj[key] = formData.get(key);
    }
    return JSON.stringify(obj)
    // return obj
}

function guardarformulario(id, form_id, url) {

    console.log(url, "esto es url")


    let datos = serialize(form_id)
    let csrf = JSON.parse(datos)['csrfmiddlewaretoken']

    axios({
        method: 'post',
        url: url,
        data: datos,
        headers: {
            "X-CSRFToken": csrf,
            "content-type": "application/json"
        }
    })
        .then(function (respuesta) {

            console.log(respuesta)

        }).catch(function (err) {
        console.log(err)
    })
}
