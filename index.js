restartButton = document.getElementById("restart-button");

restartButton.addEventListener("click", () => {
  for (let i = 0; i < 1000; i++) {
    setTimeout(() => {
      document.getElementById("button").click();
    }, 100);
  }
});

let htmlElements = "";
for (let i = 0; i < 200; i++) {
  if (i < 150) {
    htmlElements += `<div class="row row${i}" ><div class="box seat row${i} seat1"></div><div class="box seat row${i} seat2"></div><div class="box aisle row${i}"></div><div class="box seat seat3 row${i}"></div><div class="box seat row${i} seat4"></div></div>`;
  } else {
    htmlElements += `<div class="row row${i} bigBox seatsDisplayed" ><div class="box seat row${i} seat1"></div><div class="box seat row${i} seat2"></div><div class="box aisle row${i}"></div><div class="box seat seat3 row${i}"></div><div class="box seat row${i} seat4"></div></div>`;
  }
}
let container = document.getElementById("container");
container.innerHTML = htmlElements;

$.getJSON(
  "./output.json",
  function (output) {
    var out = output.everyStep.length;
    button = document.getElementById("button");
    //for (let i = 0; i < output.everyStep.length; i++) {
    //actualPosition = output.everyStep[i];

    let i = 0;

    button.addEventListener("click", () => {
      i++;
      for (let j = 0; j < 200; j++) {
        row = document.querySelector(`.row${j}`);
        string = output.everyStep[i][j];
        //console.log(string)
        //console.log(giveSeat(string, "aisle"))
        //console.log(giveSeat(string,"rightWindow"))
        place = document.querySelector(`.row${j}.seat1`);
        if (giveSeat(string, "leftWindow").localeCompare("000") != 0) {
          place.classList.add("occupied");
        } else if (place.classList.contains("occupied")) {
          place.classList.remove("occupied");
        }

        place = document.querySelector(`.row${j}.seat2`);
        if (giveSeat(string, "leftAisle").localeCompare("000") != 0) {
          place.classList.add("occupied");
        } else if (place.classList.contains("occupied")) {
          place.classList.remove("occupied");
        }

        place = document.querySelector(`.row${j}.aisle`);
        if (giveSeat(string, "aisle").localeCompare("000") != 0) {
          place.classList.add("occupied");
        } else if (place.classList.contains("occupied")) {
          place.classList.remove("occupied");
        }

        place = document.querySelector(`.row${j}.seat3`);
        if (giveSeat(string, "rightAisle").localeCompare("000") != 0) {
          place.classList.add("occupied");
        } else if (place.classList.contains("occupied")) {
          place.classList.remove("occupied");
        }

        place = document.querySelector(`.row${j}.seat4`);
        if (giveSeat(string, "rightWindow").localeCompare("000") != 0) {
          place.classList.add("occupied");
        } else if (place.classList.contains("occupied")) {
          place.classList.remove("occupied");
        }

        //setTimeout(someFunction(), 1000);
      }
    });
  }
  //}
);

function someFunction() {
  console.log("Wait");
}

function giveSeat(string, seatPosition) {
  switch (seatPosition) {
    case "leftWindow":
      return string.substring(0, 3);
    case "leftAisle":
      return string.substring(3, 6);
    case "rightAisle":
      return string.substring(9, 12);
    case "rightWindow":
      return string.substring(12, 15);
    case "aisle":
      return string.substring(6, 9);
    default:
      return "000";
  }
}
