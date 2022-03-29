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


