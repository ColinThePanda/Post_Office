function getElement(id) {
    const element = document.getElementById(id)
    if (element !== null) {
        return element
    }
    throw new Error(`Id not found ${id}`)
}

class PostData {
    constructor(line) {
        this.data = this.extract_line_data(line)
    }

    extract_line_data(line) {
        let index = line.indexOf(". ")
        data = line.substring(index+2)
        data_arr = data.split(",")
        return data_arr
    }
}

function handleSubmit() {
    const length_input = document.getElementById("length")
    if (length_input === null) {
        return
    }
    if (!(length_input instanceof  HTMLInputElement)) {
        return
    }
    let length = length_input.value
    if (length === null) {
        length = ""
    }
    //alert(length)
    length_input.value = ""
    let post_data = new PostData("1. 4,4,.009,02893,08516")
    alert(post_data.data)
}

const button = getElement("submit");
button.addEventListener("click", handleSubmit);