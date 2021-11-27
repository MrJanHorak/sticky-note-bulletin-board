// if you have multiple .draggable elements
// get all draggie elements
const draggableElems = document.querySelectorAll(".draggable");
// array of Draggabillies
let draggies = [];
// init Draggabillies
for (let x = 0; x < draggableElems.length; x++) {
  let draggableElem = draggableElems[x];
  let draggie = new Draggabilly(draggableElem);
  draggie.on("dragEnd", function () {
    console.log("dragEnd");
  });
  draggies.push(draggie);
}
