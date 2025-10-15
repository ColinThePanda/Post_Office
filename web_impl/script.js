function getElement(id) {
  const element = document.getElementById(id);
  if (element !== null) {
    return element;
  }
  throw new Error(`Id not found ${id}`);
}

class PostSize {
  constructor(length, height, thickness) {
    this.length = length;
    this.height = height;
    this.thickness = thickness;
  }

  between(min, max) {
    return (
      this.length >= min.length &&
      this.length <= max.length &&
      this.height >= min.height &&
      this.height <= max.height &&
      this.thickness >= min.thickness &&
      this.thickness <= max.thickness
    );
  }
}

function between(number, min, max) {
  return number >= min && number <= max;
}

class Zip {
  constructor(start_zip, end_zip) {
    this.start_zip = start_zip;
    this.end_zip = end_zip;
  }

  size() {
    let from = -1;
    let end = -1;
    if (between(this.start_zip, 1, 6999)) {
      from = 1;
    } else if (between(this.start_zip, 7000, 19999)) {
      from = 2;
    } else if (between(this.start_zip, 20000, 35999)) {
      from = 3;
    } else if (between(this.start_zip, 36000, 62999)) {
      from = 4;
    } else if (between(this.start_zip, 64000, 84999)) {
      from = 5;
    } else if (between(this.start_zip, 85000, 99999)) {
      from = 6;
    } else {
      alert("Start zip must be between 1 and 99,999");
      return;
    }
    if (between(this.end_zip, 1, 6999)) {
      end = 1;
    } else if (between(this.end_zip, 7000, 19999)) {
      end = 2;
    } else if (between(this.end_zip, 20000, 35999)) {
      end = 3;
    } else if (between(this.end_zip, 36000, 62999)) {
      end = 4;
    } else if (between(this.end_zip, 64000, 84999)) {
      end = 5;
    } else if (between(this.end_zip, 85000, 99999)) {
      end = 6;
    } else {
      alert("End zip must be between 1 and 99,999");
      return;
    }
    return Math.abs(from - end);
  }
}

class PostType {
  constructor(name, base_cost, shipping_cost, min_size, max_size) {
    this.name = name;
    this.base_cost = base_cost;
    this.shipping_cost = shipping_cost;
    this.min_size = min_size;
    this.max_size = max_size;
  }
}

const PostTypes = Object.freeze({
  REGULAR_CARD: new PostType(
    "Card",
    0.2,
    0.03,
    new PostSize(3.5, 3.5, 0.007),
    new PostSize(4.25, 6, 0.016)
  ),
  LARGE_CARD: new PostType(
    "Large Card",
    0.37,
    0.03,
    new PostSize(4.25, 6, 0.007),
    new PostSize(6, 11.5, 0.015)
  ),
  REGULAR_ENVELOPE: new PostType(
    "Envelope",
    0.37,
    0.04,
    new PostSize(3.5, 5, 0.16),
    new PostSize(6.125, 11.5, 0.25)
  ),
  LARGE_ENVELOPE: new PostType(
    "Large Envelope",
    0.6,
    0.05,
    new PostSize(6.125, 11, 0.25),
    new PostSize(24, 18, 0.5)
  ),
  REGULAR_PACKAGE: new PostType("Package", 2.95, 0.25),
  LARGE_PACKAGE: new PostType("Large Package", 3.95, 0.35),
  UNMAILABLE: new PostType("Unmailable"),
});

class PostData {
  constructor(data) {
    this.length = data[0];
    this.height = data[1];
    this.thickness = data[2];
    this.start_zip = data[3];
    this.end_zip = data[4];
  }
}

function classyify(data) {
  let size = new PostSize(data.length, data.height, data.thickness);
  for (const [name, type] of Object.entries(PostTypes)) {
    if (type.min_size && type.max_size) {
      let between = size.between(type.min_size, type.max_size);
      if (between === true) {
        const matchedTypeName = Object.keys(PostTypes).find(
          (key) => PostTypes[key] === type
        );
        return type;
      }
    }
  }
  let girth = 2 * data.height + 2 * data.length;
  if (girth >= 0 && girth <= 84) {
    return PostTypes.REGULAR_PACKAGE;
  } else if (girth > 84 && girth <= 130) {
    return PostTypes.LARGE_PACKAGE;
  } else {
    return PostTypes.UNMAILABLE;
  }
}

function getCost(data) {
  let post_type = classyify(data);
  let zip = new Zip(data.start_zip, data.end_zip);
  let distance = zip.size();
  if (post_type === PostTypes.UNMAILABLE) {
    return -1;
  }
  return post_type.base_cost + post_type.shipping_cost * distance;
}

function handleSubmit() {
  const data_parts = [
    document.getElementById("length"),
    document.getElementById("height"),
    document.getElementById("thickness"),
    document.getElementById("start_zip"),
    document.getElementById("end_zip"),
  ];
  for (const [index, part] of data_parts.entries()) {
    if (part === null) {
      return;
    }
    if (!(part instanceof HTMLInputElement)) {
      return;
    }
    value = Number(part.value);
    if (value == 0) {
      return;
    }
    data_parts[index] = value;
  }

  let post_data = new PostData(data_parts);
  console.log(
    `Length: ${post_data.length}\nHeight: ${post_data.height}\nThickness: ${post_data.thickness}\nStart Zip: ${post_data.start_zip}\nEnd Zip: ${post_data.end_zip}`
  );
  let post_type = classyify(post_data);

  let add_html = `
    <div class="results-container">
    <div class="result-div">
        <h2>Post Type:<br />${post_type.name}<br /></h2>
    </div>
    <div class="result-div">
        <h2>Cost:<br />$${getCost(post_data).toFixed(2)}</h2>
    </div>
    </div>
  `;

  let add_div = document.getElementById("selection-container");

  if (add_div === null) {
    document.body.insertAdjacentHTML(
      "beforeend",
      `<br />
    <br />
    <div class="section" id="selection-container">${add_html}</div>`
    );
  } else {
    add_div.innerHTML = add_html;
  }
}

const button = getElement("submit");
button.addEventListener("click", handleSubmit);
